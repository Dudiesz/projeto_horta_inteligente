from fastapi import APIRouter

# Importa as rotas específicas que criamos e que vamos criar
from app.api.v1.rotas import rota_dados_sensores
# from app.api.v1.rotas import rota_chatbot # <- Será adicionado no futuro

# Cria uma instância do APIRouter que representará a v1 da nossa API
api_router_v1 = APIRouter()

# Inclui as rotas do módulo de sensores no roteador principal.
# Todas as rotas definidas em 'rota_dados_sensores' serão adicionadas.
# A tag é usada para agrupar os endpoints na documentação automática da API.
api_router_v1.include_router(rota_dados_sensores.router, tags=["Dados dos Sensores"])

# Linha de exemplo para quando o chatbot do Aurélio for integrado
# api_router_v1.include_router(rota_chatbot.router, prefix="/chatbot", tags=["Chatbot"])