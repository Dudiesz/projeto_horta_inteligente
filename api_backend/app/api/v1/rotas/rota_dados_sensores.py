from fastapi import APIRouter, status
from app.modelos import esquemas

# Cria um "roteador" que agrupará todas as rotas relacionadas a dados de sensores.
# É uma boa prática para organizar o projeto.
router = APIRouter()

@router.post(
    "/dados-sensores", 
    response_model=esquemas.DadosSensorCreate, 
    status_code=status.HTTP_201_CREATED,
    summary="Recebe e processa dados de um sensor."
)
async def criar_dados_sensor(dados: esquemas.DadosSensorCreate):
    """
    Endpoint para receber dados de sensores.

    - **Recebe**: um JSON com os dados do sensor, que deve seguir o esquema `DadosSensorCreate`.
    - **Valida**: Automaticamente os tipos de dados e a estrutura da requisição.
    - **Retorna**: Uma confirmação com os dados que foram recebidos.
    """
    
    # Por enquanto, vamos apenas imprimir os dados no console para confirmar o recebimento.
    # O .model_dump() converte o objeto Pydantic de volta para um dicionário Python.
    print("Dados recebidos do dispositivo:", dados.model_dump())
    
    # A lógica para salvar no banco de dados será adicionada futuramente na camada de serviço.
    
    return dados