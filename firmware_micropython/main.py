# main.py

import time
import json
import random
from machine import Pin, ADC # Para a Umidade
import onewire, ds18x20 # Para a Temperatura (DS18B20)
try:
    import urequests as requests
except ImportError:
    print("ERRO: O módulo urequests não está instalado.")
    raise

# --- Configurações de Hardware e Aplicação ---

# Configuração da Umidade (ADC)
PINO_SENSOR_UMIDADE = 36 
MAX_ADC = 4095  # Calibração: Valor ADC de 12 bits (solo seco)
MIN_ADC = 1000  # Calibração: Valor ADC para água (solo úmido)

# Configuração da Temperatura (DS18B20 - OneWire)
PINO_SENSOR_TEMPERATURA = 4 # Pino GPIO 4 é o padrão para OneWire
# Inicializa o bus OneWire
ds_pin = Pin(PINO_SENSOR_TEMPERATURA)
ds_bus = onewire.OneWire(ds_pin)
# Inicializa o objeto do sensor DS18B20 e busca os dispositivos
ds_sensor = ds18x20.DS18X20(ds_bus)
# Encontra o endereço (rom) do sensor conectado
roms = ds_sensor.scan() 
print(f"Sensores DS18B20 encontrados: {roms}")


# Configurações de Rede
API_URL = "http://SEU_IP_OU_DOMINIO_DA_API/api/leituras" 
DEVICE_ID = "ESP32_Jardim_001"
SLEEP_INTERVAL_SECONDS = 300 # 5 minutos

# Inicializa o objeto ADC
adc = ADC(Pin(PINO_SENSOR_UMIDADE))
adc.width(ADC.WIDTH_12BIT)
adc.atten(ADC.ATTN_11DB) 

# --- Funções de Leitura Real ---

def ler_umidade_real():
    """
    Lê o valor analógico real do sensor de umidade e mapeia para porcentagem.
    """
    valor_bruto = adc.read()
    
    faixa_bruta = valor_bruto - MIN_ADC
    faixa_total = MAX_ADC - MIN_ADC
    
    if faixa_total <= 0:
        porcentagem = 0.0
    else:
        umidade_calculada = 100 - (faixa_bruta / faixa_total) * 100
        porcentagem = max(0.0, min(100.0, umidade_calculada))
    
    porcentagem_final = round(porcentagem, 1)

    print(f"Umidade REAL: {porcentagem_final}%")
    return porcentagem_final

def ler_temperatura_solo_real(roms):
    """
    Lê o valor do sensor digital DS18B20.
    """
    if not roms:
        print("AVISO: Nenhum sensor DS18B20 encontrado ou configurado.")
        return None
        
    try:
        # 1. Envia o comando para iniciar a conversão
        ds_sensor.convert_temp()
        time.sleep_ms(750) # Espera o tempo necessário para a conversão
        
        # 2. Lê a temperatura
        temperatura = ds_sensor.read_temp(roms[0]) # Lê o primeiro sensor encontrado
        
        temperatura_arredondada = round(temperatura, 1)
        print(f"Temperatura do Solo REAL: {temperatura_arredondada}°C")
        return temperatura_arredondada

    except Exception as e:
        print(f"ERRO ao ler DS18B20: {e}")
        return None


# --- Funções de Simulação ---

def simular_outros_dados():
    """
    SIMULAÇÃO: Gera dados fictícios para pH e NPK.
    A Temperatura do Ar foi REMOVIDA.
    """
    # pH (Levemente ácido a neutro)
    ph_solo = round(random.uniform(6.0, 7.2), 1) 
    
    # NPK (Nitrogênio, Fósforo, Potássio) em partes por milhão (ppm)
    n_ppm = random.randint(10, 50)
    p_ppm = random.randint(5, 25)
    k_ppm = random.randint(15, 60)
    
    dados_simulados = {
        "ph_solo": ph_solo,
        "n_ppm": n_ppm,
        "p_ppm": p_ppm,
        "k_ppm": k_ppm
    }
    
    print(f"Dados SIMULADOS gerados: pH={ph_solo}, NPK={n_ppm}/{p_ppm}/{k_ppm}")
    return dados_simulados

def ler_todos_os_dados():
    """
    Combina a leitura real de Umidade e Temperatura com a simulação de pH e NPK.
    """
    # 1. Leituras REAIS
    umidade = ler_umidade_real()
    temperatura_solo = ler_temperatura_solo_real(roms)
    
    # 2. Leitura SIMULADA
    dados_simulados = simular_outros_dados()
    
    # 3. Combina os resultados
    todos_os_dados = {}
    
    # Adiciona a umidade (sempre presente)
    todos_os_dados["umidade"] = umidade
    
    # Adiciona a temperatura (se a leitura for bem-sucedida)
    if temperatura_solo is not None:
        todos_os_dados["temperatura_solo"] = temperatura_solo
    
    # Adiciona os dados simulados
    todos_os_dados.update(dados_simulados) 

    return todos_os_dados


# --- Função de Envio (Permanece a mesma) ---

def enviar_dados_para_api(payload_json):
    """
    Envia a string JSON para a API.
    """
    headers = {'Content-Type': 'application/json'}
    
    try:
        print(f"Tentando enviar dados para: {API_URL}")
        response = requests.post(API_URL, data=payload_json, headers=headers)
        
        if response.status_code == 200 or response.status_code == 201:
            print(f"SUCESSO: Dados enviados. Status: {response.status_code}")
        else:
            print(f"AVISO: A API retornou um erro. Status: {response.status_code}. Resposta: {response.text}")
                
        response.close()

    except Exception as e:
        print(f"ERRO DE CONEXÃO: Não foi possível enviar os dados. Detalhe: {e}")

# --- Loop Principal ---

def main_loop():
    print("Iniciando loop principal (main.py)...")
    
    while True:
        try:
            # 1. Interface com os Sensores
            dados_lidos = ler_todos_os_dados()
            
            # 2. Estruturar os Dados
            payload = {
                "id_dispositivo": DEVICE_ID,
                "timestamp": time.time(),
                "leituras": dados_lidos  # Dicionário completo de leituras
            }
            
            # 3. Formatar para JSON
            payload_json = json.dumps(payload)
            
            # 4. Enviar para a API
            enviar_dados_para_api(payload_json)

        except Exception as e:
            print(f"ERRO CRÍTICO no ciclo principal: {e}")
            
        finally:
            # 5. Aguardar
            print(f"Ciclo completo. Dormindo por {SLEEP_INTERVAL_SECONDS} segundos...")
            time.sleep(SLEEP_INTERVAL_SECONDS)

# Executa o loop principal
if __name__ == "__main__":
    # Verifica se os sensores de temperatura foram encontrados antes de iniciar
    if roms or PINO_SENSOR_UMIDADE:
        main_loop()
    else:
        print("ERRO: O sistema não pode iniciar. Nenhum sensor essencial encontrado.")
