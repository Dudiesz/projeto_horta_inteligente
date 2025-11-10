from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1.roteador_principal import api_router_v1
# Importa o módulo de conexão que criamos no Passo 6
from app.db import conexao_mongodb 

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerenciador de ciclo de vida da aplicação.
    Executa o código antes do 'yield' ao iniciar.
    Executa o código depois do 'yield' ao desligar.
    """
    # Código a ser executado ANTES da aplicação iniciar
    print("Iniciando aplicação...")
    # Chama nossa função para conectar ao banco de dados
    conexao_mongodb.connect_to_db()
    
    yield  # Este 'yield' é o ponto onde a aplicação fica rodando
    
    # Código a ser executado DEPOIS da aplicação parar
    print("Desligando aplicação...")
    # Chama nossa função para fechar a conexão
    conexao_mongodb.close_db_connection()

# Cria a instância principal da aplicação FastAPI
app = FastAPI(
    title="API Horta Inteligente",
    version="0.1.0",
    description="API para coletar dados de sensores de uma horta e interagir com um assistente de IA.",
    lifespan=lifespan  # Informa ao FastAPI para usar nosso gerenciador de ciclo de vida
)

# Inclui todas as rotas da v1 que foram agregadas no 'roteador_principal'.
app.include_router(api_router_v1, prefix="/api/v1")

@app.get("/", tags=["Root"])
async def read_root():
    """
    Endpoint raiz para verificar se a API está online.
    """
    return {"status": "ok", "mensagem": "Bem-vindo à API da Horta Inteligente!"}