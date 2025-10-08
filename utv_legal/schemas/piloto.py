from datetime import datetime
from typing import Optional
from pydantic import EmailStr

from .base import ModelBase
from utv_legal.models.enums import EstadoCivil, TipoSanguineo

class PublicPilot(ModelBase):
    nome_piloto: str
    email_piloto: EmailStr
    numero_telefone: str
    tipo_sanguineo: TipoSanguineo
    nome_plano_saude: str
    estado_civil: EstadoCivil
    nome_contato_seguranca: str
    numero_contato_seguranca: str
    id_piloto: Optional[str] = None
    data_nascimento: Optional[datetime] = None
    foto_piloto: Optional[bytes] = None
    foto_piloto_tipo: Optional[str] = None
    termo_adesao: Optional[bytes] = None
    termo_adesao_tipo: Optional[str] = None

    class Config:
        from_attributes = True

class Piloto(PublicPilot):
    cpf_piloto: str
    foto_cnh: Optional[bytes] = None
    foto_cnh_tipo: Optional[str] = None

class PilotoList(ModelBase):
    pilotos: list[Piloto]

    class Config:
        from_attributes = True