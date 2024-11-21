from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
import csv
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import AIMessage, HumanMessage
from fastapi.middleware.cors import CORSMiddleware

# .env 파일 로드
load_dotenv()

app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 대화 기록을 저장할 디렉토리 생성
CHAT_HISTORY_DIR = "chat_histories"
os.makedirs(CHAT_HISTORY_DIR, exist_ok=True)

# OpenAI 모델 초기화
llm = ChatOpenAI(model="gpt-4-0125-preview", temperature=0.7)

# 프롬프트 템플릿 정의
prompt = ChatPromptTemplate.from_messages([
    ("system", """당신은 Todo 리스트 관리를 도와주는 생산성 전문가입니다. 
    사용자의 Todo 리스트를 분석하고 다음과 같은 도움을 제공해주세요:
    1. 할일의 우선순위나 구조화에 대한 제안
    2. 생산성을 높일 수 있는 팁
    3. 완료된 일에 대한 긍정적인 피드백
    4. 미완료된 일에 대한 동기부여
    이전 대화 내용을 참고하여 더 개인화된 조언을 제공해주세요.
    한국어로 친근하고 전문적으로 조언해주세요."""),
    MessagesPlaceholder(variable_name="history"),
    ("human", "다음 Todo 리스트를 분석해주세요:\n{todo_list}")
])

def get_chat_history(session_id: str):
    """CSV 파일에서 채팅 기록을 읽어옵니다."""
    messages = []
    csv_path = os.path.join(CHAT_HISTORY_DIR, f"{session_id}.csv")
    
    if os.path.exists(csv_path):
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['type'] == 'human':
                    messages.append(HumanMessage(content=row['content']))
                elif row['type'] == 'ai':
                    messages.append(AIMessage(content=row['content']))
    
    return messages

def save_chat_history(session_id: str, human_message: str, ai_message: str):
    """채팅 기록을 CSV 파일에 저장합니다."""
    csv_path = os.path.join(CHAT_HISTORY_DIR, f"{session_id}.csv")
    file_exists = os.path.exists(csv_path)
    
    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['timestamp', 'type', 'content'])
        
        if not file_exists:
            writer.writeheader()
        
        timestamp = datetime.now().isoformat()
        writer.writerow({
            'timestamp': timestamp,
            'type': 'human',
            'content': human_message
        })
        writer.writerow({
            'timestamp': timestamp,
            'type': 'ai',
            'content': ai_message
        })

# 간단한 in-memory database
todos = []
current_id = 0

class Todo(BaseModel):
    id: Optional[int] = None
    title: str
    completed: bool = False

class AIRequest(BaseModel):
    todo_list: str
    session_id: str

@app.get("/todos", response_model=List[Todo])
async def get_todos():
    return todos

@app.post("/todos", response_model=Todo)
async def create_todo(todo: Todo):
    global current_id
    current_id += 1
    todo.id = current_id
    todos.append(todo)
    return todo

@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo: Todo):
    todo_idx = next((i for i, t in enumerate(todos) if t.id == todo_id), -1)
    if todo_idx == -1:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.id = todo_id
    todos[todo_idx] = todo
    return todo

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    todo_idx = next((i for i, t in enumerate(todos) if t.id == todo_id), -1)
    if todo_idx == -1:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos.pop(todo_idx)
    return {"message": "Todo deleted"}

@app.post("/analyze-todos")
async def analyze_todos(request: AIRequest):
    try:
        # 이전 대화 기록 가져오기
        history = get_chat_history(request.session_id)
        
        # 프롬프트에 대화 기록 포함하여 실행
        response = prompt.invoke({
            "history": history,
            "todo_list": request.todo_list
        })
        result = llm.invoke(response)
        
        # 새로운 대화 내용 저장
        save_chat_history(request.session_id, request.todo_list, result.content)
        
        return {"advice": result.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8002)
    args = parser.parse_args()
    uvicorn.run(app, host="127.0.0.1", port=args.port)