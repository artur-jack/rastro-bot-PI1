#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>

// Definições dos pinos dos motores
#define MOTOR_ESQUERDO_PIN_A 2  // Pino A do motor esquerdo
#define MOTOR_ESQUERDO_PIN_B 3  // Pino B do motor esquerdo
#define MOTOR_DIREITO_PIN_A 4   // Pino A do motor direito
#define MOTOR_DIREITO_PIN_B 5   // Pino B do motor direito

// WiFi credentials
const char* ssid = "NOME DA REDE WIFI";
const char* password = "SENHA DA REDE WIFI";

// Endereço da API
const char* apiUrl = "link gerado pelo ngrok/api/esp32/";

// Função de inicialização
void setup() {
  pinMode(MOTOR_ESQUERDO_PIN_A, OUTPUT);
  pinMode(MOTOR_ESQUERDO_PIN_B, OUTPUT);
  pinMode(MOTOR_DIREITO_PIN_A, OUTPUT);
  pinMode(MOTOR_DIREITO_PIN_B, OUTPUT);
  
  Serial.begin(9600);

  // Inicializa a conexão Wi-Fi
  Serial.print("Conectando ao WiFi ");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" conectado");
}

// Função principal
void loop() {
  // Gerar dados simulados
  int sensorEsquerdo = random(2);
  int sensorDireito = random(2);
  float velocidade_inst = random(50, 150); // Velocidade entre 50 e 150 unidades por segundo
  float distancia_parcial = random(1000); // Distância entre 0 e 1000 unidades

  // Envia os dados simulados para a API
  enviarDadosAPI(sensorEsquerdo, sensorDireito, velocidade_inst, distancia_parcial);
  delay(1000); // Espera um segundo antes de enviar os dados novamente
}

// Função para enviar dados simulados para a API
void enviarDadosAPI(int sensorEsquerdo, int sensorDireito, float velocidade_inst, float distancia_parcial) {
  // Cria um objeto HTTPClient
  HTTPClient http;
  
  // Adiciona o cabeçalho "Content-Type"
  http.begin(apiUrl);
  http.addHeader("Content-Type", "application/json");
  
  // Cria o JSON com os dados simulados
  String jsonData = String("{\"sensor_esquerdo\": ") + sensorEsquerdo + String(", \"sensor_direito\": ") + sensorDireito + String(", \"velocidade\": ") + velocidade_inst + String(", \"distancia\": ") + distancia_parcial + String("}");

  
  // Envia a requisição POST com os dados JSON
  int httpResponseCode = http.POST(jsonData);
  
  // Verifica o código de resposta
  if (httpResponseCode > 0) {
    Serial.print("Requisicao POST bem-sucedida. Codigo de resposta: ");
    Serial.println(httpResponseCode);
  } else {
    Serial.print("Erro na requisicao POST. Codigo de resposta: ");
    Serial.println(httpResponseCode);
  }
  
  // Libera os recursos
  http.end();
}

