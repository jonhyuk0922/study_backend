from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import argparse

app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 간단한 in-memory database
todos = []
current_id = 0  # ID 관리를 위한 카운터 추가

class Todo(BaseModel):
    id: Optional[int] = None
    title: str
    completed: bool = False

@app.get("/todos", response_model=List[Todo])
async def get_todos():
    return [todo.dict() for todo in todos]

@app.post("/todos", response_model=Todo)
async def create_todo(todo: Todo):
    global current_id
    current_id += 1
    todo.id = current_id
    todos.append(todo)
    return todo.dict()

@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo: Todo):
    todo_idx = next((i for i, t in enumerate(todos) if t.id == todo_id), -1)
    if todo_idx == -1:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.id = todo_id
    todos[todo_idx] = todo
    return todo.dict()

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    todo_idx = next((i for i, t in enumerate(todos) if t.id == todo_id), -1)
    if todo_idx == -1:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos.pop(todo_idx)
    return {"message": "Todo deleted"}

if __name__ == "__main__":
    import uvicorn
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    uvicorn.run(app, host="127.0.0.1", port=args.port)