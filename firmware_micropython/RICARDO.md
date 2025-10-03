# Guia de Tarefas: Desenvolvimento do Firmware (Para Ricardo)

Olá, Ricardo.

Sua responsabilidade neste projeto é o "cérebro de campo": o código **MicroPython** que será executado no microcontrolador **ESP32**. Seu objetivo é ler os dados do sensor de solo e enviá-los para a nossa API na nuvem.

Seu universo de trabalho será a pasta `firmware_micropython/`.

---

Veja o que fazer em cada arquivo:

### 1. Arquivo: `boot.py`

* **O que é?** Este é o primeiro script que o ESP32 executa quando é ligado ou reiniciado. Sua principal e única função é preparar o ambiente, o que no nosso caso significa **conectar à internet**.

* **Sua Tarefa Aqui:**
    1.  Escrever o código para que o ESP32 se conecte à rede Wi-Fi.
    2.  As credenciais da rede (nome e senha) não devem ser escritas diretamente neste arquivo. Elas devem ser importadas de um arquivo chamado `credenciais.py`.
    3.  Implementar uma lógica que, após a tentativa de conexão, verifique se a conexão foi bem-sucedida e imprima o endereço de IP do dispositivo no console. Isso é fundamental para depuração.

---

### 2. Arquivo: `credenciais.py.example`

* **O que é?** É um arquivo de **exemplo/template**. Ele mostra quais variáveis o código precisa, mas com valores vazios. Este arquivo **é salvo no Git**, servindo como um guia para a equipe. O arquivo `credenciais.py` real, com as senhas, **não será salvo no Git**.

* **Sua Tarefa Aqui:**
    1.  Definir neste arquivo as variáveis que serão necessárias para o projeto. Por exemplo:

        ```python
        # credenciais.py.example
        WIFI_SSID = "NOME_DA_REDE_WIFI"
        WIFI_PASSWORD = "SENHA_DA_REDE_WIFI"

        API_ENDPOINT = "URL_DA_NOSSA_API_QUANDO_ESTIVER_PRONTA"
        ID_DISPOSITIVO = "ESP32_HORTA_01"
        ```
    2.  Você (e cada membro da equipe) deverá criar uma cópia deste arquivo, renomeá-la para `credenciais.py` e preencher com os dados reais para seus testes locais.

---

### 3. Arquivo: `main.py`

* **O que é?** Este é o coração do firmware. Ele é executado em um loop infinito logo após o `boot.py` terminar com sucesso. É aqui que toda a lógica principal de leitura e envio de dados vai residir.

* **Sua Tarefa Aqui:** Implementar o loop principal que fará o seguinte ciclo:
    1.  **Interface com o Sensor:** Escrever o código para se comunicar com o sensor de solo e solicitar as leituras (umidade, pH, NPK, etc.).
        * **Plano B (Para começar AGORA):** Como ainda não temos o sensor físico, o primeiro passo é criar uma função que **simula** essa leitura, gerando dados fictícios, mas realistas. Ex: `def ler_sensor_simulado(): return {"umidade": 65.5, "ph_solo": 6.8, ...}`.
    2.  **Estruturar os Dados:** Montar um dicionário Python com os dados lidos (ou simulados), seguindo exatamente a estrutura que definimos para a API (ex: `{"id_dispositivo": ..., "umidade": ..., "ph_solo": ...}`).
    3.  **Formatar para JSON:** Converter o dicionário para uma string no formato JSON.
    4.  **Enviar para a API:** Usar uma biblioteca como `urequests` para fazer uma requisição **HTTP POST** para o endpoint da nossa API, enviando o JSON no corpo da requisição.
    5.  **Tratamento de Erros:** Garantir que o código não trave se a internet cair ou a API não responder. Use blocos `try...except`.
    6.  **Aguardar:** Fazer o ESP32 "dormir" por um intervalo de tempo definido (ex: 5 minutos) antes de repetir o ciclo.

---

## Plano de Ação Sugerido para Começar

1.  **Clone o repositório** para ter a estrutura completa do projeto.
2.  Trabalhe exclusivamente na pasta `firmware_micropython/`.
3.  **Comece pelo `boot.py`**. Faça o ESP32 se conectar ao Wi-Fi da sua casa. Este é o primeiro "Hello, World!" de qualquer projeto IoT.
4.  Em seguida, no `main.py`, foque na **lógica de simulação de dados**. O objetivo inicial é fazer o ESP32 enviar, a cada minuto, um JSON com dados *simulados* para um serviço de teste online (como o [Webhook.site](https://webhook.site/)), para validar o envio HTTP.
