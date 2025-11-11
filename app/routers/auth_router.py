from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserLogin, Token
from app.core.security import create_access_token # <-- Usamos esta función

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    service = UserService(repo)

    existing_user = repo.get_by_username(user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    user = service.create_user(user_data)
    return user


@auth_router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: UserLogin, # <-- Cambio crucial: Acepta JSON body (username y password)
    db: Session = Depends(get_db)
):
    """
    Autentica al usuario usando username y password (enviados como JSON) 
    y devuelve un token JWT.
    """
    repo = UserRepository(db)
    service = UserService(repo)
    
    # 1. Autenticar el usuario
    user = service.authenticate_user(
        username=form_data.username, 
        password=form_data.password
    )
    
    # 2. Si la autenticación falla, lanzar error 401
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 3. Crear el token de acceso
    # Usamos la función IMPORTADA de app.core.auth y el ID para el 'sub'.
    access_token = create_access_token( # <-- CORREGIDO: Usamos la función importada
        data={"sub": str(user.id)} # <-- Mantener ID para consistencia con app/core/auth.py
    )
    
    # 4. Devolver la respuesta de Token
    return {"access_token": access_token, "token_type": "bearer", "name": user.name, "username": user.username, "id": user.id}
