from datetime import datetime
from typing import Optional
from sqlalchemy import func, Enum, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from .base import table_registry
from utv_legal.models.enums import EstadoCivil, TipoSanguineo


@table_registry.mapped_as_dataclass
class Piloto:
    __tablename__ = 'piloto'
    cpf_piloto: Mapped[str] = mapped_column(primary_key=True)
    nome_piloto: Mapped[str]
    email_piloto: Mapped[str] = mapped_column(unique=True)
    numero_telefone: Mapped[str] = mapped_column(unique=True)
    estado_civil: Mapped[EstadoCivil] = mapped_column(Enum(EstadoCivil))
    nome_contato_seguranca: Mapped[str]
    numero_contato_seguranca: Mapped[str]
    tipo_sanguineo: Mapped[TipoSanguineo] = mapped_column(
        Enum(TipoSanguineo)
    )
    nome_plano_saude: Mapped[str]
    foto_cnh: Mapped[Optional[bytes]] = mapped_column(LargeBinary, nullable=True)
    foto_cnh_tipo: Mapped[Optional[str]] = mapped_column(nullable=True)
    foto_piloto: Mapped[Optional[bytes]] = mapped_column(LargeBinary, nullable=True)
    foto_piloto_tipo: Mapped[Optional[str]] = mapped_column(nullable=True)
    termo_adesao: Mapped[Optional[bytes]] = mapped_column(LargeBinary, nullable=True)
    termo_adesao_tipo: Mapped[Optional[str]] = mapped_column(nullable=True)
    id_piloto: Mapped[Optional[str]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    data_nascimento: Mapped[datetime]