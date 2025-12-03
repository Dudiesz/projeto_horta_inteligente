import requests
from fastapi import APIRouter, Body
from app.servicos import servico_chatbot
from app.nucleo.configuracoes import settings

router = APIRouter()

def limpar_texto_para_telegram(texto: str) -> str:
    """
    Remove caracteres de formatação Markdown que podem quebrar o envio.
    """
    # Remove asteriscos duplos e simples
    texto_limpo = texto.replace("**", "").replace("*", "")
    # Remove sublinhados que também podem dar erro
    texto_limpo = texto_limpo.replace("__", "")
    return texto_limpo

def enviar_mensagem_telegram(chat_id, texto):
    if not settings.TELEGRAM_BOT_TOKEN:
        print("ERRO: Token do Telegram não configurado.")
        return

    # --- A MÁGICA ACONTECE AQUI ---
    texto_seguro = limpar_texto_para_telegram(texto)
    # ------------------------------

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    
    # Enviamos sem parse_mode, garantindo que vá como texto puro
    payload = {
        "chat_id": chat_id,
        "text": texto_seguro
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"Erro ao enviar para Telegram: {response.text}")
    except Exception as e:
        print(f"Erro de conexão com Telegram: {e}")

@router.post("/webhook", summary="Recebe mensagens do Telegram")
async def webhook_telegram(update: dict = Body(...)):
    try:
        message = update.get("message", {})
        texto_usuario = message.get("text", "")
        chat_id = message.get("chat", {}).get("id")

        if not texto_usuario or not chat_id:
            return {"status": "ignorado"}

        print(f"--- Telegram: Mensagem de {chat_id}: {texto_usuario}")

        resposta_ia = await servico_chatbot.processar_mensagem_usuario(texto_usuario)
        
        enviar_mensagem_telegram(chat_id, resposta_ia)
        
        return {"status": "sucesso"}

    except Exception as e:
        print(f"Erro no webhook: {e}")
        return {"status": "erro"}