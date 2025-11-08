# Incident Tracker API

API-сервис для учёта инцидентов

| Метод | Путь | Тег | Описание | Параметры / Тело запроса | Ответ | Аутентификация |
|-------|------|-----|----------|--------------------------|-------|----------------|
| GET   | /api/v1/incidents/ | incidents | Список инцидентов | `status` (query, необязательный), `page` (query, необязательный, default=1), `page_size` (query, необязательный, default=50) | `ListIncidentResponseSchema` | Да |
| POST  | /api/v1/incidents/ | incidents | Создать новый инцидент | Тело: `NewIncidentRequestSchema` | `IncidentResponseSchema` | Да |
| PATCH | /api/v1/incidents/{incident_id} | incidents | Изменить статус инцидента | Path: `incident_id` (UUID), Тело: `NewIncidentStatusRequestSchema` | `IncidentResponseSchema` | Да |
| POST  | /api/v1/services/ | services | Создать новый сервис | Тело: `NewServiceRequestSchema` | `ServiceResponseSchema` | Нет |
| POST  | /api/v1/token/ | token | Создать токен | Тело: `CreateTokenRequestSchema` | `CreateTokenResponseSchema` | Нет |
| POST  | /api/v1/token/refresh | token | Обновить токен | Тело: `RefreshTokenRequestSchema` | `RefreshTokenResponseSchema` | Нет |
| POST  | /api/v1/token/revoke | token | Отозвать токен | Тело: `RevokeTokenRequestSchema` | `RevokeTokenResponseSchema` | Нет |


---

## 🚀 Как запустить

1. Склонировать репозиторий:

```bash
git clone git@github.com:aleksandrkomyagin/incident_tracker.git
cd incident_tracker
```

2. В корне проекта создать файл `.env` на основе [`.env.example`](https://github.com/aleksandrkomyagin/incident_tracker/blob/main/.env.example) 
и заполнить нужными значениями те переменные, где есть пометка `(Заполнить)`

3. Выполнить команду:

```bash
docker compose -f docker-compose.yml up --build
```

---

### Для работы с инцидентами сначала нужно зарегистрировать сервис, от имени которого будет производиться работа с инцидентами.
#### Сделал этот эндпоинт открытым для удобства. В теории, сервисы могут добавлять только уполномоченные люди, например, через админ-панель 
1. В Swagger на [вкладке](http://localhost/docs#/services/new_service_api_v1_services__post) введите нужные значение и создайте сервис

Тело запроса
```
{
  "name": "monitoring",
  "scopes": [
    "read",
    "write"
  ]
}
```
Ответ
```
{
  "id": "7c5f6d6e-ebb6-4bc3-8f5f-85fb6f5a6e4d",
  "name": "monitoring",
  "created_at": "08.11.2025 10:03:52",
  "scopes": [
    "read",
    "write"
  ]
}
```

2. Скопируйте `id` для получения токена доступа(JWT)

3. Откройте [вкладку](http://localhost/docs#/token/create_token_api_v1_token__post) для получения токена и вставьте его в тело запроса

Тело запрос
```
{
  "service_id": "7c5f6d6e-ebb6-4bc3-8f5f-85fb6f5a6e4d"
}
```
Ответ
```
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJSUzI1NiIsInR..."
}
```

4. Авторизуйтесь в Swagger используя `access_token`


### Работа с инцидентами

1. Создание инцидента

Тело запроса
```
{
  "source": "operator",
  "description": "Перестал заряжаться самокат"
}
```
Ответ
```
{
  "id": "49fcd8e9-4169-4afc-ad63-31e43e232efa",
  "status": "new",
  "source": "operator",
  "description": "Перестал заряжаться самокат",
  "created_at": "08.11.2025 10:26:12"
}
```

2. Получение списка инцидентов
#####
Доступные Query-параметры:
```
status: ["new", "in_progress", "resolved", "closed"]
page: число больше 1
page_size: число от 20 до 50
```
Запрос
```
http://localhost/api/v1/incidents/?page=1&page_size=50
```
Ответ
```
{
  "items": [
    {
      "id": "49fcd8e9-4169-4afc-ad63-31e43e232efa",
      "status": "new",
      "source": "operator",
      "description": "Перестал заряжаться самокат",
      "created_at": "08.11.2025 10:26:12"
    }
  ],
  "page": 1,
  "page_size": 50
}
```
Если параметр `status` не передан, то будут возвращены все инциденты

3. Обновление статуса инцидента

Запрос
```
http://localhost/api/v1/incidents/49fcd8e9-4169-4afc-ad63-31e43e232efa
```
Тело запроса
```
{
  "status": "in_progress"
}
```
Ответ
```
{
  "id": "49fcd8e9-4169-4afc-ad63-31e43e232efa",
  "status": "in_progress",
  "source": "operator",
  "description": "Перестал заряжаться самокат",
  "created_at": "08.11.2025 10:26:12"
}
```