#include <WiFi.h>
#include <WebSocketsServer.h>

// Configurações do ponto de acesso
const char* ssid = "ESP32_AP";
const char* password = "12345678";
const int ledPin = 2; // Pino GPIO 2 no ESP32 para o LED

WebSocketsServer webSocket = WebSocketsServer(81);

void setup() {
  Serial.begin(115200);

  // Inicializa o ponto de acesso
  WiFi.softAP(ssid, password);
  Serial.print("IP do ponto de acesso: ");
  Serial.println(WiFi.softAPIP());

  // Inicializa o servidor WebSocket
  webSocket.begin();
  webSocket.onEvent(webSocketEvent);

  // Configura o pino do LED como saída
  pinMode(ledPin, OUTPUT);
}

void loop() {
  // WebSocket loop
  webSocket.loop();

  // Blink do led
  digitalWrite(ledPin, HIGH); 
  webSocket.broadcastTXT("LED is ON");
  delay(3000); 

  digitalWrite(ledPin, LOW);
  webSocket.broadcastTXT("LED is OFF");
  delay(3000); 
  
  // Outras tarefas podem ser adicionadas aqui
}

void webSocketEvent(uint8_t num, WStype_t type, uint8_t *payload, size_t length) {
  switch(type) {
    case WStype_DISCONNECTED:
      Serial.printf("[%u] Disconnected!\n", num);
      break;
    case WStype_CONNECTED: {
      IPAddress ip = webSocket.remoteIP(num);
      Serial.printf("[%u] Conectado de %s\n", num, ip.toString().c_str());
    }
      break;
    case WStype_TEXT:
      Serial.printf("[%u] Texto recebido: %s\n", num, payload);
      break;
    case WStype_ERROR:
      Serial.printf("[%u] Erro\n", num);
      break;
  }
}
