import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# FastAPI 서버 URL을 환경변수로 설정하거나 기본값 사용
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8002")

# Session state 초기화
if 'todos' not in st.session_state:
    st.session_state.todos = []
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(hash(os.getpid()))

def get_todos():
    try:
        response = requests.get(f"{BACKEND_URL}/todos")
        st.session_state.todos = response.json()
        return st.session_state.todos
    except requests.exceptions.RequestException:
        st.error(f"백엔드 서버({BACKEND_URL})에 연결할 수 없습니다.")
        return st.session_state.todos

def add_todo(title):
    try:
        todo = {"title": title, "completed": False}
        response = requests.post(f"{BACKEND_URL}/todos", json=todo)
        if response.status_code == 200:
            st.session_state.todos.append(response.json())
            return True
        return False
    except requests.exceptions.RequestException:
        st.error("할일을 추가하는데 실패했습니다.")
        return False

def update_todo(todo):
    try:
        response = requests.put(f"{BACKEND_URL}/todos/{todo['id']}", json=todo)
        if response.status_code == 200:
            idx = next((i for i, t in enumerate(st.session_state.todos) if t['id'] == todo['id']), -1)
            if idx != -1:
                st.session_state.todos[idx] = response.json()
            return True
        return False
    except requests.exceptions.RequestException:
        st.error("할일을 업데이트하는데 실패했습니다.")
        return False

def delete_todo(todo_id):
    try:
        response = requests.delete(f"{BACKEND_URL}/todos/{todo_id}")
        if response.status_code == 200:
            st.session_state.todos = [todo for todo in st.session_state.todos if todo['id'] != todo_id]
            return True
        return False
    except requests.exceptions.RequestException:
        st.error("할일을 삭제하는데 실패했습니다.")
        return False

def get_ai_advice(todo_list_str, session_id):
    try:
        response = requests.post(
            f"{BACKEND_URL}/analyze-todos",
            json={"todo_list": todo_list_str, "session_id": session_id}
        )
        if response.status_code == 200:
            return response.json()["advice"]
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"AI 조언을 받아오는데 실패했습니다: {str(e)}")
        return None

# Streamlit UI
st.title("Todo 앱")

# 새 할일 추가
new_todo = st.text_input("새로운 할일")
if st.button("추가", key="add_button"):
    if new_todo:
        if add_todo(new_todo):
            st.success("할일이 추가되었습니다!")
            st.rerun()

# 할일 목록 표시
st.subheader("할일 목록")
todos = get_todos()

if not todos:
    st.info("할일이 없습니다. 새로운 할일을 추가해보세요!")
else:
    for idx, todo in enumerate(todos):
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            if todo['completed']:
                st.markdown(f"~~{todo['title']}~~")
            else:
                st.write(todo['title'])
        
        with col2:
            if st.button(
                "완료" if not todo['completed'] else "미완료", 
                key=f"toggle_{todo['id']}_{idx}"
            ):
                todo['completed'] = not todo['completed']
                if update_todo(todo):
                    st.rerun()
        
        with col3:
            if st.button(
                "삭제", 
                key=f"delete_{todo['id']}_{idx}"
            ):
                if delete_todo(todo['id']):
                    st.rerun()

    # AI 어시스턴트 섹션
    st.subheader("💡 AI 어시스턴트의 조언")
    if st.button("조언 받기", key="get_advice"):
        with st.spinner("AI가 할일 목록을 분석하고 있습니다..."):
            todo_list_str = "\n".join([
                f"- {'[완료] ' if todo['completed'] else '[미완료] '}{todo['title']}"
                for todo in todos
            ])
            
            advice = get_ai_advice(todo_list_str, st.session_state.session_id)
            if advice:
                st.markdown(advice)

# 디버깅용 session state 표시
if st.checkbox("Show session state", key="show_state"):
    st.write(st.session_state)