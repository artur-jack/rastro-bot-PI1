# Rodar API

Os arquivos usados são:

- ESP_pontoAcesso_Encoder.c
- api_pontoAcesso_Encoder.py
  
## Descrição

Esta API foi desenvolvida para monitorar as métricas de um carrinho autônomo. Ela permite iniciar e finalizar corridas, bem como armazenar dados de velocidade, distância, aceleração e consumo em um banco de dados MySQL.

## Requisitos

- Flask
- Flask-JSON
- PyMySQL
- MySQL Server

## Instalação

1. Clone o repositório:

2. Instale as dependencias
   ```bash
    pip install Flask Flask-JSON PyMySQL
  
3. Configure o banco no código da api
   ```bash
    db_config = {
    'host': 'localhost',
    'user': 'seu_usuario',
    'password': 'sua_senha',
    'database': 'carrodoovo'
    }

3.1 Crie uma base de dados no banco mysql chamada carrodoovo
  ```bash
  CREATE DATABASE carrodoovo;
  ```
4. Rode a api. Pode ser pelo botão do vscode ou:
   ```bash
    python app.py

5. Quando a ESP32 já estiver ligada com o código rodando conecte no WIFI da ESP

WIFI: ESP32_AP
SENHA: 12345678

6. Use a requisição abaixo para começar uma corrida via CMD.
   ```bash
    curl -X POST http://192.168.4.2:3000/api/start_corrida

7. Use a requisição abaixo no cmd quando quiser encerrar a corrida:
    ```bash
    curl -X POST http://192.168.4.2:3000/api/end_corrida

# Configurar a ESP32

- Baixe e instale todas as bibliotecas usadas no código da ESP, compile e envia para a placa.
- Após isso ela ficara printando 'Aguardando' no monitor serial até alguém conectar em seu ponto de acesso (WIFI). Caso conecte no wifi e a API não esteja rodando ou não esteja conseguindo se conectar com a API, a ESP deve dar conection refused.

# Cálculos e Unidades

# Cálculos e Unidades

## Velocidade (speed_dir, speed_esq)
- **Cálculo**: `(circumference / pulse_per_revolution) / (time / 1000.0)`
- **Unidade**: metros por segundo (m/s)

## Distância (distance_dir, distance_esq)
- **Cálculo**: `pulseCount * (circumference / pulse_per_revolution)`
- **Unidade**: metros (m)

## Aceleração (acceleration)
- **Cálculo**: `speed / (time / 1000.0)` (simplificação)
- **Unidade**: metros por segundo ao quadrado (m/s²)

## Consumo (consumption)
- **Cálculo**: Gerado aleatoriamente para exemplo
- **Unidade**: unidade arbitrária

## Tempo Total (tempo_total)
- **Cálculo**: `fim_corrida - inicio_corrida`
- **Unidade**: horas:minutos (hh:mm)

# Estrutura do Banco de Dados

## Tabela readings

| Campo         | Tipo    | Descrição               |
| ------------- | ------- | ----------------------- |
| id            | INT     | Identificador único     |
| speed_dir     | FLOAT   | Velocidade direita      |
| speed_esq     | FLOAT   | Velocidade esquerda     |
| distance_dir  | FLOAT   | Distância direita       |
| distance_esq  | FLOAT   | Distância esquerda      |
| timestamp     | DATETIME| Data e hora da leitura  |

## Tabela metrics

| Campo          | Tipo    | Descrição               |
| id             | INT     | Identificador único     |
| speed          | FLOAT   | Velocidade média        |
| total_distance | FLOAT   | Distância total         |
| acceleration   | FLOAT   | Aceleração              |
| consumption    | FLOAT   | Consumo                 |
| timestamp      | DATETIME| Data e hora da métrica  |

## Tabela corridas

| Campo             | Tipo      | Descrição                    |
| ----------------- | --------- | ---------------------------- |
| id                | INT       | Identificador único          |
| inicio            | DATETIME  | Início da corrida            |
| fim               | DATETIME  | Fim da corrida               |
| tempo_total       | VARCHAR(8)| Tempo total da corrida (hh:mm)|
| trajeto_total     | FLOAT     | Distância total da corrida   |
| consumo_medio     | FLOAT     | Consumo médio                |
| aceleracao_media  | FLOAT     | Aceleração média             |
| velocidade_media  | FLOAT     | Velocidade média             |
