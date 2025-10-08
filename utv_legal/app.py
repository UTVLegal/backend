from http import HTTPStatus
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from utv_legal.routes import auth, piloto, endereco, carro, usuario
from utv_legal.auth.dependencies import get_current_user, require_role

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Incluir as rotas
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(usuario.router, prefix="/usuarios", tags=["usuarios"])
app.include_router(piloto.router, prefix="/pilotos", tags=["pilotos"])
app.include_router(endereco.router, prefix="/endereco", tags=["endereco"])
app.include_router(carro.router, prefix="/carros", tags=["carros"])

@app.get('/', status_code=HTTPStatus.OK, response_model=dict)
def root():
    return {'message': 'API is working!'}