import google.generativeai as genai
import os
from dotenv import load_dotenv

# Carrega a chave do .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Erro: Chave GOOGLE_API_KEY não encontrada no arquivo .env")
else:
    genai.configure(api_key=api_key)
    print(f"✅ Chave encontrada! Listando modelos disponíveis para você...\n")
    
    try:
        # Lista todos os modelos que servem para gerar texto (generateContent)
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
    except Exception as e:
        print(f"❌ Erro ao listar modelos: {e}")