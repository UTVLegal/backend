from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import Enum, String, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column

from utv_legal.models.enums import TipoUsuario
from .base import table_registry


@table_registry.mapped_as_dataclass
class Usuario:
    __tablename__ = 'usuario'
    
    id: Mapped[Optional[int]] = mapped_column(
        primary_key=True, autoincrement=True, init=False
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    senha: Mapped[str] = mapped_column(String(255), nullable=False)
    tipo_usuario: Mapped[TipoUsuario] = mapped_column(Enum(TipoUsuario), default=TipoUsuario.USER)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] =mapped_column(
        init=False, server_default=func.now()
    )