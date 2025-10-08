from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from utv_legal.database import get_session
from utv_legal.models import Piloto, Carro
from utv_legal.schemas import CarroCreate, CarroPublic, CarroUpdate, Message

router = APIRouter()

@router.post('/{cpf}', status_code=HTTPStatus.CREATED, response_model=CarroPublic)
def create_carro(
    cpf: str,
    carro: CarroCreate,
    session: Session = Depends(get_session)
):
    db_piloto = session.scalar(select(Piloto).where(Piloto.cpf_piloto == cpf))

    if not db_piloto:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    
    db_carro = session.scalar(select(Carro).where(Carro.cpf_piloto == cpf))

    if db_carro:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Piloto com carro já cadastrado"
        )
    
    novo_carro = Carro(
        cpf_piloto=db_piloto.cpf_piloto,
        foto_frente=carro.foto_frente,
        foto_tras=carro.foto_tras,
        foto_esquerda=carro.foto_esquerda,
        foto_direita=carro.foto_direita,
        nota_fiscal=carro.nota_fiscal
    )

    session.add(novo_carro)
    session.commit()
    session.refresh(novo_carro)

    return novo_carro

@router.get('/{cpf}', status_code=HTTPStatus.OK, response_model=CarroPublic)
async def read_carro(cpf: str, session: Session = Depends(get_session)):
    db_piloto = session.scalar(select(Piloto).where(Piloto.cpf_piloto == cpf))
    
    if not db_piloto:
        raise HTTPException(
            detail='Piloto não encontrado', status_code=HTTPStatus.NOT_FOUND
        )
    
    carro = session.scalar(select(Carro).where(Carro.cpf_piloto == cpf))

    if not carro:
        raise HTTPException(
            detail='Carro não encontrado', status_code=HTTPStatus.NOT_FOUND
        )

    return carro

@router.put('/{cpf}', status_code=HTTPStatus.OK, response_model=Message)
def update_carro(
    cpf: str,
    carro: CarroUpdate,
    session: Session = Depends(get_session)
):
    db_carro = session.scalar(select(Carro).where(Carro.cpf_piloto == cpf))

    if not db_carro:
        raise HTTPException(
            detail='Carro não encontrado', status_code=HTTPStatus.NOT_FOUND
        )
    
    # ... (restante do código de update)
    
    return {'message': f'Carro Id:{db_carro.id} atualizado'}

@router.delete('/{cpf}', status_code=HTTPStatus.OK, response_model=Message)
def delete_carro(cpf: str, session: Session = Depends(get_session)):
    db_carro = session.scalar(select(Carro).where(Carro.cpf_piloto == cpf))

    if not db_carro:
        raise HTTPException(
            detail='Carro não encontrado', status_code=HTTPStatus.NOT_FOUND
        )
    
    session.delete(db_carro)
    session.commit()

    return {'message': 'Carro deleted successfully'}