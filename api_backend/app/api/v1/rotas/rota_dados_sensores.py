from fastapi import APIRouter, status, HTTPException
from app.modelos import esquemas
# Importa o serviço que acabamos de criar
from app.servicos import servico_banco_de_dados 

# Cria o roteador (isso já existia)
router = APIRouter()

@router.post(
    "/dados-sensores", 
    # Atualizamos o response_model para refletir o que realmente retornamos
    response_model=esquemas.CreateResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Recebe e salva dados de um sensor."
)
async def criar_dados_sensor(dados: esquemas.DadosSensorCreate):
    """
    Endpoint para receber e salvar dados de sensores.

    - **Recebe**: JSON com dados do sensor (esquema DadosSensorCreate).
    - **Valida**: Automaticamente pelo Pydantic (como antes).
    - **Salva**: Chama o serviço para salvar no banco de dados (novo).
    - **Retorna**: O ID do novo registro (novo).
    """
    
    # Esta linha ainda é útil para vermos a atividade no log
    print(f"Dados recebidos do dispositivo: {dados.id_dispositivo}")
    
    # --- A GRANDE MUDANÇA ESTÁ AQUI ---
    # Em vez de só printar, chamamos a função do serviço
    inserted_id = servico_banco_de_dados.salvar_dados_sensor(dados)
    
    # Se o serviço retornar None, algo deu errado (ex: banco offline)
    if inserted_id is None:
        # Retorna um erro HTTP 500 (Erro Interno do Servidor)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro interno ao salvar os dados no banco de dados."
        )
    
    # Se tudo deu certo, retorna uma resposta de sucesso
    return {"status": "sucesso", "id_inserido": str(inserted_id)}