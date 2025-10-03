# Guia de Tarefas: Inteligência Artificial e Chatbot (Para Aurélio)

Olá, Aurélio.

Sua missão é dar vida ao assistente virtual da horta. Você irá construir a ponte entre o usuário no **Telegram** e o cérebro de Inteligência Artificial (**Google Gemini**), permitindo que se façam perguntas em linguagem natural sobre o estado do cultivo.

Seu universo de trabalho será principalmente dentro da pasta `api_backend/`, com foco especial nos seguintes arquivos:

* `app/servicos/servico_chatbot.py` (Onde a mágica da IA acontece)
* `app/api/v1/rotas/rota_chatbot.py` (A porta de entrada para o Telegram)
* `.env.example` e `app/nucleo/configuracoes.py` (Para gerenciar as chaves de API)

---

## Estrutura de Trabalho e Suas Tarefas

### 1. Arquivo: `app/servicos/servico_chatbot.py`

* **O que é?** Este é o **cérebro** da sua funcionalidade. Toda a lógica de negócio, processamento de linguagem e comunicação com a IA do Google deve residir aqui. Manter a lógica separada da rota (API) é uma boa prática que facilita os testes e a manutenção.

* **Sua Tarefa Aqui:**
    1.  **Conexão com Gemini:** Implementar uma função que se conecte à API do Google Gemini. Esta função deve receber um texto (o "prompt") e retornar a resposta gerada pelo modelo `Gemini 1.5 Flash`. A chave da API deve ser lida a partir das configurações do ambiente, nunca diretamente no código.
    2.  **Lógica de Resposta:** Criar a função principal de processamento, como `processar_mensagem_usuario(texto_da_mensagem: str)`.
    3.  **Construção do Prompt:** Inicialmente, esta função pode simplesmente repassar a pergunta do usuário para o Gemini. No futuro, ela se tornará mais inteligente: você irá enriquecer o prompt com dados do projeto.
        * **Exemplo Futuro:** Se o usuário perguntar "Como está a umidade?", sua função primeiro buscará o último dado de umidade no banco de dados (interagindo com o `servico_banco_de_dados`) e depois montará um prompt para o Gemini como: *"Contexto: A última leitura de umidade do solo foi de 65%. Pergunta do usuário: Como está a umidade? Por favor, gere uma resposta amigável."*

---

### 2. Arquivo: `app/api/v1/rotas/rota_chatbot.py`

* **O que é?** Esta é a **porta de entrada** para o mundo exterior. É o endpoint (URL) que o Telegram irá chamar sempre que um usuário enviar uma mensagem para o nosso bot. Isso é conhecido como "Webhook".

* **Sua Tarefa Aqui:**
    1.  **Definir o Endpoint do Webhook:** Criar uma rota usando o `APIRouter` do FastAPI que aceite requisições **HTTP POST** em uma URL como `/chatbot/webhook`.
    2.  **Receber e Validar a Mensagem:** O Telegram envia um objeto JSON complexo. Você precisará definir um esquema Pydantic (no arquivo `app/modelos/esquemas.py`) para mapear e validar essa estrutura, facilitando a extração do texto da mensagem do usuário e do ID da conversa.
    3.  **Chamar o Serviço:** A única responsabilidade desta rota é extrair a informação relevante (o texto da mensagem) e passá-la para a sua função `processar_mensagem_usuario` no `servico_chatbot.py`.
    4.  **Responder ao Usuário:** Após receber a resposta do serviço, esta rota será responsável por usar a API do Telegram para enviar a mensagem de volta para o chat do usuário correto.

---

### 3. Arquivos de Configuração (`.env.example` e `app/nucleo/configuracoes.py`)

* **O que são?** São os arquivos que gerenciam as configurações e segredos do projeto.

* **Sua Tarefa Aqui:**
    1.  Adicionar as novas variáveis de ambiente necessárias ao arquivo `.env.example`: `TELEGRAM_BOT_TOKEN` e `GOOGLE_API_KEY`.
    2.  Assegurar que o arquivo `app/nucleo/configuracoes.py` seja atualizado para carregar essas novas variáveis, disponibilizando-as para o resto da aplicação.

---

## Plano de Ação Sugerido para Começar

1.  **Obtenha as Chaves:**
    * Fale com o **"BotFather"** no Telegram para criar um novo bot e obter seu `TELEGRAM_BOT_TOKEN`.
    * Acesse o **Google AI Studio** para gerar sua `GOOGLE_API_KEY` para o Gemini.
2.  **Configure o Ambiente:** Adicione essas duas chaves ao seu arquivo `.env` local (que não está no Git) e atualize o `.env.example` com os nomes das variáveis.
3.  **Comece pelo Serviço (`servico_chatbot.py`):** Crie um script de teste simples e separado (que não seja parte da API ainda) para focar em fazer a comunicação com a API do Gemini funcionar. Dê a ele um texto fixo e veja se ele retorna uma resposta. Isso isola o problema e facilita a depuração.
4.  **Construa o Webhook:** Uma vez que a lógica de IA esteja funcionando isoladamente, passe para a implementação da rota em `rota_chatbot.py` para receber as mensagens do Telegram.

Seguindo estes passos, você construirá a funcionalidade de forma incremental e organizada.
