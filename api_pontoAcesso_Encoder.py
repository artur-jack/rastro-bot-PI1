from flask import Flask, request
from flask_json import FlaskJSON, json_response
import pymysql
from datetime import datetime
import random
from flask_cors import CORS
from flask import jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)
FlaskJSON(app)
CORS(app)

# Configuração do banco de dados MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456789',
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
        distance_dir = speed_dir * (data['timeDIR'] / 1000.0)  # m
        distance_esq = speed_esq * (data['timeESQ'] / 1000.0)  # m

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
    tempo_total = (fim_corrida - inicio_corrida).total_seconds()
    tempo_total_str = str(datetime.utcfromtimestamp(tempo_total).strftime('%H:%M:%S'))  # Tempo total em horas:minutos:segundos
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
        ''', (fim_corrida, tempo_total_str, trajeto_total, consumo_medio, aceleracao_media, velocidade_media, corrida_id))
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

# Rota para buscar uma corrida específica pelo ID
@app.route('/api/corrida/<int:corrida_id>', methods=['GET'])
def get_corrida(corrida_id):
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        # Utiliza o índice para buscar a corrida pelo ID
        cursor.execute('SELECT * FROM corridas WHERE id = %s', (corrida_id,))
        corrida = cursor.fetchone()

        if corrida:
            keys = [desc[0] for desc in cursor.description]
            corrida_dict = dict(zip(keys, corrida))
            return json_response(data=corrida_dict)
        else:
            return json_response(status=404, message=f'Corrida com ID {corrida_id} não encontrada.')
    except Exception as e:
        print(f'Erro ao buscar corrida com ID {corrida_id}:', e)
        return json_response(status=500, message=f'Erro ao buscar corrida com ID {corrida_id}.')
    finally:
        cursor.close()
        connection.close()

@app.route('/api/real_time', methods=['GET'])
def get_first_corrida():
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT * FROM metrics ORDER BY id DESC LIMIT 1')
        first_corrida = cursor.fetchone()
        if first_corrida:
            keys = [desc[0] for desc in cursor.description]
            first_corrida_dict = dict(zip(keys, first_corrida))
            data = {
                "data": first_corrida_dict,
                "status": 200
            }
            return jsonify(data)
        else:
            return jsonify({"status": 404, "message": 'Nenhuma corrida encontrada.'})
    except Exception as e:
        print('Erro ao buscar primeira corrida:', e)
        return jsonify({"status": 500, "message": 'Erro ao buscar primeira corrida.'})
    finally:
        cursor.close()
        connection.close()

'''
# Função para buscar uma corrida específica pelo ID e os readings(dados das rodas) correspondentes
@app.route('/api/corrida/<int:corrida_id>/readings', methods=['GET'])
def get_corrida_readings(corrida_id):
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        # Busca a corrida pelo ID
        cursor.execute('SELECT * FROM corridas WHERE id = %s', (corrida_id,))
        corrida = cursor.fetchone()

        if not corrida:
            return json_response(status=404, message=f'Corrida com ID {corrida_id} não encontrada.')

        # Extrai os tempos de início e fim da corrida
        corrida_id, inicio_corrida, fim_corrida, tempo_total, trajeto_total, consumo_medio, aceleracao_media, velocidade_media = corrida

        # Busca os readings dentro do intervalo de tempo da corrida
        cursor.execute('SELECT * FROM readings WHERE timestamp BETWEEN %s AND %s', (inicio_corrida, fim_corrida))
        readings = cursor.fetchall()

        # Converte os resultados em dicionários
        corrida_dict = {
            'id': corrida_id,
            'inicio': inicio_corrida,
            'fim': fim_corrida,
            'tempo_total': tempo_total,
            'trajeto_total': trajeto_total,
            'consumo_medio': consumo_medio,
            'aceleracao_media': aceleracao_media,
            'velocidade_media': velocidade_media
        }

        readings_list = []
        readings_keys = ['id', 'speed_dir', 'speed_esq', 'distance_dir', 'distance_esq', 'timestamp']
        for reading in readings:
            readings_list.append(dict(zip(readings_keys, reading)))

        return json_response(data={'corrida': corrida_dict, 'readings': readings_list})

    except Exception as e:
        print(f'Erro ao buscar readings da corrida com ID {corrida_id}:', e)
        return json_response(status=500, message=f'Erro ao buscar readings da corrida com ID {corrida_id}.')
    finally:
        cursor.close()
        connection.close()
