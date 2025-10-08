from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from utv_legal.core.security import get_password_hash
from utv_legal.database import get_session
from utv_legal.models import Usuario
from utv_legal.schemas import Usuario as UsuarioModel, UsuarioList, Message
from utv_legal.schemas.usuario import UsuarioCreate, UsuarioUpdate
from utv_legal.auth.dependencies import get_current_user, require_admin
from utv_legal.models.enums import TipoUsuario as Role

router = APIRouter( tags=["usuarios"])

@router.post('/', status_code=HTTPStatus.CREATED, response_model=UsuarioModel)
async def create_usuario(
    usuario: UsuarioCreate,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(require_admin)
):
    # Verifica se usuário já existe
    db_usuario = session.scalar(
        select(Usuario).where(
            Usuario.email == usuario.email
        )
    )
    
    if db_usuario:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Email já cadastrado"
        )
    hashed_password = get_password_hash(usuario.senha)

    novo_usuario = Usuario(
        email=usuario.email,
        senha=hashed_password,
        tipo_usuario=usuario.tipo_usuario
    )
    
    session.add(novo_usuario)
    session.commit()
    session.refresh(novo_usuario)

    return novo_usuario

@router.get('/', status_code=HTTPStatus.OK, response_model=UsuarioList)
def read_usuarios(
    limit: int = 10,
    offset: int = 0,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(require_admin)
):
    usuarios = session.scalars(select(Usuario).limit(limit).offset(offset))
    return {'usuarios': usuarios}

@router.get(
        '/{usuario_email}',
        status_code=HTTPStatus.OK,
        response_model=UsuarioModel
    )
def get_usuario(usuario_email: str,
                session: Session = Depends(get_session),
                current_user: Depends = Depends(get_current_user)
            ):
    
    # Verifica se o usuário pode acessar estes dados
    if current_user.email != usuario_email and current_user.tipo_usuario != Role.ADMIN:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Você só pode acessar seus próprios dados"
        )
    usuario = session.scalar(
        select(Usuario).where(Usuario.email == usuario_email)
    )

    if not usuario:
        raise HTTPException(
            detail='Usuário não encontrado', status_code=HTTPStatus.NOT_FOUND
        )

    return usuario

@router.put(
        '/{usuario_email}',
        status_code=HTTPStatus.OK,
        response_model=UsuarioModel
    )
def update_usuario(
    usuario_email: str,
    usuario: UsuarioUpdate,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(require_admin)
):
    db_usuario = session.scalar(
        select(Usuario).where(Usuario.email == usuario_email)
    )

    if not db_usuario:
        raise HTTPException(
            detail='Usuário não encontrado', status_code=HTTPStatus.NOT_FOUND
        )
    
    try:
        if usuario.is_active is not None:
            db_usuario.is_active = usuario.is_active
        if usuario.email is not None:
            db_usuario.email = usuario.email
        if usuario.tipo_usuario is not None:
            db_usuario.tipo_usuario = usuario.tipo_usuario
        if usuario.senha is not None:
            hashed_password = get_password_hash(usuario.senha)
            db_usuario.senha = hashed_password
        
        session.add(db_usuario)
        session.commit()
        session.refresh(db_usuario)

        return db_usuario
    
    except Exception as e:
        session.rollback()
        raise HTTPException(
            detail=f'Erro ao atualizar usuário: {str(e)}',
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        )

@router.delete(
    '/{usuario_email}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_usuario(
    usuario_email: str,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(require_admin)
):
    usuario_db = session.scalar(
        select(Usuario).where(Usuario.email == usuario_email)
    )

    if not usuario_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    session.delete(usuario_db)
    session.commit()

    return {'message': 'Usuário deletado com sucesso'}