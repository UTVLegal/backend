from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional
from utv_legal.models.usuario import TipoUsuario

class UsuarioBase(BaseModel):
    email: str  # ⭐ MODIFICADO: De EmailStr para str
    tipo_usuario: Optional[TipoUsuario] = TipoUsuario.USER
    is_active: Optional[bool] = True

    @field_validator('email')
    @classmethod
    def validate_email_based_on_user_type(cls, v, info):
        if 'tipo_usuario' in info.data and info.data['tipo_usuario'] != TipoUsuario.FISCAL:
            # Para ADMIN e USER, validar como email
            try:
                # Tenta validar como email
                from pydantic import EmailStr
                return str(EmailStr.validate(v))
            except ValueError:
                raise ValueError('Email inválido')
        # Para FISCAL, aceita qualquer string
        return v

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioUpdate(BaseModel):
    email: Optional[str] = None  # ⭐ MODIFICADO: De EmailStr para str
    tipo_usuario: Optional[TipoUsuario] = None
    is_active: Optional[bool] = None
    senha: Optional[str] = None

    @field_validator('email')
    @classmethod
    def validate_email_based_on_user_type(cls, v, info):
        if v is not None:
            if 'tipo_usuario' in info.data and info.data['tipo_usuario'] != TipoUsuario.FISCAL:
                # Para ADMIN e USER, validar como email
                try:
                    from pydantic import EmailStr
                    return str(EmailStr.validate(v))
                except ValueError:
                    raise ValueError('Email inválido')
        return v

class Usuario(UsuarioBase):
    id: Optional[int]

    class Config:
        from_attributes = True

class UsuarioLogin(BaseModel):
    email: str  # ⭐ MODIFICADO: De EmailStr para str
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