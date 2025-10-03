# Dicionário da Estrutura do Projeto: Horta Inteligente

Este documento detalha o propósito de cada pasta e arquivo dentro do projeto, servindo como um guia central para qualquer desenvolvedor.

---

## 🌳 Estrutura Geral

- **`projeto_horta_inteligente/`**: Diretório raiz que contém todos os módulos do projeto.

---

## ☁️ `api_backend/`

Módulo principal do servidor, escrito em Python com o framework FastAPI. É o cérebro que gerencia os dados, a lógica de negócio e as integrações.

- **`app/`**: Pacote Python contendo todo o código fonte da aplicação.
    - **`api/`**: Submódulo que organiza os endpoints (rotas) da API.
        - **`v1/`**: Agrupa todos os arquivos relacionados à versão 1 da API.
            - **`rotas/`**: Contém os arquivos que definem os endpoints.
                - `rota_chatbot.py`: Lógica para as rotas do chatbot do Telegram.
                - `rota_dados_sensores.py`: Lógica para a rota que recebe os dados do ESP32.
            - `roteador_principal.py`: Unifica todos os roteadores da `v1` para serem registrados na aplicação principal.
    - **`nucleo/`**: Armazena configurações centrais e lógica core da aplicação.
        - `configuracoes.py`: Carrega e gerencia as variáveis de ambiente (chaves de API, URI do banco) a partir do arquivo `.env`.
    - **`db/`**: Responsável pela comunicação com o banco de dados.
        - `conexao_mongodb.py`: Funções para conectar, desconectar e obter a instância do banco de dados MongoDB.
    - **`modelos/`**: Define os schemas (formatos) dos dados.
        - `esquemas.py`: Contém as classes Pydantic que validam os dados de entrada e saída da API.
    - **`servicos/`**: Camada da lógica de negócio.
        - `servico_chatbot.py`: Funções que processam as mensagens do chatbot e interagem com a IA.
        - `servico_banco_de_dados.py`: Funções que manipulam os dados no banco (salvar, buscar, etc.).
    - `main.py`: Ponto de entrada que inicializa e configura a aplicação FastAPI.
- **`testes/`**: Diretório para testes automatizados.
- **`.env`**: Arquivo local para armazenar segredos e credenciais (ex: senhas, API keys). **Não deve ser versionado no Git.**
- **`.env.example`**: Arquivo de exemplo que serve como guia para a criação do arquivo `.env`.
- **`.gitignore`**: Especifica quais arquivos e pastas o Git deve ignorar.
- **`README.md`**: Documentação específica do backend, com instruções de instalação e uso.
- **`requirements.txt`**: Lista de todas as bibliotecas Python necessárias para o backend.

---

## 📊 `dashboard/`

Módulo dedicado à camada de Business Intelligence (BI) e visualização de dados.

- **`README.md`**: Contém as instruções detalhadas para conectar a ferramenta de BI (Looker Studio) ao banco de dados, além do link para o dashboard publicado.

---

## 📟 `firmware_micropython/`

Contém todo o código MicroPython que será executado no microcontrolador ESP32.

- **`boot.py`**: Script executado uma única vez na inicialização do ESP32. Ideal para tarefas de configuração, como conectar à rede Wi-Fi.
- **`main.py`**: O código principal que roda em loop no dispositivo. Responsável por ler os sensores, formatar os dados e enviá-los para a `api_backend`.
- **`credenciais.py.example`**: Um modelo para o arquivo `credenciais.py`, que armazenará de forma segura os dados da rede Wi-Fi e outras informações sensíveis no dispositivo.
