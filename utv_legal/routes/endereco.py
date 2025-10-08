from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from utv_legal.database import get_session
from utv_legal.models import Piloto, Endereco
from utv_legal.models.enums import EstadosBrasileiros
from utv_legal.schemas import CreateEndereco, EnderecoPublico, Message

router = APIRouter()

@router.post('/{cpf}', status_code=HTTPStatus.CREATED, response_model=EnderecoPublico)
def create_endereco(
    cpf: str,
    endereco: CreateEndereco,
    session: Session = Depends(get_session)
):
    piloto = session.scalar(select(Piloto).where(Piloto.cpf_piloto == cpf))

    if not piloto:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    
    endereco_db = session.scalar(select(Endereco).where(Endereco.cpf_piloto == cpf))

    if endereco_db:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Piloto com endereço já cadastrado"
        )
    
    novo_endereco = Endereco(
        cpf_piloto=piloto.cpf_piloto,
        tipo_endereco=endereco.tipo_endereco,
        logradouro=endereco.logradouro,
        numero=endereco.numero,
        complemento=endereco.complemento,
        cep=endereco.cep,
        bairro=endereco.bairro,
        cidade=endereco.cidade,
        uf=EstadosBrasileiros(endereco.uf),
        pais=endereco.pais
    )

    session.add(novo_endereco)
    session.commit()
    session.refresh(novo_endereco)

    return novo_endereco

@router.get('/{cpf_piloto}', status_code=HTTPStatus.OK, response_model=EnderecoPublico)
def get_endereco(cpf_piloto: str, session: Session = Depends(get_session)):
    endereco = session.scalar(select(Endereco).where(Endereco.cpf_piloto == cpf_piloto))

    if not endereco:
        raise HTTPException(
            detail='Endereço não encontrado', status_code=HTTPStatus.NOT_FOUND
        )

    return endereco

@router.put('/{cpf_piloto}', status_code=HTTPStatus.OK, response_model=EnderecoPublico)
def update_endereco(
    cpf_piloto: str,
    endereco: EnderecoPublico,
    session: Session = Depends(get_session)
):
    endereco_db = session.scalar(select(Endereco).where(Endereco.cpf_piloto == cpf_piloto))
    
    if not endereco_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Endereco not found'
        )
    
    # ... (restante do código de update)
    
    return endereco_db

@router.delete('/{cpf_piloto}', status_code=HTTPStatus.OK, response_model=Message)
def delete_endereco(cpf_piloto: str, session: Session = Depends(get_session)):
    endereco_db = session.scalar(select(Endereco).where(Endereco.cpf_piloto == cpf_piloto))

    if not endereco_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Endereco not found'
        )

    session.delete(endereco_db)
    session.commit()

    return {'message': 'Endereco deleted successfully'}