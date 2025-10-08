from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from utv_legal.auth.dependencies import get_current_user, require_admin, require_fiscal
from utv_legal.database import get_session
from utv_legal.models import Piloto
from utv_legal.models.enums import EstadoCivil, TipoSanguineo
from utv_legal.models.usuario import Usuario
from utv_legal.schemas import Piloto as PilotoSchema, PilotoList, Message
from utv_legal.models.enums import TipoUsuario

router = APIRouter()

@router.post('/', status_code=HTTPStatus.CREATED, response_model=PilotoSchema)
async def create_piloto(
    piloto: PilotoSchema,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(require_admin)
):
    # Verifica se piloto já existe
    db_piloto = session.scalar(
        select(Piloto).where(
            (Piloto.cpf_piloto == piloto.cpf_piloto) |
            (Piloto.email_piloto == piloto.email_piloto)
        )
    )
    
    if db_piloto:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="CPF ou e-mail já cadastrado"
        )

    novo_piloto = Piloto(
        cpf_piloto=piloto.cpf_piloto,
        nome_piloto=piloto.nome_piloto,
        email_piloto=piloto.email_piloto,
        numero_telefone=piloto.numero_telefone,
        estado_civil=EstadoCivil(piloto.estado_civil),
        nome_contato_seguranca=piloto.nome_contato_seguranca,
        numero_contato_seguranca=piloto.numero_contato_seguranca,
        tipo_sanguineo=TipoSanguineo(piloto.tipo_sanguineo),
        nome_plano_saude=piloto.nome_plano_saude,
        foto_piloto=piloto.foto_piloto,
        foto_piloto_tipo=piloto.foto_piloto_tipo,
        foto_cnh=piloto.foto_cnh,
        foto_cnh_tipo=piloto.foto_cnh_tipo,
        termo_adesao=piloto.termo_adesao,
        termo_adesao_tipo=piloto.termo_adesao_tipo,
        data_nascimento=piloto.data_nascimento,
        id_piloto=piloto.id_piloto
    )

    session.add(novo_piloto)
    session.commit()
    session.refresh(novo_piloto)

    return novo_piloto

@router.get('/', status_code=HTTPStatus.OK, response_model=PilotoList)
def read_pilotos(
    limit: int = 10,
    offset: int = 0,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(require_fiscal)
):
    pilotos = session.scalars(select(Piloto).limit(limit).offset(offset))
    return {'pilotos': pilotos}

@router.get('/{cpf_piloto}', status_code=HTTPStatus.OK, response_model=PilotoSchema)
def get_piloto(
    cpf_piloto: str,
    session: Session = Depends(get_session),
    current_user: Depends = Depends(get_current_user)
    ):
    piloto = session.scalar(select(Piloto).where(Piloto.cpf_piloto == cpf_piloto))

    if not piloto:
        raise HTTPException(
            detail='Piloto not found', status_code=HTTPStatus.NOT_FOUND
        )
    if piloto.email_piloto != current_user.email and current_user.tipo_usuario != TipoUsuario.ADMIN:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Você só pode acessar seus próprios dados"
        )

    return piloto


@router.get('/email/{email_piloto}', status_code=HTTPStatus.OK, response_model=PilotoSchema)
def get_piloto(
    email_piloto: str,
    session: Session = Depends(get_session)
    ):
    piloto = session.scalar(select(Piloto).where(Piloto.email_piloto == email_piloto))

    if not piloto:
        raise HTTPException(
            detail='Piloto not found', status_code=HTTPStatus.NOT_FOUND
        )

    return piloto

# TODO : Criar schema para esse retorno
@router.get('/fiscalizar/{id_piloto}', status_code=HTTPStatus.OK, response_model=PilotoSchema)
def get_piloto_by_id(
    id_piloto: str,
    session: Session = Depends(get_session),
    current_user: Depends = Depends(require_fiscal)
    ):
    piloto = session.scalar(select(Piloto).where(Piloto.id_piloto == id_piloto))

    if not piloto:
        raise HTTPException(
            detail='Piloto not found', status_code=HTTPStatus.NOT_FOUND
        )

    return piloto

@router.put('/{cpf_piloto}', status_code=HTTPStatus.OK, response_model=PilotoSchema)
def update_piloto(
    cpf_piloto: str,
    piloto: PilotoSchema,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(require_admin)
):
    db_piloto = session.scalar(select(Piloto).where(Piloto.cpf_piloto == cpf_piloto))

    if not db_piloto:
        raise HTTPException(
            detail='Piloto not found', status_code=HTTPStatus.NOT_FOUND
        )
    
    try:
        if piloto.nome_piloto is not None:
            db_piloto.nome_piloto = piloto.nome_piloto
        if piloto.email_piloto is not None:
            db_piloto.email_piloto = piloto.email_piloto
        # ... (restante das atualizações)
        
        session.add(db_piloto)
        session.commit()
        session.refresh(db_piloto)

        return db_piloto
    
    except Exception as e:
        session.rollback()
        raise HTTPException(
            detail=f'Error updating piloto: {str(e)}',
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        )

@router.delete('/{cpf_piloto}', status_code=HTTPStatus.OK, response_model=Message)
def delete_piloto(
    cpf_piloto: str,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(require_admin)
    ):
    piloto_db = session.scalar(select(Piloto).where(Piloto.cpf_piloto == cpf_piloto))

    if not piloto_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    session.delete(piloto_db)
    session.commit()

    return {'message': 'Piloto deleted successfully'}