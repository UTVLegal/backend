from enum import Enum

class EstadosBrasileiros(Enum):
    AC = "Acre"
    AL = "Alagoas"
    AP = "Amapá"
    AM = "Amazonas"
    BA = "Bahia"
    CE = "Ceará"
    DF = "Distrito Federal"
    ES = "Espírito Santo"
    GO = "Goiás"
    MA = "Maranhão"
    MT = "Mato Grosso"
    MS = "Mato Grosso do Sul"
    MG = "Minas Gerais"
    PA = "Pará"
    PB = "Paraíba"
    PR = "Paraná"
    PE = "Pernambuco"
    PI = "Piauí"
    RJ = "Rio de Janeiro"
    RN = "Rio Grande do Norte"
    RS = "Rio Grande do Sul"
    RO = "Rondônia"
    RR = "Roraima"
    SC = "Santa Catarina"
    SP = "São Paulo"
    SE = "Sergipe"
    TO = "Tocantins"

class TipoUsuario(Enum):
    ADMIN = "ADMIN"
    FISCAL = "FISCAL"
    USER = "USER"

class EstadoCivil(Enum):
    SOLTEIRO = 1
    CASADO = 2
    VIUVO = 3
    OUTROS = 4

class TipoSanguineo(Enum):
    A_POSITIVO = 1
    A_NEGATIVO = 2
    B_POSITIVO = 3
    B_NEGATIVO = 4
    AB_POSITIVO = 5
    AB_NEGATIVO = 6
    O_POSITIVO = 7
    O_NEGATIVO = 8

class TipoEndereco(Enum):
    RESIDENCIAL = 'RESIDENCIAL'
    COMERCIAL = 'COMERCIAL'
    OUTROS = 'OUTROS'