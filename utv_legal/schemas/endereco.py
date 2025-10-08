from typing import Optional
from .base import ModelBase
from utv_legal.models.enums import TipoEndereco, EstadosBrasileiros

class EnderecoPublico(ModelBase):
    tipo_endereco: TipoEndereco
    cep: str
    logradouro: str
    numero: Optional[int] = None
    complemento: Optional[str] = None
    bairro: str
    cidade: str
    uf: EstadosBrasileiros
    pais: str = 'Brasil'

class CreateEndereco(EnderecoPublico):
    cpf_piloto: str

class Endereco(CreateEndereco):
    id: int