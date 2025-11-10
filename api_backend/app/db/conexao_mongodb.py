from pymongo import MongoClient
from pymongo.database import Database
from app.nucleo.configuracoes import settings

class DBConnection:
    """
    Classe simples para manter o estado da conexão (cliente e banco)
    acessível em um único lugar.
    """
    client: MongoClient | None = None
    db: Database | None = None

# Instância única que será importada por outros módulos
db_conn = DBConnection()

def connect_to_db():
    """
    Inicia a conexão com o MongoDB.
    Esta função será chamada quando a API iniciar.
    """
    print("Conectando ao MongoDB...")
    try:
        # Usa a URI carregada pelo arquivo de configurações
        db_conn.client = MongoClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=5000  # Tenta por 5s antes de falhar
        )
        
        # Testa a conexão para garantir que está tudo OK
        db_conn.client.server_info() 
        
        # Define qual banco de dados queremos usar dentro do cluster
        # Se não existir, o MongoDB o criará na primeira inserção
        db_conn.db = db_conn.client.get_database("horta_inteligente")
        
        print("Conexão com MongoDB estabelecida com sucesso.")
        
    except Exception as e:
        print(f"Erro ao conectar ao MongoDB: {e}")
        db_conn.client = None
        db_conn.db = None

def close_db_connection():
    """
    Fecha a conexão com o MongoDB.
    Esta função será chamada quando a API desligar.
    """
    if db_conn.client:
        db_conn.client.close()
        print("Conexão com MongoDB fechada.")

def get_db_collection(collection_name: str):
    """
    Função auxiliar que nossos 'serviços' usarão para obter
    uma 'collection' (tabela) específica do banco.
    """
    if db_conn.db is None:
        # Se o banco não estiver conectado, levanta um erro
        raise Exception("A conexão com o banco de dados não foi estabelecida.")
        
    # Retorna a coleção (ex: "dados_sensores")
    return db_conn.db[collection_name]