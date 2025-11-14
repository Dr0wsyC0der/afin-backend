#!/usr/bin/env python3
"""
Скрипт для просмотра содержимого базы данных AFIN
"""
import sys
from sqlalchemy import create_engine, inspect, text
from shared.config import settings

def print_section(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def view_database():
    """Просмотр содержимого базы данных"""
    print_section("ПОДКЛЮЧЕНИЕ К БАЗЕ ДАННЫХ")
    print(f"URL: {settings.DATABASE_URL.replace(settings.POSTGRES_PASSWORD, '***')}")
    
    try:
        # Создаем подключение
        engine = create_engine(settings.DATABASE_URL)
        
        # Проверяем подключение
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✅ Подключено к PostgreSQL: {version.split(',')[0]}")
        
        # Получаем список таблиц
        print_section("ТАБЛИЦЫ В БАЗЕ ДАННЫХ")
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if not tables:
            print("❌ Таблицы не найдены")
            return
        
        for table in tables:
            print(f"\n📋 Таблица: {table}")
            columns = inspector.get_columns(table)
            print(f"   Колонки ({len(columns)}):")
            for col in columns:
                col_type = str(col['type'])
                nullable = "NULL" if col['nullable'] else "NOT NULL"
                print(f"     - {col['name']}: {col_type} ({nullable})")
            
            # Показываем количество записей
            with engine.connect() as conn:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.fetchone()[0]
                print(f"   Записей: {count}")
                
                # Показываем данные, если есть
                if count > 0:
                    result = conn.execute(text(f"SELECT * FROM {table} LIMIT 10"))
                    rows = result.fetchall()
                    if rows:
                        print(f"   Первые {min(10, count)} записей:")
                        for i, row in enumerate(rows, 1):
                            # Форматируем вывод
                            row_dict = dict(row._mapping)
                            print(f"     {i}. {row_dict}")
        
        # Показываем детали для каждой таблицы
        print_section("ДЕТАЛЬНЫЙ ПРОСМОТР ДАННЫХ")
        
        for table in tables:
            with engine.connect() as conn:
                result = conn.execute(text(f"SELECT * FROM {table}"))
                rows = result.fetchall()
                
                if rows:
                    print(f"\n📊 Таблица: {table}")
                    print(f"   Всего записей: {len(rows)}")
                    
                    # Получаем названия колонок
                    columns = [col.name for col in result.keys()]
                    print(f"   Колонки: {', '.join(columns)}")
                    
                    print(f"\n   Данные:")
                    for i, row in enumerate(rows, 1):
                        row_dict = dict(row._mapping)
                        print(f"   {i}. {row_dict}")
                else:
                    print(f"\n📊 Таблица: {table} - пуста")
        
    except Exception as e:
        print(f"❌ Ошибка при подключении к БД: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    try:
        view_database()
    except KeyboardInterrupt:
        print("\n\n⚠️  Просмотр прерван пользователем")
    except Exception as e:
        print(f"\n\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()

