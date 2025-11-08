/*
 * Código para leitura do sensor de umidade do solo FC-28 com ESP32
 * Versão com CALIBRAÇÃO e 6 NÍVEIS DE SEGMENTAÇÃO.
 */

// --- Configuração ---
const int PINO_SENSOR = 4; 

// --- Calibração (ATUALIZE COM SEUS VALORES!) ---
// Estes valores devem ser os que você mediu anteriormente.
const int VALOR_SECO = 3510;     // (Exemplo) Valor lido com sensor NO AR
const int VALOR_MOLHADO = 1350;  // (Exemplo) Valor lido com sensor NA ÁGUA

void setup() {
  Serial.begin(115200);
  Serial.println("Iniciando leitor de umidade (6 Níveis)...");
}

void loop() {
  // 1. Lê o valor bruto
  int valorBruto = analogRead(PINO_SENSOR);

  // 2. Garante que o valor esteja dentro da faixa de calibração
  int valorConstrito = constrain(valorBruto, VALOR_MOLHADO, VALOR_SECO);

  // 3. Mapeia para porcentagem (0-100%)
  int porcentagemUmidade = map(valorConstrito, VALOR_SECO, VALOR_MOLHADO, 0, 100);

  // 4. Segmenta e interpreta o valor (Usando a nova função)
  String estadoDoSolo = interpretarUmidade(porcentagemUmidade);

  // Exibe os resultados
  Serial.print("Valor Bruto: ");
  Serial.print(valorBruto);
  Serial.print(" \t| Umidade (%): ");
  Serial.print(porcentagemUmidade);
  Serial.print("% \t| Estado: ");
  Serial.println(estadoDoSolo);

  delay(2000);
}

/**
 * Função de Segmentação (Classificação) em 6 Níveis
 * Recebe a porcentagem de umidade e retorna um estado textual.
 * * ** AJUSTE ESTES VALORES DE % CONFORME SUA NECESSIDADE **
 */
String interpretarUmidade(int umidade) {
  if (umidade <= 15) {
    return "Muito Seco";
  } else if (umidade <= 30) {
    return "Seco";
  } else if (umidade <= 45) {
    return "Pouco Seco";
  } else if (umidade <= 60) {
    return "Pouco Umido";
  } else if (umidade <= 85) {
    return "Umido";
  } else { // (umidade > 85)
    // Usei "Encharcado" para "muito muito umido"
    return "Encharcado (Muito Umido)";
  }
}
