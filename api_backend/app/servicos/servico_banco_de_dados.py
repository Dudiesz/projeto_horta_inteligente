import datetime
from app.modelos import esquemas
from app.db.conexao_mongodb import get_db_collection
from pymongo.errors import PyMongoError
from pymongo import DESCENDING
import pytz

# Nome da coleção
COLLECTION_NAME = "dados_reais"

def salvar_dados_sensor(dados: esquemas.DadosSensorCreate):
    """
    1. Limpa campos vazios.
    2. Adiciona Data/Hora completa.
    3. Salva no Mongo.
    """
    try:
        collection = get_db_collection(COLLECTION_NAME)
        
        # 1. LIMPEZA: Converte para dicionário removendo os Nulos (None)
        # Isso remove ph, npk, etc., se não vierem do Arduino
        dados_dict = dados.model_dump(exclude_none=True) 
        
        # 2. ENRIQUECIMENTO: Adiciona o Calendário (Fuso Brasil)
        fuso_brasil = pytz.timezone('America/Sao_Paulo')
        agora = datetime.datetime.now(fuso_brasil)
        
        dados_dict["timestamp"] = agora
        dados_dict["data"] = agora.strftime("%d/%m/%Y") # 03/12/2025
        dados_dict["hora"] = agora.strftime("%H:%M:%S") # 19:30:00
        
        # Campos para filtros fáceis no Dashboard
        dados_dict["dia"] = agora.day
        dados_dict["mes"] = agora.month
        dados_dict["ano"] = agora.year
        dados_dict["hora_simples"] = agora.hour
        
        # 3. PERSISTÊNCIA: Salva o dicionário completo
        result = collection.insert_one(dados_dict)
        
        print(f"✅ [REAL] Salvo em '{COLLECTION_NAME}' | ID: {result.inserted_id}")
        return result.inserted_id
    
    except Exception as e:
        print(f"❌ Erro ao salvar: {e}")
        return None

def buscar_ultimos_dados():
    try:
        collection = get_db_collection(COLLECTION_NAME)
        return collection.find_one({}, sort=[("timestamp", DESCENDING)], projection={'_id': 0})
    except Exception as e:
        print(f"Erro busca: {e}")
        return None