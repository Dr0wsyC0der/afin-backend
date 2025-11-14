# Примеры запросов для проверки работы сервисов

Базовый URL: `http://localhost:8000`

## 1. Проверка Gateway и всех сервисов

### Проверка здоровья Gateway и всех сервисов
```bash
GET http://localhost:8000/health
```

**Ожидаемый ответ:**
```json
{
  "gateway": "ok",
  "services": {
    "auth": {"status": "ok", "service": "auth"},
    "models": {"status": "ok", "service": "models"},
    "simulation": {"status": "ok", "service": "simulation"},
    "analytics": {"status": "ok", "service": "analytics"}
  }
}
```

---

## 2. Сервис Auth (Аутентификация)

### Проверка здоровья сервиса
```bash
GET http://localhost:8000/api/v1/auth/health
```

### Регистрация нового пользователя
```bash
POST http://localhost:8000/api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Ожидаемый ответ:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true
}
```

### Вход (получение токена)
```bash
POST http://localhost:8000/api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=password123
```

**Ожидаемый ответ:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## 3. Сервис Models (Модели бизнес-процессов)

### Проверка здоровья сервиса
```bash
GET http://localhost:8000/api/v1/models/health
```

### Создание модели
```bash
POST http://localhost:8000/api/v1/models/
Content-Type: application/json

{
  "name": "Test Process Model",
  "data": {
    "process_id": "proc1",
    "elements": [
      {"type": "task", "id": "task1", "name": "Task 1"},
      {"type": "task", "id": "task2", "name": "Task 2"}
    ]
  },
  "user_id": 1
}
```

**Ожидаемый ответ:**
```json
{
  "id": 1,
  "name": "Test Process Model",
  "data": {...},
  "user_id": 1
}
```

### Получение списка моделей
```bash
GET http://localhost:8000/api/v1/models/
```

### Получение модели по ID
```bash
GET http://localhost:8000/api/v1/models/1
```

### Обновление модели
```bash
PUT http://localhost:8000/api/v1/models/1
Content-Type: application/json

{
  "name": "Updated Model Name"
}
```

### Удаление модели
```bash
DELETE http://localhost:8000/api/v1/models/1
```

### Импорт BPMN файла
```bash
POST http://localhost:8000/api/v1/models/import/bpmn
Content-Type: multipart/form-data

[Файл BPMN]
```

### Экспорт модели в BPMN
```bash
GET http://localhost:8000/api/v1/models/1/export/bpmn
```

---

## 4. Сервис Simulation (Симуляция)

### Проверка здоровья сервиса
```bash
GET http://localhost:8000/api/v1/simulation/health
```

### Запуск симуляции
```bash
POST http://localhost:8000/api/v1/simulation/
Content-Type: application/json

{
  "model_id": 1,
  "model_data": {
    "elements": [
      {"type": "task", "id": "task1", "name": "Task 1", "duration": 2.5},
      {"type": "task", "id": "task2", "name": "Task 2", "duration": 1.0}
    ]
  }
}
```

**Ожидаемый ответ:**
```json
{
  "id": 1,
  "model_id": 1,
  "results": null,
  "duration": null,
  "status": "running"
}
```

### Получение результата симуляции
```bash
GET http://localhost:8000/api/v1/simulation/1
```

**Ожидаемый ответ (после завершения):**
```json
{
  "id": 1,
  "model_id": 1,
  "results": {
    "completed_tasks": 2,
    "total_simulation_time": 0.123,
    "status": "completed"
  },
  "duration": 0.123,
  "status": "completed"
}
```

---

## 5. Сервис Analytics (Аналитика)

### Проверка здоровья сервиса
```bash
GET http://localhost:8000/api/v1/analytics/health
```

### Базовый эндпоинт
```bash
GET http://localhost:8000/api/v1/analytics/
```

**Ожидаемый ответ:**
```json
{
  "message": "Hello from analytics service!"
}
```

---

## Примеры с использованием cURL

### Проверка здоровья всех сервисов
```bash
curl http://localhost:8000/health
```

### Регистрация пользователя
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "test123"}'
```

### Вход
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=test123"
```

### Создание модели
```bash
curl -X POST http://localhost:8000/api/v1/models/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Process",
    "data": {"process_id": "proc1", "elements": []},
    "user_id": 1
  }'
```

### Запуск симуляции
```bash
curl -X POST http://localhost:8000/api/v1/simulation/ \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": 1,
    "model_data": {
      "elements": [
        {"type": "task", "id": "t1", "name": "Task", "duration": 1.0}
      ]
    }
  }'
```

---

## Примеры с использованием Python (requests)

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Проверка здоровья
response = requests.get(f"{BASE_URL}/health")
print(response.json())

# 2. Регистрация
response = requests.post(
    f"{BASE_URL}/api/v1/auth/register",
    json={"email": "user@example.com", "password": "password123"}
)
print(response.json())

# 3. Вход
response = requests.post(
    f"{BASE_URL}/api/v1/auth/login",
    data={"username": "user@example.com", "password": "password123"}
)
token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# 4. Создание модели
response = requests.post(
    f"{BASE_URL}/api/v1/models/",
    json={
        "name": "Test Model",
        "data": {"process_id": "proc1", "elements": []},
        "user_id": 1
    }
)
model_id = response.json()["id"]

# 5. Запуск симуляции
response = requests.post(
    f"{BASE_URL}/api/v1/simulation/",
    json={
        "model_id": model_id,
        "model_data": {
            "elements": [
                {"type": "task", "id": "t1", "name": "Task", "duration": 1.0}
            ]
        }
    }
)
simulation_id = response.json()["id"]

# 6. Получение результата
import time
time.sleep(2)  # Ждем завершения
response = requests.get(f"{BASE_URL}/api/v1/simulation/{simulation_id}")
print(response.json())
```

---

## Swagger UI (Интерактивная документация)

Доступна по адресу:
- Gateway: http://localhost:8000/docs
- Auth: http://localhost:8000/api/v1/auth/docs (через gateway)
- Models: http://localhost:8000/api/v1/models/docs (через gateway)
- Simulation: http://localhost:8000/api/v1/simulation/docs (через gateway)
- Analytics: http://localhost:8000/api/v1/analytics/docs (через gateway)

---

## Последовательность проверки

1. **Проверка Gateway**: `GET /health`
2. **Проверка Auth**: `GET /api/v1/auth/health`
3. **Регистрация**: `POST /api/v1/auth/register`
4. **Вход**: `POST /api/v1/auth/login`
5. **Проверка Models**: `GET /api/v1/models/health`
6. **Создание модели**: `POST /api/v1/models/`
7. **Проверка Simulation**: `GET /api/v1/simulation/health`
8. **Запуск симуляции**: `POST /api/v1/simulation/`
9. **Проверка Analytics**: `GET /api/v1/analytics/health`

