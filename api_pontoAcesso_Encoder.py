from flask import Flask, request
from flask_json import FlaskJSON, json_response
import pymysql
from datetime import datetime, timedelta
import random

app = Flask(__name__)
FlaskJSON(app)

# Configuração do banco de dados MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'ajlf2468',
    'database': 'carrodoovo'
}

# Variáveis de estado da corrida
corrida_iniciada = False
corrida_id = None
inicio_corrida = None

# Distância total percorrida pelo carrinho
total_distance_dir = 0.0
total_distance_esq = 0.0

# Função para configurar o banco de dados MySQL
def setup_database():
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            speed_dir FLOAT,
            speed_esq FLOAT,
            distance_dir FLOAT,
            distance_esq FLOAT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metrics (
            id INT AUTO_INCREMENT PRIMARY KEY,
            speed FLOAT,
            total_distance FLOAT,
            acceleration FLOAT,
            consumption FLOAT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS corridas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            inicio DATETIME,
            fim DATETIME,
            tempo_total VARCHAR(8),
            trajeto_total FLOAT,
            consumo_medio FLOAT,
            aceleracao_media FLOAT,
            velocidade_media FLOAT
        )
    ''')
    connection.commit()
    cursor.close()
    connection.close()
    print('Conectado ao banco de dados MySQL')

# Função para calcular e formatar tempo total
def calcular_tempo_total(inicio, fim):
    tdelta = fim - inicio
    total_seconds = int(tdelta.total_seconds())
    
    # Convertendo para formato hh:mm:ss
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    tempo_total = f"{hours:02}:{minutes:02}:{seconds:02}"
    return tempo_total

# Função para calcular as métricas e inserir dados no banco de dados
def insert_data(data):
    global total_distance_dir, total_distance_esq

    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    try:
        # Parâmetros do carrinho
        wheel_diameter = 0.1  # Diâmetro da roda em metros (ajustar conforme necessário)
        pulse_per_revolution = 20  # Pulsos por rotação (ajustar conforme necessário)
        circumference = wheel_diameter * 3.14159  # Circunferência da roda

        # Exibe o conteúdo de 'data' para depuração
        print(f'Dados recebidos para inserção: {data}')

        # Calcula as métricas
        speed_dir = (circumference / pulse_per_revolution) / (data['timeDIR'] / 1000.0)  # m/s
        speed_esq = (circumference / pulse_per_revolution) / (data['timeESQ'] / 1000.0)  # m/s
        distance_dir = data['pulseCountDIR'] * (circumference / pulse_per_revolution)  # m
        distance_esq = data['pulseCountESQ'] * (circumference / pulse_per_revolution)  # m

        # Atualiza a distância total percorrida pelo carrinho
        total_distance_dir += distance_dir
        total_distance_esq += distance_esq

        # Média da velocidade e distância
        speed = (speed_dir + speed_esq) / 2
        total_distance = (total_distance_dir + total_distance_esq) / 2

        # Cálculo da aceleração (simplificação para exemplo)
        acceleration = speed / (data['timeDIR'] / 1000.0)

        # Consumo aleatório para exemplo
        consumption = random.uniform(0.1, 1.0)

        # Insere os dados calculados na tabela readings
        cursor.execute('''
            INSERT INTO readings (speed_dir, speed_esq, distance_dir, distance_esq, timestamp)
            VALUES (%s, %s, %s, %s, %s)
        ''', (speed_dir, speed_esq, distance_dir, distance_esq, datetime.now()))
        
        # Insere os dados calculados na tabela metrics
        cursor.execute('''
            INSERT INTO metrics (speed, total_distance, acceleration, consumption, timestamp)
            VALUES (%s, %s, %s, %s, %s)
        ''', (speed, total_distance, acceleration, consumption, datetime.now()))
        
        connection.commit()
        print('Dados inseridos com sucesso no banco de dados')
    except Exception as e:
        print('Erro ao inserir dados:', e)
    finally:
        cursor.close()
        connection.close()

# Função para iniciar uma corrida
@app.route('/api/start_corrida', methods=['POST'])
def start_corrida():
    global corrida_iniciada, corrida_id, inicio_corrida

    corrida_iniciada = True
    inicio_corrida = datetime.now()

    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    try:
        cursor.execute('''
            INSERT INTO corridas (inicio)
            VALUES (%s)
        ''', (inicio_corrida,))
        corrida_id = cursor.lastrowid
        connection.commit()
        print(f'Corrida iniciada com ID: {corrida_id}')
    except Exception as e:
        print('Erro ao iniciar corrida:', e)
    finally:
        cursor.close()
        connection.close()

    return json_response(message='Corrida iniciada!', corrida_id=corrida_id)

# Função para finalizar uma corrida
@app.route('/api/end_corrida', methods=['POST'])
def end_corrida():
    global corrida_iniciada, corrida_id, inicio_corrida, total_distance_dir, total_distance_esq

    if not corrida_iniciada:
        return json_response(status=400, message='Nenhuma corrida em andamento.')

    fim_corrida = datetime.now()
    tempo_total = calcular_tempo_total(inicio_corrida, fim_corrida)
    trajeto_total = (total_distance_dir + total_distance_esq) / 2  # Distância total média

    # Calcula médias das métricas
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT AVG(speed), AVG(acceleration), AVG(consumption) FROM metrics')
        result = cursor.fetchone()
        velocidade_media, aceleracao_media, consumo_medio = result

        cursor.execute('''
            UPDATE corridas
            SET fim=%s, tempo_total=%s, trajeto_total=%s, consumo_medio=%s, aceleracao_media=%s, velocidade_media=%s
            WHERE id=%s
        ''', (fim_corrida, tempo_total, trajeto_total, consumo_medio, aceleracao_media, velocidade_media, corrida_id))
        connection.commit()
        print(f'Corrida finalizada com ID: {corrida_id}')
    except Exception as e:
        print('Erro ao finalizar corrida:', e)
    finally:
        cursor.close()
        connection.close()

    corrida_iniciada = False
    corrida_id = None
    inicio_corrida = None
    total_distance_dir = 0.0
    total_distance_esq = 0.0

    return json_response(message='Corrida finalizada!', corrida_id=corrida_id)

# Middleware para registrar a hora da requisição
@app.before_request
def before_request():
    request.request_time = datetime.now().isoformat()
    print(f'Requisição recebida em: {request.request_time}')

# Rota para receber os dados do dispositivo ESP
@app.route('/api/data', methods=['POST'])
def api_data():
    if not corrida_iniciada:
        return json_response(status=400, message='Corrida não iniciada.')

    data = request.json  # Recebe o array de objetos JSON enviado pelo ESP32

    # Exibe o conteúdo de 'data' para depuração
    print(f'Dados recebidos: {data}')

    # Envie uma resposta de sucesso imediatamente
    json_response(message='Dados recebidos, processamento em andamento!')

    # Verifica se 'data' é uma lista ou um único objeto e processa adequadamente
    if isinstance(data, list):
        for item in data:
            insert_data(item)
    else:
        insert_data(data)

    return json_response(message='Processamento concluído!')

# Inicia o servidor após configurar o banco de dados
if __name__ == '__main__':
    setup_database()
    app.run(host='0.0.0.0', port=3000)
