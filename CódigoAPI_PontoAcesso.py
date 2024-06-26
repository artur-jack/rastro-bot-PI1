from flask import Flask, request, jsonify
from flask_json import FlaskJSON, json_response
import pymysql
from datetime import datetime

app = Flask(__name__)
FlaskJSON(app)

# Configuração do banco de dados MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'ajlf2468',
    'database': 'carrodoovo'
}

# Função para configurar o banco de dados MySQL
def setup_database():
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            sensor_esquerdo INT,
            sensor_direito INT,
            velocidade FLOAT,
            distancia FLOAT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    connection.commit()
    cursor.close()
    connection.close()
    print('Conectado ao banco de dados MySQL')

# Função para inserir dados no banco de dados
def insert_data(data):
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    try:
        if 'timestamp' in data:
            cursor.execute('''
                INSERT INTO readings (sensor_esquerdo, sensor_direito, velocidade, distancia, timestamp)
                VALUES (%s, %s, %s, %s, %s)
            ''', (data['sensor_esquerdo'], data['sensor_direito'], data['velocidade'], data['distancia'], data['timestamp']))
        else:
            cursor.execute('''
                INSERT INTO readings (sensor_esquerdo, sensor_direito, velocidade, distancia)
                VALUES (%s, %s, %s, %s)
            ''', (data['sensor_esquerdo'], data['sensor_direito'], data['velocidade'], data['distancia']))
        connection.commit()
        print('Dados inseridos com sucesso no banco de dados')
    except Exception as e:
        print('Erro ao inserir dados:', e)
    finally:
        cursor.close()
        connection.close()

# Middleware para registrar a hora da requisição
@app.before_request
def before_request():
    request.request_time = datetime.now().isoformat()
    print(f'Requisição recebida em: {request.request_time}')

# Rota para receber os dados do dispositivo ESP
@app.route('/api/data', methods=['POST'])
def api_data():
    try:
        # Debug: Mostrar o corpo da requisição
        print(f"Corpo da requisição: {request.data}")
        data = request.get_json()
        
        # Debug: Mostrar dados recebidos
        print(f"Dados recebidos: {data}")
        
        if data is None:
            return jsonify({"error": "Nenhum dado recebido"}), 400

        for item in data:
            insert_data(item)

        return json_response(message='Processamento concluído!')
    except Exception as e:
        print(f"Erro ao processar requisição: {e}")
        return jsonify({"error": str(e)}), 400

# Inicia o servidor após configurar o banco de dados
if _name_ == '_main_':
    setup_database()
    app.run(host='0.0.0.0', port=3000)