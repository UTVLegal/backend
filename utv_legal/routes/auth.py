from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import timedelta

from utv_legal.database import get_session
from utv_legal.dependencies.auth import get_current_active_user
from utv_legal.models.usuario import Usuario
from utv_legal.schemas.usuario import UsuarioCreate, Usuario as UsuarioModel, Token, UsuarioLogin
from utv_legal.core.security import (
    authenticate_user, create_user_token, verify_password, get_password_hash, create_access_token
)

router = APIRouter(tags=["auth"])

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Use a nova função que cria token com ID como subject
    access_token = create_user_token(user.id, user.email, user.tipo_usuario.value)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.email,
        "tipo": user.tipo_usuario.value
    }

@router.get("/me", response_model=Usuario)
async def read_users_me(current_user: Usuario = Depends(get_current_active_user)):
    return current_user