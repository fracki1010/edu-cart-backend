from pydantic import BaseModel, EmailStr, validator, Field
from sqlmodel import SQLModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    name: str
    email: str
    password: str

    @validator("password")
    def password_not_hashed(cls, v):
        if v.startswith("$2b$") or v.startswith("$2a$"):
            raise ValueError("La contraseña no debe estar cifrada.")
        return v

class UserRead(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str


class Token(SQLModel):
    """Esquema de salida para el token JWT."""
    access_token: str
    token_type: str = "bearer"
    name: str = Field(..., description="El nombre del usuario autenticado")
    username: str = Field(..., description="El username del usuario autenticado")
    id: int = Field(..., description="El id del usuario autenticado")
    
    # 5. ESQUEMA DE DATOS DEL TOKEN (PAYLOAD): Usado en app/core/auth.py
# Este modelo solo existe en memoria y define lo que hay dentro del JWT.
class TokenData(SQLModel):
    id: Optional[int] = None