'''
# Função para calcular as posições x e y do carrinho
def calcular_posicoes(dataframe):
    x = 0.0
    y = 0.0
    theta = 0.0  # Ângulo inicial (em radianos)
    
    posicoes = []

    for i in range(1, len(dataframe)):
        # Velocidades das rodas direita e esquerda
        speed_dir = dataframe['speed_dir'].iloc[i]
        speed_esq = dataframe['speed_esq'].iloc[i]
        
        # Distâncias percorridas pelas rodas direita e esquerda
        distance_dir = dataframe['distance_dir'].iloc[i]
        distance_esq = dataframe['distance_esq'].iloc[i]
        
        # Intervalo de tempo entre as amostras
        delta_time = (dataframe['timestamp'].iloc[i] - dataframe['timestamp'].iloc[i-1]).total_seconds()
        
        # Calculando a diferença de distância entre as rodas
        delta_distance = (distance_dir + distance_esq) / 2.0
        
        # Atualizando as posições x e y
        x += delta_distance * np.cos(theta)
        y += delta_distance * np.sin(theta)
        
        # Atualizando o ângulo theta com base nas diferenças de velocidade
        delta_theta = ((speed_dir - speed_esq) * delta_time) / 0.1  # Supondo um comprimento de base de 0.1 (em metros)
        theta += delta_theta
        
        posicoes.append((x, y))

    return posicoes

# Função para buscar uma corrida específica pelo ID e os readings correspondentes
@app.route('/api/corrida/<int:corrida_id>/readings', methods=['GET'])
def get_corrida_readings(corrida_id):
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        # Busca a corrida pelo ID
        cursor.execute('SELECT * FROM corridas WHERE id = %s', (corrida_id,))
        corrida = cursor.fetchone()

        if not corrida:
            return json_response(status=404, message=f'Corrida com ID {corrida_id} não encontrada.')

        # Extrai os tempos de início e fim da corrida
        corrida_id, inicio_corrida, fim_corrida, tempo_total, trajeto_total, consumo_medio, aceleracao_media, velocidade_media = corrida

        # Busca os readings dentro do intervalo de tempo da corrida
        cursor.execute('SELECT * FROM readings WHERE timestamp BETWEEN %s AND %s', (inicio_corrida, fim_corrida))
        readings = cursor.fetchall()

        if not readings:
            return json_response(status=404, message=f'Nenhum reading encontrado para a corrida com ID {corrida_id}.')

        # Converte os resultados em dicionários
        corrida_dict = {
            'id': corrida_id,
            'inicio': inicio_corrida,
            'fim': fim_corrida,
            'tempo_total': tempo_total,
            'trajeto_total': trajeto_total,
            'consumo_medio': consumo_medio,
            'aceleracao_media': aceleracao_media,
            'velocidade_media': velocidade_media
        }

        readings_list = []
        readings_keys = ['id', 'speed_dir', 'speed_esq', 'distance_dir', 'distance_esq', 'timestamp']
        for reading in readings:
            readings_list.append(dict(zip(readings_keys, reading)))

        # Converte readings_list para um DataFrame para cálculo das posições
        df_readings = pd.DataFrame(readings_list)
        df_readings['timestamp'] = pd.to_datetime(df_readings['timestamp'])

        # Calcula as posições x e y
        posicoes = calcular_posicoes(df_readings)

        # Cria uma lista de dicionários contendo apenas x e y
        posicoes_list = [{'x': pos[0], 'y': pos[1]} for pos in posicoes]

        return json_response(data={'corrida': corrida_dict, 'posicoes': posicoes_list})

    except Exception as e:
        print(f'Erro ao buscar readings da corrida com ID {corrida_id}:', e)
        return json_response(status=500, message=f'Erro ao buscar readings da corrida com ID {corrida_id}.')
    finally:
        cursor.close()
        connection.close()


    

# Inicia o servidor após configurar o banco de dados
if __name__ == '__main__':
    setup_database()
    app.run(host='0.0.0.0', port=3000)
