
# Todo 앱 with AI 어시스턴트

할 일 관리와 AI 조언을 결합한 웹 애플리케이션입니다.

## 브랜치 설명
- **main**: 기본적인 Todo 리스트 관리 기능 (CRUD)
- **feat/add_llm**: OpenAI GPT-4를 활용한 AI 어시스턴트 기능 추가
  - Todo 리스트 분석 및 우선순위 제안
  - 생산성 향상을 위한 맞춤형 조언
  - CSV 기반 대화 기록을 통한 개인화된 피드백

## 프로젝트 구조
.
├── step1/
│   ├── backend/
│   │   ├── __pycache__/
│   │   │   └── main.cpython-311.pyc
│   │   └── main.py
│   ├── frontend/
│   │   └── app.py
│   ├── run.sh
│   └── setup.sh
│
└── step2/
    ├── backend/
    │   ├── __init__.py
    │   └── main.py
    ├── frontend/
    │   ├── __init__.py
    │   └── app.py
    ├── chat_histories/
    ├── setup.sh
    ├── .env.example
    └── README.md

## 프로젝트 설치 및 실행
### 복제
```bash
git clone <repository-url>
cd step2
```

### 설정

#### 설치 스크립트 실행
```bash
chmod +x setup.sh
./setup.sh
```

#### 환경 변수 설정
```bash
cp .env.example .env
```
`.env` 파일에 `OPENAI_API_KEY` 입력 (feat/add_llm 브랜치)

### 실행

#### 백엔드 실행
```bash
cd backend
uvicorn main:app --reload --port 8002
```

#### 프론트엔드 실행 (새 터미널에서)
```bash
cd frontend
streamlit run app.py
```

---

이제 Todo 리스트 관리와 AI 어시스턴트 기능을 함께 사용할 준비가 완료되었습니다!
