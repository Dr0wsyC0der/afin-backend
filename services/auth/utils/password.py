# services/auth/utils/password.py
import bcrypt

def _normalize_password(password) -> bytes:
    """Нормализует пароль: конвертирует в bytes и обрезает до 72 байт"""
    # Убеждаемся, что это строка
    if isinstance(password, bytes):
        password_str = password.decode('utf-8', errors='ignore')
    elif not isinstance(password, str):
        password_str = str(password)
    else:
        password_str = password
    
    # Bcrypt ограничение: 72 байта максимум
    # Конвертируем в bytes и обрезаем до 72 байт
    password_bytes = password_str.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    return password_bytes

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет пароль"""
    try:
        # Нормализуем пароль в bytes
        password_bytes = _normalize_password(plain_password)
        
        # Конвертируем хеш в bytes, если нужно
        if isinstance(hashed_password, str):
            hashed_bytes = hashed_password.encode('utf-8')
        else:
            hashed_bytes = hashed_password
        
        # Проверяем пароль
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception as e:
        # Логируем ошибку, но не раскрываем детали
        print(f"Password verification error: {e}")
        return False

def get_password_hash(password: str) -> str:
    """Хеширует пароль используя bcrypt напрямую"""
    try:
        # Нормализуем пароль в bytes
        password_bytes = _normalize_password(password)
        
        # Убеждаемся, что пароль не пустой
        if not password_bytes:
            raise ValueError("Password cannot be empty")
        
        # Генерируем соль и хешируем
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password_bytes, salt)
        
        # Возвращаем как строку
        return hashed.decode('utf-8')
    except ValueError:
        raise
    except Exception as e:
        # Более информативная ошибка
        password_info = f"type: {type(password)}, length: {len(str(password))}"
        if isinstance(password, str):
            password_bytes = password.encode('utf-8')
            password_info += f", bytes: {len(password_bytes)}"
        raise ValueError(f"Password hashing failed: {str(e)}. {password_info}")
