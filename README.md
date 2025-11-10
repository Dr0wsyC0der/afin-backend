# AFIN Backend (v0.1)

Микросервисный бэкенд платформы **AFIN** — прогнозирующее управление бизнес-процессами.

---

## Сервисы

| Сервис | Порт | API |
|-------|------|-----|
| `gateway` | 8000 | `/api/v1/...` |
| `auth` | — | `/api/v1/auth/...` |
| `models` | — | `/api/v1/models/...` |
| `analytics` | — | `/api/v1/analytics/...` |
| `simulation` | — | `/api/v1/simulations/...` |

---

## Запуск

```bash
docker-compose up --build