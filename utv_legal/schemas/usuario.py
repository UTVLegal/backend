from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from utv_legal.models.usuario import TipoUsuario

class UsuarioBase(BaseModel):
    email: EmailStr
    tipo_usuario: Optional[TipoUsuario] = TipoUsuario.USER
    is_active: Optional[bool] = True

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr] = None
    tipo_usuario: Optional[TipoUsuario] = None
    is_active: Optional[bool] = None
    senha: Optional[str] = None

class Usuario(UsuarioBase):
    id: Optional[int]

    class Config:
        from_attributes = True

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

class UsuarioList(BaseModel):
    usuarios: list[Usuario]

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
    user_id: int
    tipo: TipoUsuario

class TokenData(BaseModel):
    email: Optional[str] = None