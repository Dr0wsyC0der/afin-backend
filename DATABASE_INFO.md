# Информация о базе данных

## Расположение базы данных

База данных PostgreSQL запущена в Docker контейнере. Данные хранятся в **Docker volume** `postgres_data`.

### Физическое расположение данных

Данные находятся в Docker volume, который обычно расположен по адресу:
- **Linux/Mac**: `/var/lib/docker/volumes/afin-backend_postgres_data/_data`
- **Windows**: `\\wsl$\docker-desktop-data\data\docker\volumes\afin-backend_postgres_data\_data` (если используется WSL2)

### Параметры подключения

```
Host: localhost (или db внутри Docker сети)
Port: 5432
Database: afin
User: afin
Password: secret
```

**Connection String:**
```
postgresql://afin:secret@localhost:5432/afin
```

## Способы просмотра базы данных

### 1. Через Python скрипт (рекомендуется)

```bash
python view_database.py
```

Этот скрипт покажет:
- Список всех таблиц
- Структуру каждой таблицы
- Количество записей
- Содержимое таблиц

### 2. Через psql (командная строка)

#### Подключение из контейнера:
```bash
docker-compose exec db psql -U afin -d afin
```

#### Подключение с локальной машины:
```bash
psql -h localhost -p 5432 -U afin -d afin
# Пароль: secret
```

#### Полезные команды psql:
```sql
-- Список всех таблиц
\dt

-- Описание таблицы
\d table_name

-- Просмотр данных
SELECT * FROM users;
SELECT * FROM process_models;
SELECT * FROM simulation_runs;

-- Количество записей в таблицах
SELECT 
    schemaname,
    tablename,
    n_live_tup as row_count
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;

-- Выход
\q
```

### 3. Через Docker exec

```bash
# Войти в контейнер БД
docker-compose exec db bash

# Внутри контейнера
psql -U afin -d afin
```

### 4. Через графические инструменты

#### DBeaver
1. Скачайте DBeaver: https://dbeaver.io/
2. Создайте новое подключение PostgreSQL
3. Параметры:
   - Host: `localhost`
   - Port: `5432`
   - Database: `afin`
   - Username: `afin`
   - Password: `secret`

#### pgAdmin
1. Скачайте pgAdmin: https://www.pgadmin.org/
2. Создайте новое подключение с теми же параметрами

#### VS Code расширения
- **PostgreSQL** (от Chris Kolkman)
- **SQLTools** с драйвером PostgreSQL

## Структура базы данных

### Таблицы в проекте:

1. **users** (сервис auth)
   - `id` - INTEGER PRIMARY KEY
   - `email` - VARCHAR UNIQUE
   - `hashed_password` - VARCHAR
   - `is_active` - BOOLEAN

2. **process_models** (сервис models)
   - `id` - INTEGER PRIMARY KEY
   - `name` - VARCHAR
   - `data` - JSON
   - `user_id` - INTEGER

3. **simulation_runs** (сервис simulation)
   - `id` - INTEGER PRIMARY KEY
   - `model_id` - INTEGER
   - `results` - JSON
   - `duration` - FLOAT
   - `status` - VARCHAR

## Полезные SQL запросы

### Просмотр всех пользователей
```sql
SELECT id, email, is_active FROM users;
```

### Просмотр всех моделей
```sql
SELECT id, name, user_id, created_at FROM process_models;
```

### Просмотр всех симуляций
```sql
SELECT id, model_id, status, duration FROM simulation_runs;
```

### Статистика по таблицам
```sql
SELECT 
    'users' as table_name, COUNT(*) as count FROM users
UNION ALL
SELECT 
    'process_models', COUNT(*) FROM process_models
UNION ALL
SELECT 
    'simulation_runs', COUNT(*) FROM simulation_runs;
```

### Очистка данных (осторожно!)
```sql
-- Удалить все данные из таблицы
TRUNCATE TABLE users CASCADE;
TRUNCATE TABLE process_models CASCADE;
TRUNCATE TABLE simulation_runs CASCADE;
```

## Резервное копирование

### Создание бэкапа
```bash
docker-compose exec db pg_dump -U afin afin > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Восстановление из бэкапа
```bash
docker-compose exec -T db psql -U afin afin < backup_20240101_120000.sql
```

## Управление volume

### Просмотр volumes
```bash
docker volume ls
docker volume inspect afin-backend_postgres_data
```

### Удаление данных (осторожно!)
```bash
# Остановить контейнеры
docker-compose down

# Удалить volume
docker volume rm afin-backend_postgres_data

# Запустить заново (создаст новый volume)
docker-compose up -d
```

## Проверка состояния БД

```bash
# Проверка здоровья БД
docker-compose exec db pg_isready -U afin

# Статистика БД
docker-compose exec db psql -U afin -d afin -c "SELECT version();"
docker-compose exec db psql -U afin -d afin -c "\l"  # Список баз данных
docker-compose exec db psql -U afin -d afin -c "\dt" # Список таблиц
```

