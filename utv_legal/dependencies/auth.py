from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from typing import Optional

from utv_legal.database import get_session
from utv_legal.models.usuario import Usuario
from utv_legal.core.security import verify_token
from utv_legal.schemas.usuario import TokenData

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
    
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    token_data = TokenData(email=email)
    
    user = session.query(Usuario).filter(Usuario.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User inactive"
        )
    
    return user

async def get_current_active_user(current_user: Usuario = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User inactive"
        )
    return current_user

async def get_current_admin_user(current_user: Usuario = Depends(get_current_user)):
    if current_user.tipo_usuario != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user

async def get_current_fiscal_user(current_user: Usuario = Depends(get_current_user)):
    if current_user.tipo_usuario not in ["ADMIN", "FISCAL"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Fiscal or Admin privileges required"
        )
    return current_user