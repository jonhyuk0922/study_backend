
# 프로젝트 구조 및 HTTP Methods 정리

## HTTP Methods

### **PUT (Update)**
- **사용 목적:** 기존 리소스를 수정/갱신
- **요청 본문:** 수정할 데이터를 담아 전송
- **특징:**
  - 리소스의 **모든 필드**를 업데이트
  - **멱등성:** 동일한 요청을 여러 번 보내도 결과가 같음
  - 리소스 전체 교체에 사용
  - 존재하지 않는 리소스에 대해서는 **404 에러 반환**
  - 요청 시 **모든 필드**를 포함해야 함

#### **예시:**
```http
PUT /resource/1 HTTP/1.1
Host: example.com
Content-Type: application/json

{
  "field1": "updated_value",
  "field2": "updated_value"
}
```

---

### **DELETE (Delete)**
- **사용 목적:** 기존 리소스를 삭제
- **요청 본문:** 일반적으로 필요 없음
- **특징:**
  - **멱등성:** 동일한 요청을 여러 번 호출해도 결과는 동일
  - 성공 시 일반적으로 **204 No Content** 또는 **200 OK** 반환
  - 이미 삭제된 리소스에 대한 요청은 **404 반환**
  - 단순하고 명확한 동작

#### **예시:**
```http
DELETE /resource/1 HTTP/1.1
Host: example.com
```

---

## 현재 코드베이스의 구현

### **FastAPI 백엔드**
- **PUT 구현:**
```python
@app.put("/resource/{resource_id}")
async def update_resource(resource_id: int, data: ResourceModel):
    existing_resource = get_resource_by_id(resource_id)
    if not existing_resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    update_resource_in_db(resource_id, data)
    return {"message": "Resource updated successfully"}
```

- **DELETE 구현:**
```python
@app.delete("/resource/{resource_id}")
async def delete_resource(resource_id: int):
    existing_resource = get_resource_by_id(resource_id)
    if not existing_resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    delete_resource_from_db(resource_id)
    return {"message": "Resource deleted successfully"}
```

---

### **프론트엔드에서의 구현**
- **PUT 요청:** 수정된 데이터를 포함하여 API 호출
- **DELETE 요청:** 리소스를 삭제하는 단순 API 호출

---

## CRUD 작업
- 현재 코드베이스는 FastAPI를 기반으로 구현되어 있으며, CRUD 작업을 완전히 지원
- RESTful API의 기본 원칙에 충실하게 설계됨
