# services/auth/schemas.py
from pydantic import BaseModel, EmailStr, field_validator

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Валидация пароля: убеждаемся, что это строка и не превышает 72 байта"""
        if not isinstance(v, str):
            v = str(v)
        # Bcrypt ограничение: 72 байта максимум
        password_bytes = v.encode('utf-8')
        if len(password_bytes) > 72:
            # Обрезаем до 72 байт
            v = password_bytes[:72].decode('utf-8', errors='ignore')
        if len(v) == 0:
            raise ValueError("Password cannot be empty")
        return v

class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"