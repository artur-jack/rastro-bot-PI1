#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// Configurações do ponto de acesso
const char* ssid = "ESP32_AP";
const char* password = "12345678";
const char* serverUrl = "http://192.168.4.2:3000/api/data";  // Atualize com o IP correto do notebook

const unsigned long intervaloArmazenamento = 200; // Intervalo de armazenamento em milissegundos (0,5 segundos)
const unsigned long intervaloEnvio = 800;       // Intervalo de envio em milissegundos (2 segundos)
const int maxRetries = 3;                        // Máximo de tentativas de reconexão HTTP

unsigned long lastStorageTime = 0;  // Último tempo de armazenamento
unsigned long lastSendTime = 0;     // Último tempo de envio

struct Dados {
  int sensorEsquerdo;
  int sensorDireito;
  float velocidade;
  float distancia;
  String timestamp;
};

Dados dadosArmazenados[4];  // Array para armazenar até 4 conjuntos de dados
int dadosIndex = 0;  // Índice para controlar onde armazenar os dados

HTTPClient http;

void setup() {
  Serial.begin(115200);
  Serial.println();

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

    // Simulação de leitura de dados dos sensores
    int sensorEsquerdo = random(0, 100);  // Exemplo de leitura do sensor esquerdo
    int sensorDireito = random(0, 100);   // Exemplo de leitura do sensor direito
    float velocidade = random(0, 50) / 10.0;  // Exemplo de leitura da velocidade
    float distancia = random(0, 100);         // Exemplo de leitura da distância

    // Armazena os dados no array
    dadosArmazenados[dadosIndex].sensorEsquerdo = sensorEsquerdo;
    dadosArmazenados[dadosIndex].sensorDireito = sensorDireito;
    dadosArmazenados[dadosIndex].velocidade = velocidade;
    dadosArmazenados[dadosIndex].distancia = distancia;
    dadosArmazenados[dadosIndex].timestamp = "2024-06-26 10:10:10";  // Use um timestamp fixo

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
      obj["sensor_esquerdo"] = dadosArmazenados[i].sensorEsquerdo;
      obj["sensor_direito"] = dadosArmazenados[i].sensorDireito;
      obj["velocidade"] = dadosArmazenados[i].velocidade;
      obj["distancia"] = dadosArmazenados[i].distancia;
      obj["timestamp"] = dadosArmazenados[i].timestamp;
    }

    // Serializa o documento JSON em uma string
    String payload;
    serializeJson(doc, payload);
    Serial.print("Payload enviado: ");
    Serial.println(payload);

    // Envia os dados via HTTP POST para o servidor Flask
    sendPostRequest(payload);
  }
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
