import datetime
from app.modelos import esquemas
from app.db.conexao_mongodb import get_db_collection
from pymongo.errors import PyMongoError

# Define o nome da 'collection' (tabela) que usaremos no MongoDB
COLLECTION_NAME = "dados_sensores"

def salvar_dados_sensor(dados: esquemas.DadosSensorCreate):
    """
    Recebe os dados validados do sensor, adiciona um timestamp 
    e os insere no banco de dados.
    """
    try:
        # Pega a coleção (tabela) "dados_sensores"
        # Esta função vem do arquivo que acabamos de criar (Passo 6)
        collection = get_db_collection(COLLECTION_NAME)
        
        # Converte o modelo Pydantic (esquemas.py - Passo 1)
        # de volta para um dicionário Python simples
        dados_dict = dados.model_dump()
        
        # Adiciona o timestamp do servidor (importante para consistência)
        # Usamos UTC para um fuso horário padronizado
        dados_dict["timestamp"] = datetime.datetime.now(datetime.timezone.utc)
        
        # Insere o dicionário como um novo 'documento' no MongoDB
        result = collection.insert_one(dados_dict)
        
        print(f"Dados salvos no MongoDB com sucesso. ID: {result.inserted_id}")
        
        # Retorna o ID do objeto que acabou de ser inserido
        return result.inserted_id
    
    except PyMongoError as e:
        # Erro específico do MongoDB
        print(f"Erro ao salvar dados no MongoDB: {e}")
        return None
    except Exception as e:
        # Qualquer outro erro inesperado
        print(f"Erro inesperado no serviço de banco de dados: {e}")
        return None