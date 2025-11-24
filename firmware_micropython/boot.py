# boot.py

# Importa os módulos necessários
import network
import time

# Importa as credenciais do arquivo credenciais.py
# Este arquivo DEVE conter as variáveis SSID e PASSWORD.
try:
    from credenciais import SSID, PASSWORD
except ImportError:
    print("ERRO: Não foi possível importar SSID e/ou PASSWORD do arquivo credenciais.py.")
    print("Certifique-se de que o arquivo existe e contém ambas as variáveis.")
    # Se não puder importar, não há como continuar, então paramos.
    raise

# Define a função de conexão
def connect_to_wifi(ssid, password, max_attempts=10):
    """
    Tenta conectar o ESP32 à rede Wi-Fi.
    """
    
    # 1. Cria a interface da estação (Station)
    sta_if = network.WLAN(network.STA_IF)
    
    # 2. Verifica se já está conectado e desliga/liga se necessário
    if not sta_if.isconnected():
        print(f"Tentando conectar à rede '{ssid}'...")
        sta_if.active(True) # Ativa a interface
        sta_if.connect(ssid, password)
        
        # 3. Loop de tentativa de conexão
        attempt_count = 0
        while not sta_if.isconnected() and attempt_count < max_attempts:
            # Espera 1 segundo entre as tentativas
            print('.', end='') # Imprime um ponto para mostrar que está tentando
            time.sleep(1)
            attempt_count += 1
            
        print() # Nova linha após o loop de pontos

    # 4. Verifica o resultado final
    if sta_if.isconnected():
        # Conexão bem-sucedida
        print("Conexão Wi-Fi bem-sucedida!")
        # Imprime o endereço IP (Tupla: (IP, Netmask, Gateway, DNS))
        ip_address = sta_if.ifconfig()[0]
        print(f"Endereço IP do dispositivo: {ip_address}")
    else:
        # Falha na conexão
        print("ERRO: Falha na conexão Wi-Fi após várias tentativas.")
        print("Verifique o SSID e a senha em credenciais.py.")

# Executa a função de conexão
connect_to_wifi(SSID, PASSWORD)
