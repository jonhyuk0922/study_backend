# Backend CRUD 및 HTTP Methods 정리

## CRUD란?
CRUD는 대부분의 컴퓨터 소프트웨어가 가지는 기본적인 데이터 처리 기능을 묶어서 일컫는 말입니다.

- **Create (생성)**: 새로운 데이터 생성
- **Read (읽기)**: 데이터 조회
- **Update (갱신)**: 기존 데이터 수정
- **Delete (삭제)**: 데이터 삭제

## HTTP Methods와 CRUD의 관계

### GET (Read)
- 서버로부터 데이터를 조회할 때 사용
- URL에 데이터가 노출됨
- 브라우저 히스토리에 기록이 남음
- 북마크 가능
- 데이터 길이에 제한이 있음
- 캐시 가능

예시:
```http
GET /api/users/1
```

### POST (Create)
- 새로운 데이터를 생성할 때 사용
- 요청 본문(body)에 데이터를 담아 전송
- URL에 데이터가 노출되지 않음
- 브라우저 히스토리에 기록이 남지 않음
- 데이터 길이 제한이 없음
- 캐시할 수 없음

예시:
```http
POST /api/users
Content-Type: application/json

{
    "name": "홍길동",
    "email": "hong@example.com"
}
```

## GET과 POST의 주요 차이점

1. **보안성**
   - GET: URL에 데이터가 노출되어 보안에 취약
   - POST: 데이터가 body에 담겨 전송되어 상대적으로 안전

2. **데이터 길이**
   - GET: URL 길이 제한으로 인한 데이터 제한
   - POST: 데이터 길이 제한 없음

3. **캐싱**
   - GET: 캐시 가능
   - POST: 캐시 불가능

4. **사용 목적**
   - GET: 데이터 조회
   - POST: 데이터 생성/수정

5. **멱등성**
   - GET: 멱등성 있음 (여러 번 호출해도 같은 결과)
   - POST: 멱등성 없음 (호출할 때마다 새로운 리소스 생성 가능)
