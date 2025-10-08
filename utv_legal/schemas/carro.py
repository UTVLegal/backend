from typing import Optional
from .base import ModelBase

class CarroBase(ModelBase):
    foto_frente: bytes
    foto_tras: bytes
    foto_esquerda: bytes
    foto_direita: bytes
    nota_fiscal: bytes

class CarroCreate(CarroBase):
    pass

class CarroPublic(CarroBase):
    id: int
    cpf_piloto: str

class CarroUpdate(ModelBase):
    foto_frente: Optional[bytes] = None
    foto_tras: Optional[bytes] = None
    foto_esquerda: Optional[bytes] = None
    foto_direita: Optional[bytes] = None
    nota_fiscal: Optional[bytes] = None