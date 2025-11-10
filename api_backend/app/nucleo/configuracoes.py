from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    """
    Carrega e valida as variáveis de ambiente do projeto.
    """
    
    # Carrega as variáveis de um arquivo .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # --- Variáveis do Banco de Dados (Eduardo) ---
    MONGODB_URI: str
    
    # --- Variáveis do Chatbot (Aurélio) ---
    GOOGLE_API_KEY: Optional[str] = None
    TELEGRAM_BOT_TOKEN: Optional[str] = None

# Cria uma instância única das configurações
settings = Settings()