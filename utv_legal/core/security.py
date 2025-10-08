from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional

from pytest import Session
from sqlalchemy import select

from utv_legal.core.settings import Settings
from utv_legal.models.usuario import Usuario

# Configurações
SECRET_KEY = Settings().SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Função específica para criar token de usuário
def create_user_token(user_id: int, email: str, role: str):
    return create_access_token(
        data={"sub": str(user_id), "email": email, "role": role}
    )

def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
    
def authenticate_user(session: Session, email: str, password: str) -> Optional[Usuario]:
    """
    Autentica um usuário pelo email e senha
    """
    user = session.scalar(select(Usuario).where(Usuario.email == email))
    if not user:
        return None
    
    if not verify_password(password, user.senha):
        return None
    
    return user