# main.py

import time
import json
import random # Necessário para a simulação
from machine import Pin, ADC 
try:
    import urequests as requests
except ImportError:
    print("ERRO: O módulo urequests não está instalado.")
    raise

# --- Configurações de Hardware e Aplicação ---
PINO_SENSOR_UMIDADE = 36 
# Calibração do ADC (Ajuste estes valores!):
MAX_ADC = 4095  # Valor ADC de 12 bits (solo seco)
MIN_ADC = 1000  # Valor ADC para água (solo úmido)

API_URL = "http://SEU_IP_OU_DOMINIO_DA_API/api/leituras" 
DEVICE_ID = "ESP32_Jardim_001"
SLEEP_INTERVAL_SECONDS = 300 # 5 minutos

# Inicializa o objeto ADC
adc = ADC(Pin(PINO_SENSOR_UMIDADE))
adc.width(ADC.WIDTH_12BIT)
adc.atten(ADC.ATTN_11DB) 

# --- Funções de Leitura e Simulação ---

def ler_umidade_real():
    """
    Lê o valor analógico real do sensor de umidade e mapeia para porcentagem.
    """
    valor_bruto = adc.read()
    
    # Mapeamento para Porcentagem (0-100%)
    faixa_bruta = valor_bruto - MIN_ADC
    faixa_total = MAX_ADC - MIN_ADC
    
    if faixa_total <= 0:
        porcentagem = 0.0
    else:
        # 100 - Porcentagem de secura (inverte a lógica)
        umidade_calculada = 100 - (faixa_bruta / faixa_total) * 100
        porcentagem = max(0.0, min(100.0, umidade_calculada))
    
    porcentagem_final = round(porcentagem, 1)

    print(f"Leitura Bruta ADC: {valor_bruto} -> Umidade REAL: {porcentagem_final}%")
    return porcentagem_final

def simular_outros_dados():
    """
    SIMULAÇÃO: Gera dados fictícios para pH, NPK e Temperatura do ar.
    """
    # pH (Levemente ácido a neutro)
    ph_solo = round(random.uniform(6.0, 7.2), 1) 
    
    # NPK (Nitrogênio, Fósforo, Potássio) em partes por milhão (ppm)
    n_ppm = random.randint(10, 50)
    p_ppm = random.randint(5, 25)
    k_ppm = random.randint(15, 60)
    
    # Temperatura do Ar (em Celsius)
    temperatura_ar = round(random.uniform(20.0, 30.0), 1)
    
    dados_simulados = {
        "ph_solo": ph_solo,
        "n_ppm": n_ppm,
        "p_ppm": p_ppm,
        "k_ppm": k_ppm,
        "temperatura_ar": temperatura_ar
    }
    
    print(f"Dados SIMULADOS gerados: pH={ph_solo}, Temp={temperatura_ar}°C, NPK={n_ppm}/{p_ppm}/{k_ppm}")
    return dados_simulados

def ler_todos_os_dados():
    """
    Combina a leitura real da umidade com a simulação dos demais dados.
    """
    # 1. Leitura REAL de umidade
    umidade = ler_umidade_real()
    
    # 2. Leitura SIMULADA dos outros parâmetros
    dados_simulados = simular_outros_dados()
    
    # 3. Combina os resultados
    todos_os_dados = {"umidade": umidade}
    todos_os_dados.update(dados_simulados) # Adiciona os dados simulados ao dicionário

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
            # 1. Interface com os Sensores (Real e Simulado)
            dados_lidos = ler_todos_os_dados()
            
            # 2. Estruturar os Dados
            payload = {
                "id_dispositivo": DEVICE_ID,
                "timestamp": time.time(),
                "leituras": dados_lidos  # Dicionário completo de leituras
            }
            
            print(f"Payload estruturado (completo): {payload}")
            
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
    main_loop()
