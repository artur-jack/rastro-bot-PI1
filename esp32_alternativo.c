#include <BluetoothSerial.h>
#include <ArduinoJson.h>
#include <time.h>

BluetoothSerial SerialBT;

String getCurrentTime() {
  time_t now = time(nullptr);
  struct tm* p_tm = localtime(&now);
  char buffer[20];
  sprintf(buffer, "%04d-%02d-%02d %02d:%02d:%02d", 
          p_tm->tm_year + 1900, p_tm->tm_mon + 1, p_tm->tm_mday, 
          p_tm->tm_hour, p_tm->tm_min, p_tm->tm_sec);
  return String(buffer);
}

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32"); // Nome do dispositivo Bluetooth da ESP32

  Serial.println("Espere uma conexão Bluetooth...");

  // Configuração de tempo (opcional, necessário se você quiser obter a hora correta)
  configTime(0, 0, "pool.ntp.org"); // Use NTP para obter a hora correta
}

void loop() {
  if (SerialBT.connected()) {
    // Leitura dos valores dos sensores e outros dados
    int sensorEsquerdo = analogRead(34); // Exemplo de leitura do sensor esquerdo
    int sensorDireito = analogRead(35); // Exemplo de leitura do sensor direito
    float velocidade = 10.5; // Exemplo de leitura da velocidade
    float distancia = 20.0; // Exemplo de leitura da distância
    
    // Criar um objeto JSON
    StaticJsonDocument<256> jsonDocument;
    jsonDocument["sensor_esquerdo"] = sensorEsquerdo;
    jsonDocument["sensor_direito"] = sensorDireito;
    jsonDocument["velocidade"] = velocidade;
    jsonDocument["distancia"] = distancia;
    jsonDocument["current_time"] = getCurrentTime(); // Adiciona o tempo formatado
    
    // Serializar o JSON em uma String
    String jsonString;
    serializeJson(jsonDocument, jsonString);
    
    // Enviar o JSON via Bluetooth
    SerialBT.println(jsonString);
    Serial.println("Enviado: " + jsonString);

    delay(200); // Atraso para evitar sobrecarga do envio de dados
  }
}
