from fastapi import FastAPI
from app.api.v1.roteador_principal import api_router_v1

# Cria a instância principal da aplicação FastAPI
# Os metadados como title, version e description aparecerão na documentação automática.
app = FastAPI(
    title="API Horta Inteligente",
    version="0.1.0",
    description="API para coletar dados de sensores de uma horta e interagir com um assistente de IA."
)

# Inclui todas as rotas da v1 que foram agregadas no 'roteador_principal'.
# O prefixo '/api/v1' será adicionado na frente de todas essas rotas.
app.include_router(api_router_v1, prefix="/api/v1")

@app.get("/", tags=["Root"])
async def read_root():
    """
    Endpoint raiz para verificar se a API está online.
    """
    return {"status": "ok", "mensagem": "Bem-vindo à API da Horta Inteligente!"}