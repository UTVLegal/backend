# utv_legal/core/admin_setup.py
from sqlalchemy import select
from sqlalchemy.orm import Session

from utv_legal.database import get_session
from utv_legal.models import Usuario
from utv_legal.models.enums import TipoUsuario as Role
from utv_legal.core.security import get_password_hash

async def create_default_admin():
    """
    Cria um usuário admin padrão se não existir nenhum admin no sistema
    """
    session: Session = next(get_session())
    
    try:
        # Verifica se existe algum admin no sistema
        admin_exists = session.scalar(
            select(Usuario).where(Usuario.tipo_usuario == Role.ADMIN)
        )
        
        if not admin_exists:
            # Verifica se o admin padrão já existe
            default_admin = session.scalar(
                select(Usuario).where(Usuario.email == "admin@admin.com")
            )
            
            if not default_admin:
                # Cria o admin padrão
                hashed_password = get_password_hash("admin")
                
                novo_admin = Usuario(
                    email="admin@admin.com",
                    senha=hashed_password,
                    tipo_usuario=Role.ADMIN,
                    is_active=True
                )
                
                session.add(novo_admin)
                session.commit()
                print("✅ Usuário admin padrão criado: admin@admin.com / admin")
            else:
                print("ℹ️  Usuário admin padrão já existe")
        else:
            print("ℹ️  Já existem administradores no sistema")
            
    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao criar admin padrão: {str(e)}")
    finally:
        session.close()