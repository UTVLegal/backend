from .base import table_registry
from .enums import (
    EstadoCivil, 
    TipoSanguineo, 
    TipoEndereco, 
    EstadosBrasileiros, 
    TipoUsuario
)
from .piloto import Piloto
from .endereco import Endereco
from .carro import Carro
from .usuario import Usuario

__all__ = [
    'table_registry',
    'EstadoCivil',
    'TipoSanguineo',
    'TipoEndereco',
    'EstadosBrasileiros',
    'TipoUsuario',
    'Piloto',
    'Endereco',
    'Carro',
    'Usuario'
]