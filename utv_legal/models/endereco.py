from datetime import datetime
from typing import Optional
from sqlalchemy import func, Enum as SQLEnum, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import table_registry
from .enums import TipoEndereco, EstadosBrasileiros


@table_registry.mapped_as_dataclass
class Endereco:
    __tablename__ = 'endereco'

    id: Mapped[Optional[int]] = mapped_column(primary_key=True, autoincrement=True, init=False)
    cpf_piloto: Mapped[str] = mapped_column(
        String(11),
        ForeignKey('piloto.cpf_piloto'),
        nullable=False
    )
    tipo_endereco: Mapped[TipoEndereco] = mapped_column(SQLEnum(TipoEndereco))
    cep: Mapped[str] = mapped_column(String(10), nullable=False)
    logradouro: Mapped[str] = mapped_column(String(100), nullable=False)
    numero: Mapped[Optional[int]] = mapped_column(nullable=True)
    complemento: Mapped[Optional[str]] = mapped_column()
    bairro: Mapped[str] = mapped_column(String(50), nullable=False)
    cidade: Mapped[str] = mapped_column(String(50))
    uf: Mapped[EstadosBrasileiros] = mapped_column(SQLEnum(EstadosBrasileiros))
    pais: Mapped[str] = mapped_column(String(30), default='Brasil')
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )