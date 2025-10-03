# Guia de Tarefas: API e Dados (Para Eduardo)

Olá, Eduardo.

Sua função é a de **arquiteto e guardião do núcleo do backend**. Você é responsável por garantir que a API funcione de maneira coesa, que os dados fluam corretamente desde a sua chegada até o armazenamento, e que estejam disponíveis para serem consumidos por outras partes do sistema (como o chatbot da IA e o dashboard).

Seu universo de trabalho abrange a estrutura geral da `api_backend/`, com foco especial em garantir que as partes construídas por Ricardo e Aurélio se conectem perfeitamente através da sua camada de dados.

---

## Estrutura de Trabalho e Suas Tarefas

### 1. Camada de Dados (Seu Foco Principal)

Esta é a sua principal responsabilidade: gerenciar como a aplicação interage com o banco de dados MongoDB.

* **Arquivo:** `app/db/conexao_mongodb.py`
    * **O que é?** O ponto central e único de conexão com o banco de dados.
    * **Sua Tarefa Aqui:**
        1.  Implementar a lógica para se conectar ao cluster do MongoDB Atlas usando a biblioteca `pymongo`.
        2.  A string de conexão (URI) deve ser lida a partir das configurações (`configuracoes.py`), nunca escrita diretamente no código.
        3.  Criar funções auxiliares para iniciar a conexão quando a API sobe e fechar a conexão quando ela desce (usando os eventos de "lifespan" do FastAPI).

* **Arquivo:** `app/servicos/servico_banco_de_dados.py`
    * **O que é?** O coração da lógica de dados. Este arquivo isola o resto da aplicação dos detalhes de implementação do MongoDB. Nenhuma outra parte do código (além deste serviço) deve "falar" diretamente com o banco.
    * **Sua Tarefa Aqui:**
        1.  **Criar a função `salvar_dados_sensor(dados: esquemas.DadosSensorCreate)`:**
            * Ela receberá o objeto de dados validado vindo da rota.
            * Irá converter o objeto Pydantic para um dicionário Python.
            * Adicionará um `timestamp` gerado no lado do servidor para garantir a consistência.
            * Usará `pymongo` para inserir este dicionário como um novo documento na coleção correta no MongoDB.
        2.  **Criar funções de consulta (para o futuro):**
            * Implementar funções como `buscar_ultima_leitura_sensores()` ou `buscar_leituras_por_periodo(data_inicio, data_fim)`.
            * Essas funções serão essenciais para que o serviço do Aurélio (IA/Chatbot) possa obter dados para dar respostas contextuais e para que o dashboard possa exibir gráficos.

---

### 2. Camada de API e Aplicação Principal

Você é o responsável por montar o "quebra-cabeça" da API.

* **Arquivo:** `app/api/v1/roteador_principal.py`
    * **O que é?** O arquivo que agrega todas as rotas da versão 1 da nossa API.
    * **Sua Tarefa Aqui:**
        1.  Importar os `router` dos arquivos `rota_dados_sensores.py` (de Ricardo/Dados) e `rota_chatbot.py` (de Aurélio).
        2.  Incluí-los em um `APIRouter` principal da v1, para manter o `main.py` limpo.

* **Arquivo:** `app/main.py`
    * **O que é?** O ponto de entrada que inicia o servidor FastAPI.
    * **Sua Tarefa Aqui:**
        1.  Criar a instância principal do FastAPI.
        2.  Incluir o roteador principal da v1 (`roteador_principal.py`) na aplicação.
        3.  Configurar o `lifespan` para gerenciar a conexão com o banco de dados.
        4.  Configurar CORS (Cross-Origin Resource Sharing) se for necessário no futuro para o dashboard.

* **Arquivo:** `app/api/v1/rotas/rota_dados_sensores.py` (Integração)
    * **Sua Tarefa Aqui:**
        1.  Você irá editar este arquivo para **conectar a rota ao seu serviço**. A função `criar_dados_sensor` não irá mais apenas "printar" os dados; ela deverá chamar a função `salvar_dados_sensor` que você criou no `servico_banco_de_dados.py`.

---

### 3. Camada de Configuração

* **Arquivos:** `.env.example` e `app/nucleo/configuracoes.py`
    * **O que são?** Gerenciam as configurações e segredos.
    * **Sua Tarefa Aqui:**
        1.  Adicionar a variável `MONGODB_URI` ao arquivo `.env.example`.
        2.  Garantir que o `configuracoes.py` carregue esta variável para ser usada no módulo de conexão com o banco.

---

## Plano de Ação Sugerido para Começar

1.  **Obtenha a URI do MongoDB:** Crie uma conta gratuita no [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register), crie um cluster gratuito (tier M0) e obtenha a string de conexão (URI). Lembre-se de liberar o acesso para todos os IPs (`0.0.0.0/0`) para facilitar os testes iniciais.
2.  **Configure o Ambiente:** Adicione a `MONGODB_URI` ao seu arquivo `.env` local e atualize o `.env.example`.
3.  **Foco na Conexão (`conexao_mongodb.py`):** Crie um script de teste simples e separado para garantir que sua aplicação consegue se conectar com sucesso ao cluster na nuvem. Esta é a validação mais importante.
4.  **Implemente o Serviço (`servico_banco_de_dados.py`):** Crie a função `salvar_dados_sensor`.
5.  **Integre com a Rota (`rota_dados_sensores.py`):** Faça a rota chamar o seu serviço.
6.  **Junte Tudo (`main.py`):** Monte a aplicação principal para poder executar o servidor e testar o fluxo completo com o script simulador.
