#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// Configurações do ponto de acesso
const char* ssid = "ESP32_AP";
const char* password = "12345678";
const char* serverUrl = "http://192.168.4.2:3000/api/data";  // Atualize com o IP correto do notebook

const unsigned long intervaloArmazenamento = 200;  // Intervalo de armazenamento em milissegundos (0,2 segundos)
const unsigned long intervaloEnvio = 800;  // Intervalo de envio em milissegundos (0,8 segundos)
const int maxRetries = 3;  // Máximo de tentativas de reconexão HTTP

// Variáveis de contagem de pulsos
volatile int pulseCountDIR = 0;
volatile int pulseCountESQ = 0;

// Buffers para armazenar dados
struct Dados {
  int pulseCountDIR;
  int pulseCountESQ;
  unsigned long timeDIR;
  unsigned long timeESQ;
};

Dados dadosArmazenados[4];  // Array para armazenar até 4 conjuntos de dados
int dadosIndex = 0;  // Índice para controlar onde armazenar os dados

unsigned long lastStorageTime = 0;  // Último tempo de armazenamento
unsigned long lastSendTime = 0;  // Último tempo de envio

HTTPClient http;

void setup() {
  Serial.begin(115200);

  // Inicializa o ponto de acesso
  WiFi.softAP(ssid, password);
  Serial.print("IP do ponto de acesso: ");
  Serial.println(WiFi.softAPIP());

  // Aguarda conexão de um cliente
  while (WiFi.softAPgetStationNum() == 0) {
    Serial.println("Aguardando conexão do cliente...");
    delay(1000);
  }
  Serial.println("Cliente conectado.");
}

void loop() {
  unsigned long currentTime = millis();

  // Verifica se é hora de armazenar os dados
  if (currentTime - lastStorageTime >= intervaloArmazenamento) {
    lastStorageTime = currentTime;

    // Simula dados fictícios de pulsos e tempos
    pulseCountDIR = random(100, 200);
    pulseCountESQ = random(100, 200);
    unsigned long mockTimeDIR = random(50, 100);
    unsigned long mockTimeESQ = random(50, 100);

    // Armazena os dados no array
    dadosArmazenados[dadosIndex].pulseCountDIR = pulseCountDIR;
    dadosArmazenados[dadosIndex].pulseCountESQ = pulseCountESQ;
    dadosArmazenados[dadosIndex].timeDIR = mockTimeDIR;
    dadosArmazenados[dadosIndex].timeESQ = mockTimeESQ;

    // Incrementa o índice e verifica se chegou ao limite
    dadosIndex++;
    if (dadosIndex >= 4) {
      dadosIndex = 0;  // Reinicia o índice se chegou ao fim do array
    }
  }

  // Verifica se é hora de enviar os dados armazenados
  if (currentTime - lastSendTime >= intervaloEnvio) {
    lastSendTime = currentTime;

    // Cria um objeto JSON para armazenar os dados
    StaticJsonDocument<1024> doc;
    JsonArray array = doc.to<JsonArray>();

    // Adiciona os dados armazenados ao JSON
    for (int i = 0; i < 4; i++) {
      JsonObject obj = array.createNestedObject();
      obj["pulseCountDIR"] = dadosArmazenados[i].pulseCountDIR;
      obj["pulseCountESQ"] = dadosArmazenados[i].pulseCountESQ;
      obj["timeDIR"] = dadosArmazenados[i].timeDIR;
      obj["timeESQ"] = dadosArmazenados[i].timeESQ;
    }

    // Serializa o documento JSON em uma string
    String payload;
    serializeJson(doc, payload);
    Serial.print("Payload enviado: ");
    Serial.println(payload);

    sendPostRequest(payload);
  }

  delay(10);
}

void sendPostRequest(String payload) {
  int attempts = 0;
  bool success = false;

  while (attempts < maxRetries && !success) {
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    int httpResponseCode = http.POST(payload);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.print("Resposta do servidor: ");
      Serial.println(response);
      success = true;
    } else {
      Serial.print("Erro na solicitação HTTP: ");
      Serial.println(httpResponseCode);
      Serial.print("Mensagem de erro: ");
      Serial.println(http.errorToString(httpResponseCode));
      attempts++;
      delay(1000);  // Aguarda um segundo antes de tentar novamente
    }

    http.end();
  }

  if (!success) {
    Serial.println("Falha ao enviar dados após múltiplas tentativas.");
  }
}
