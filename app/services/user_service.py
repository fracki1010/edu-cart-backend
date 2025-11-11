from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate
from app.repositories.user_repository import UserRepository


pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"], 
    deprecated="auto"
)

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    
    def get_password_hash(self, password: str):
        # La función debe ser simple, devolviendo el resultado directo de hash.
        return pwd_context.hash(password)
    
    
    def verify_password(self, plain_password, hashed_password) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


    def create_user(self, user_data: UserCreate) -> User:
        # ... (código de hasheo)
        password_hash = self.get_password_hash(user_data.password)

        user = User(
            name=user_data.name,
            username=user_data.username,
            email=user_data.email,
            password=password_hash
        )

        # La función repo.create es la que necesita devolver el objeto
        # Si tu repositorio solo hace el commit y devuelve None, modifícalo:
        created_user = self.repo.create(user) 
        
        # Debe DEVOLVER el usuario que acaba de ser creado e insertado.
        return created_user
    


    def authenticate_user(self, username: str, password: str):
        user = self.repo.get_by_username(username)
        if not user or not self.verify_password(password, user.password):
            return None
        return user

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
