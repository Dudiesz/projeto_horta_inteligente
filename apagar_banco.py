from pymongo import MongoClient
from dotenv import load_dotenv
import os

# 1. Carrega configurações
load_dotenv("api_backend/.env")
URI = os.getenv("MONGODB_URI")

# ⚠️ NOME DA COLEÇÃO (Confira se está certo!)
COLLECTION_NAME = "dados_sinteticos"

def limpar_tudo():
    print("--- INICIANDO LIMPEZA DO BANCO DE DADOS ---")
    
    try:
        # Conecta
        client = MongoClient(URI)
        db = client["horta_inteligente"]
        collection = db[COLLECTION_NAME]
        
        # Conta antes
        qtd_antes = collection.count_documents({})
        print(f"📉 Documentos encontrados: {qtd_antes}")
        
        if qtd_antes == 0:
            print("✅ A coleção já está vazia.")
            return

        # Pergunta de segurança
        confirmacao = input(f"TEM CERTEZA que deseja apagar {qtd_antes} registros? (s/n): ")
        
        if confirmacao.lower() == 's':
            # --- O COMANDO DE DESTRUIR ---
            resultado = collection.delete_many({}) 
            # -----------------------------
            
            print(f"🗑️ Sucesso! {resultado.deleted_count} documentos foram apagados.")
            print("✨ O banco está limpo e pronto para novos dados.")
        else:
            print("❌ Operação cancelada.")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    limpar_tudo()