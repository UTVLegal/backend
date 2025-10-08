from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from utv_legal.database import get_session
from utv_legal.models import Usuario
from utv_legal.core.security import verify_token
from utv_legal.models.enums import TipoUsuario as Role

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = verify_token(token)
        if payload is None:
            raise credentials_exception
            
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
        # Converta para inteiro já que o ID é numérico
        user_id_int = int(user_id)
        
    except (JWTError, ValueError):
        raise credentials_exception
        
    user = session.get(Usuario, user_id_int)
    if user is None:
        raise credentials_exception
    return user

def require_role(required_role: Role):
    def role_checker(current_user: Usuario = Depends(get_current_user)):
        if current_user.tipo_usuario not in [required_role, Role.ADMIN]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permissão insuficiente"
            )
        return current_user
    return role_checker

# Dependência específica para ADMIN
def require_admin(current_user: Usuario = Depends(get_current_user)):
    if current_user.tipo_usuario != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores"
        )
    return current_user

# Dependência específica para FISCAL ou superior
def require_fiscal(current_user: Usuario = Depends(get_current_user)):
    if current_user.tipo_usuario not in [Role.FISCAL, Role.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a fiscais e administradores"
        )
    return current_user

# Dependência para usuário acessar apenas seus próprios dados
def require_self_or_admin(user_id: int, current_user: Usuario = Depends(get_current_user)):
    if current_user.id != user_id and current_user.tipo_usuario != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você só pode acessar seus próprios dados"
        )
    return current_user