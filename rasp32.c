#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <time.h>

// Configurações do Wi-Fi
const char* ssid = "";       // Nome da sua rede Wi-Fi
const char* password = "";  // Senha da sua rede Wi-Fi

const char* serverUrl = "AQUI/api/data"; // COLE AQUI O SEU NGROK
const unsigned long intervaloArmazenamento = 250;  // Intervalo de armazenamento em milissegundos (0,5 segundos)
const unsigned long intervaloEnvio = 1000;  // Intervalo de envio em milissegundos (4 segundos)
const int maxRetries = 3; // Máximo de tentativas de reconexão HTTP

unsigned long lastStorageTime = 0;  // Último tempo de armazenamento
unsigned long lastSendTime = 0;     // Último tempo de envio

// Estrutura para armazenar os dados
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
  connectWiFi();
  syncTime();
}

void loop() {
  unsigned long currentTime = millis();

  // Verifica se é hora de armazenar os dados
  if (currentTime - lastStorageTime >= intervaloArmazenamento) {
    lastStorageTime = currentTime;

    // Lê os dados dos sensores (simulados)
    int sensorEsquerdo = analogRead(34); // Exemplo de leitura do sensor esquerdo
    int sensorDireito = analogRead(35);  // Exemplo de leitura do sensor direito
    float velocidade = 10.5;             // Exemplo de leitura da velocidade
    float distancia = 20.0;              // Exemplo de leitura da distância

    // Armazena os dados no array
    dadosArmazenados[dadosIndex].sensorEsquerdo = sensorEsquerdo;
    dadosArmazenados[dadosIndex].sensorDireito = sensorDireito;
    dadosArmazenados[dadosIndex].velocidade = velocidade;
    dadosArmazenados[dadosIndex].distancia = distancia;
    dadosArmazenados[dadosIndex].timestamp = getCurrentTime();

    // Incrementa o índice e verifica se chegou ao limite
    dadosIndex++;
    if (dadosIndex >= 4) {
      dadosIndex = 0;  // Reinicia o índice se chegou ao fim do array
    }
  }

  // Verifica se é hora de enviar os dados armazenados
  if (currentTime - lastSendTime >= intervaloEnvio) {
    lastSendTime = currentTime;

    // Cria um array para armazenar os dados a enviar
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

    // Envia os dados via HTTP POST para o servidor Node.js
    sendPostRequest(payload);
  }

  // Verifica a conexão WiFi e reconecta, se necessário
  checkWiFiConnection();
}

void connectWiFi() {
  Serial.print("Conectando ao WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado");
  Serial.print("Endereço IP: ");
  Serial.println(WiFi.localIP());
}

void syncTime() {
  configTime(0, 0, "pool.ntp.org", "time.nist.gov");  // Configura sincronização com NTP
  Serial.print("Sincronizando com o NTP");
  while (time(nullptr) < 8 * 3600 * 2) {
    Serial.print(".");
    delay(500);
  }
  Serial.println("\nNTP sincronizado.");
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

void checkWiFiConnection() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi desconectado! Tentando reconectar...");
    connectWiFi();
  }
}

String getCurrentTime() {
  time_t now = time(nullptr);
  struct tm* p_tm = localtime(&now);
  char buffer[20];
  sprintf(buffer, "%04d-%02d-%02d %02d:%02d:%02d",
          p_tm->tm_year + 1900, p_tm->tm_mon + 1, p_tm->tm_mday,
          p_tm->tm_hour, p_tm->tm_min, p_tm->tm_sec);
  return String(buffer);
}
