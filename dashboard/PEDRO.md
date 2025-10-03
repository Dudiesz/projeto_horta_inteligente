# Guia de Tarefas: Dashboard de BI (Para Pedro)

Olá, Pedro.

Sua missão é ser o **analista de dados e especialista em Business Intelligence (BI)** da equipe. Seu objetivo é transformar os dados brutos que coletamos da horta em *insights* visuais e compreensíveis. Você será o responsável por responder à pergunta: "O que os dados estão nos dizendo?".

Seu trabalho não será primariamente no VS Code, mas sim em uma plataforma web poderosa e em documentar seus resultados.

### Seu Ambiente de Trabalho

* **Ferramenta Principal:** [**Google Looker Studio**](https://lookerstudio.google.com/) (antigo Data Studio). É aqui que você vai construir o dashboard.
* **Fonte de Dados:** O cluster do **MongoDB Atlas** do nosso projeto, onde todos os dados dos sensores estarão armazenados.
* **Seu "Arquivo" no Projeto:** O `dashboard/README.md`. Este arquivo é onde você irá documentar o processo e, mais importante, colocar o link para o dashboard final.

---

## Estrutura de Trabalho e Suas Tarefas

Seu trabalho é um processo que começa com a conexão dos dados e termina com a criação de um relatório interativo.

### 1. Acesso e Preparação

* **O que é?** A fase inicial para garantir que você tenha tudo o que precisa para começar.
* **Sua Tarefa Aqui:**
    1.  **Obter Acesso ao Banco de Dados:** Você precisará conversar com o **Eduardo** (responsável pela API e Dados) para obter a **string de conexão (URI)** do nosso cluster no MongoDB Atlas.
    2.  **Liberar Acesso (se necessário):** Eduardo também precisará garantir que o seu endereço de IP esteja liberado nas configurações de segurança do MongoDB Atlas para que o Looker Studio possa se conectar.
    3.  **Familiarização com a Ferramenta:** Enquanto espera os primeiros dados serem coletados, sua tarefa é explorar o Google Looker Studio. Assista a alguns tutoriais básicos no YouTube, especialmente sobre como conectar o Looker Studio a uma fonte de dados do MongoDB.

---

### 2. Conexão da Fonte de Dados

* **O que é?** Ensinar ao Looker Studio onde nossos dados estão e como acessá-los.
* **Sua Tarefa Aqui:**
    1.  Dentro do Looker Studio, vá em `Criar` e selecione `Fonte de dados`.
    2.  Na galeria de conectores, procure e selecione o conector oficial do **MongoDB**.
    3.  Configure a conexão usando a string de conexão (URI) fornecida pelo Eduardo.
    4.  Especifique o **Database** (banco de dados) e a **Collection** (coleção) que vamos usar (ex: database `horta_inteligente`, collection `dados_sensores`).
    5.  Ao final, você deverá ver os campos do nosso sensor (`umidade`, `ph_solo`, `timestamp`, etc.) disponíveis no Looker Studio.

---

### 3. Construção do Dashboard

* **O que é?** A parte criativa e analítica, onde você monta os gráficos e visualizações.
* **Sua Tarefa Aqui:**
    1.  Crie um novo **Relatório** no Looker Studio e associe a ele a fonte de dados do MongoDB que você acabou de criar.
    2.  **Planeje e Crie os Gráficos:** Comece com visualizações essenciais:
        * **Gráfico de Série Temporal:** Crie um gráfico de linhas que mostre a variação da `umidade` e da `temperatura` ao longo do `timestamp`.
        * **Medidores (Gauges):** Adicione medidores que mostrem o valor **mais recente** de cada sensor (pH, Nitrogênio, Potássio, Fósforo).
        * **Tabela:** Insira uma tabela que mostre as últimas 10 ou 20 leituras completas, com todos os dados.
    3.  **Adicione Interatividade:** Insira um controle de **período**, permitindo que o usuário filtre os dados do dashboard para ver uma data ou semana específica.

---

### 4. Documentação e Compartilhamento

* **O que é?** Finalizar e entregar o seu trabalho para a equipe.
* **Sua Tarefa Aqui:**
    1.  No Looker Studio, clique em `Compartilhar` para gerar um link público (ou restrito à equipe) para o seu dashboard.
    2.  Edite o arquivo `dashboard/README.md` no nosso repositório Git.
    3.  Cole o **link do dashboard** no `README.md` e escreva uma breve descrição do que cada gráfico no dashboard representa.

---

## Plano de Ação Sugerido para Começar

1.  **Comunique-se:** Sua primeira ação é alinhar com o **Eduardo** para obter as credenciais do MongoDB Atlas. Você depende dos dados que a parte dele do sistema irá salvar.
2.  **Aprenda:** Enquanto os primeiros dados não estão disponíveis, assista a 1 ou 2 vídeos sobre "Conectar MongoDB ao Looker Studio". Isso vai te poupar muito tempo.
3.  **Conecte:** Assim que houver dados de teste no banco, seu primeiro objetivo técnico é simples: conseguir criar a **Fonte de Dados** no Looker Studio e ver os nomes dos nossos campos (`umidade`, `ph_solo`, etc.) aparecerem na plataforma.
4.  **Crie o Primeiro Gráfico:** Comece com o mais simples e mais importante: um gráfico de linhas mostrando a `umidade` pelo `timestamp`.
