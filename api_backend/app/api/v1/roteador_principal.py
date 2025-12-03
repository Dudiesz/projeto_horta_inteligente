from fastapi import APIRouter

# Importa as rotas
from app.api.v1.rotas import rota_dados_sensores
from app.api.v1.rotas import rota_chatbot  # <--- CERTIFIQUE-SE DE QUE ESTA LINHA EXISTE

api_router_v1 = APIRouter()

# Inclui a rota de Sensores
api_router_v1.include_router(rota_dados_sensores.router, tags=["Dados dos Sensores"])

# Inclui a rota do Chatbot (ADICIONE ESTA LINHA)
api_router_v1.include_router(rota_chatbot.router, prefix="/chatbot", tags=["Chatbot"])