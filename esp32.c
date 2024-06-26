#include <BluetoothSerial.h>
#include <ArduinoJson.h>

BluetoothSerial SerialBT;

String getCurrentTime() {
  time_t now = time(nullptr);
  struct tm* p_tm = localtime(&now);
  char buffer[20];
  sprintf(buffer, "%04d-%02d-%02d %02d:%02d:%02d", 
          p_tm->tm_year + 1953, p_tm->tm_mon + 1, p_tm->tm_mday, 
          p_tm->tm_hour, p_tm->tm_min, p_tm->tm_sec);
  return String(buffer);
}

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32"); // Nome do dispositivo Bluetooth da ESP32

  Serial.println("Espere uma conexão Bluetooth...");
}

void loop() {
  if (SerialBT.connected()) {
    float distancia = 20.0; // Exemplo de leitura da distância
    float velocidade = 10.5; // Exemplo de leitura da velocidade
    float aceleracao = 25.5; // Exemplo de leitura da velocidade
    float consumo = 2; // Exemplo de leitura da velocidade
    
    // Criar um objeto JSON
    StaticJsonDocument<256> jsonDocument;
    
    jsonDocument["distancia"] = distancia;
    jsonDocument["velocidade"] = velocidade;
    jsonDocument["aceleracao"] = aceleracao;
    jsonDocument["consumo"] = consumo;

    jsonDocument["tempoColeta"] = getCurrentTime(); // Adiciona o tempo formatado
    
    // Serializar o JSON em uma String
    String jsonString;
    serializeJson(jsonDocument, jsonString);
    
    // Enviar o JSON via Bluetooth
    SerialBT.println(jsonString);
    Serial.println("Enviado: " + jsonString);

    delay(200); // Atraso para evitar sobrecarga do envio de dados
  }
}
