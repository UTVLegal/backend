from typing import Optional
from sqlalchemy import LargeBinary, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import table_registry


@table_registry.mapped_as_dataclass
class Carro:
    __tablename__ = 'carro'

    id: Mapped[Optional[int]] = mapped_column(primary_key=True, autoincrement=True, init=False)
    cpf_piloto: Mapped[str] = mapped_column(
        String(11),
        ForeignKey('piloto.cpf_piloto'),
        nullable=False
    )
    foto_frente: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    foto_tras: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    foto_esquerda: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    foto_direita: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    nota_fiscal: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)