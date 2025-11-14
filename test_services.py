#!/usr/bin/env python3
"""
Скрипт для проверки работы всех сервисов AFIN Backend
"""
import requests
import time
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def print_section(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def test_gateway_health() -> bool:
    """Проверка здоровья Gateway и всех сервисов"""
    print_section("1. Проверка Gateway и всех сервисов")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Gateway: {data.get('gateway')}")
            print("\nСтатус сервисов:")
            for service, status in data.get('services', {}).items():
                status_icon = "✅" if status.get('status') == 'ok' else "❌"
                print(f"  {status_icon} {service}: {status}")
            return all(s.get('status') == 'ok' for s in data.get('services', {}).values())
        else:
            print(f"❌ Gateway вернул код {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка при проверке Gateway: {e}")
        return False

def test_auth_service() -> Dict[str, Any]:
    """Тестирование сервиса Auth"""
    print_section("2. Тестирование Auth Service")
    result = {"success": False, "token": None, "user_id": None}
    
    # Проверка здоровья
    try:
        response = requests.get(f"{BASE_URL}/api/v1/auth/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ Auth health: {response.json()}")
        else:
            print(f"❌ Auth health вернул код {response.status_code}")
            return result
    except Exception as e:
        print(f"❌ Ошибка при проверке Auth health: {e}")
        return result
    
    # Регистрация
    test_email = f"test_{int(time.time())}@example.com"
    test_password = "test123456"
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/register",
            json={"email": test_email, "password": test_password},
            timeout=5
        )
        print(f"   Статус код: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('content-type', 'unknown')}")
        
        if response.status_code == 200:
            try:
                user_data = response.json()
                print(f"✅ Регистрация успешна: {user_data['email']} (ID: {user_data['id']})")
                result["user_id"] = user_data['id']
            except ValueError as e:
                print(f"❌ Ошибка парсинга JSON ответа: {e}")
                print(f"   Ответ сервера: {response.text[:200]}")
                return result
        elif response.status_code == 400:
            try:
                error_data = response.json()
                print(f"⚠️  Ошибка регистрации: {error_data}")
                print(f"   Пробуем войти...")
            except ValueError:
                print(f"⚠️  Пользователь уже существует или ошибка (код 400)")
                print(f"   Ответ: {response.text[:200]}")
        else:
            print(f"❌ Регистрация вернула код {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Ошибка: {error_data}")
            except ValueError:
                print(f"   Ответ: {response.text[:200]}")
            return result
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при регистрации (сетевая ошибка): {e}")
        return result
    except Exception as e:
        print(f"❌ Ошибка при регистрации: {e}")
        import traceback
        traceback.print_exc()
        return result
    
    # Вход
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/login",
            data={"username": test_email, "password": test_password},
            timeout=5
        )
        if response.status_code == 200:
            token_data = response.json()
            result["token"] = token_data["access_token"]
            print(f"✅ Вход успешен, получен токен")
            result["success"] = True
        else:
            print(f"❌ Вход вернул код {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка при входе: {e}")
    
    return result

def test_models_service() -> Dict[str, Any]:
    """Тестирование сервиса Models"""
    print_section("3. Тестирование Models Service")
    result = {"success": False, "model_id": None}
    
    # Проверка здоровья
    try:
        response = requests.get(f"{BASE_URL}/api/v1/models/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ Models health: {response.json()}")
        else:
            print(f"❌ Models health вернул код {response.status_code}")
            return result
    except Exception as e:
        print(f"❌ Ошибка при проверке Models health: {e}")
        return result
    
    # Создание модели
    test_model = {
        "name": f"Test Model {int(time.time())}",
        "data": {
            "process_id": "test_proc_1",
            "elements": [
                {"type": "task", "id": "task1", "name": "Task 1"},
                {"type": "task", "id": "task2", "name": "Task 2"}
            ]
        },
        "user_id": 1
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/models/",
            json=test_model,
            timeout=5
        )
        if response.status_code == 200:
            model_data = response.json()
            result["model_id"] = model_data["id"]
            print(f"✅ Модель создана: {model_data['name']} (ID: {model_data['id']})")
            result["success"] = True
        else:
            print(f"❌ Создание модели вернуло код {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка при создании модели: {e}")
    
    # Получение списка моделей
    if result["model_id"]:
        try:
            response = requests.get(f"{BASE_URL}/api/v1/models/", timeout=5)
            if response.status_code == 200:
                models = response.json()
                print(f"✅ Получен список моделей: {len(models)} шт.")
        except Exception as e:
            print(f"⚠️  Ошибка при получении списка моделей: {e}")
    
    return result

def test_simulation_service(model_id: int = None) -> Dict[str, Any]:
    """Тестирование сервиса Simulation"""
    print_section("4. Тестирование Simulation Service")
    result = {"success": False, "simulation_id": None}
    
    # Проверка здоровья
    try:
        response = requests.get(f"{BASE_URL}/api/v1/simulation/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ Simulation health: {response.json()}")
        else:
            print(f"❌ Simulation health вернул код {response.status_code}")
            return result
    except Exception as e:
        print(f"❌ Ошибка при проверке Simulation health: {e}")
        return result
    
    # Запуск симуляции
    if not model_id:
        model_id = 1  # Используем модель по умолчанию
    
    simulation_request = {
        "model_id": model_id,
        "model_data": {
            "elements": [
                {"type": "task", "id": "task1", "name": "Task 1", "duration": 1.0},
                {"type": "task", "id": "task2", "name": "Task 2", "duration": 0.5}
            ]
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/simulation/",
            json=simulation_request,
            timeout=5
        )
        if response.status_code == 200:
            sim_data = response.json()
            result["simulation_id"] = sim_data["id"]
            print(f"✅ Симуляция запущена: ID {sim_data['id']}, статус: {sim_data['status']}")
            result["success"] = True
            
            # Ждем немного и проверяем результат
            print("⏳ Ожидание завершения симуляции...")
            time.sleep(2)
            
            try:
                response = requests.get(
                    f"{BASE_URL}/api/v1/simulation/{result['simulation_id']}",
                    timeout=5
                )
                if response.status_code == 200:
                    sim_result = response.json()
                    print(f"✅ Результат симуляции: статус={sim_result.get('status')}, "
                          f"длительность={sim_result.get('duration')}")
                    if sim_result.get('results'):
                        print(f"   Результаты: {json.dumps(sim_result['results'], indent=2)}")
            except Exception as e:
                print(f"⚠️  Ошибка при получении результата: {e}")
        else:
            print(f"❌ Запуск симуляции вернул код {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка при запуске симуляции: {e}")
    
    return result

def test_analytics_service() -> bool:
    """Тестирование сервиса Analytics"""
    print_section("5. Тестирование Analytics Service")
    
    # Проверка здоровья
    try:
        response = requests.get(f"{BASE_URL}/api/v1/analytics/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ Analytics health: {response.json()}")
        else:
            print(f"❌ Analytics health вернул код {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка при проверке Analytics health: {e}")
        return False
    
    # Базовый эндпоинт
    try:
        response = requests.get(f"{BASE_URL}/api/v1/analytics/", timeout=5)
        if response.status_code == 200:
            print(f"✅ Analytics root: {response.json()}")
            return True
        else:
            print(f"❌ Analytics root вернул код {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка при проверке Analytics root: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("  ТЕСТИРОВАНИЕ СЕРВИСОВ AFIN BACKEND")
    print("="*60)
    
    results = {
        "gateway": False,
        "auth": False,
        "models": False,
        "simulation": False,
        "analytics": False
    }
    
    # 1. Проверка Gateway
    results["gateway"] = test_gateway_health()
    
    if not results["gateway"]:
        print("\n❌ Gateway не работает, дальнейшие тесты невозможны")
        return
    
    # 2. Тестирование Auth
    auth_result = test_auth_service()
    results["auth"] = auth_result["success"]
    
    # 3. Тестирование Models
    models_result = test_models_service()
    results["models"] = models_result["success"]
    
    # 4. Тестирование Simulation
    simulation_result = test_simulation_service(models_result.get("model_id"))
    results["simulation"] = simulation_result["success"]
    
    # 5. Тестирование Analytics
    results["analytics"] = test_analytics_service()
    
    # Итоги
    print_section("ИТОГИ ТЕСТИРОВАНИЯ")
    for service, success in results.items():
        status = "✅ РАБОТАЕТ" if success else "❌ НЕ РАБОТАЕТ"
        print(f"  {service.upper():15} {status}")
    
    all_ok = all(results.values())
    print(f"\n{'✅ ВСЕ СЕРВИСЫ РАБОТАЮТ' if all_ok else '❌ НЕКОТОРЫЕ СЕРВИСЫ НЕ РАБОТАЮТ'}")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Тестирование прервано пользователем")
    except Exception as e:
        print(f"\n\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()

