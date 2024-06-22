import serial
from datetime import datetime
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import pymysql
import json

pymysql.install_as_MySQLdb()

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://leandro:123456789@localhost/rastrobotdb2'
db = SQLAlchemy(app)

# Definir a classe do modelo do banco de dados
class esp32_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_esquerdo = db.Column(db.String(100))
    sensor_direito = db.Column(db.String(100))
    velocidade = db.Column(db.Float, default=0.0)
    distancia = db.Column(db.Float, default=0.0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


    def to_json(self):
        return {"id": self.id, "sensor_esquerdo": self.sensor_esquerdo, 
                "sensor_direito": self.sensor_direito, "velocidade": self.velocidade,
                "distancia": self.distancia, "timestamp": self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

# Criar tabelas se ainda não existirem
with app.app_context():
    db.create_all()

# Função para verificar os dados recebidos pela porta serial Bluetooth e adicionar ao banco de dados
def verificar_e_inserir_dados_ble():
    with app.app_context():
        # Configuração da porta serial Bluetooth
        porta_serial = serial.Serial('COM8', 115200)  # Substitua 'COM8' pelo nome da porta serial Bluetooth e 115200 pela mesma taxa de baud do código do ESP32
        print("Espere uma conexão Bluetooth...")

        while True:
            # Verificar se há dados disponíveis na porta serial
            if porta_serial.in_waiting > 0:
                # Ler os dados recebidos da porta serial
                dados_ble = porta_serial.readline().decode().strip()
                print("Dados recebidos via Bluetooth:", dados_ble)
                
                # Converter os dados para JSON
                dados_ble_json = json.loads(dados_ble)

                # Inserir os dados no banco de dados
                try:
                    timestamp = datetime.strptime(dados_ble_json["current_time"], '%Y-%m-%d %H:%M:%S')
                    dados = esp32_data(sensor_esquerdo=dados_ble_json["sensor_esquerdo"],
                                       sensor_direito=dados_ble_json["sensor_direito"],
                                       velocidade=dados_ble_json["velocidade"],
                                       distancia=dados_ble_json["distancia"],
                                       timestamp=timestamp)
                    db.session.add(dados)
                    db.session.commit()
                    print("Dados inseridos no banco de dados com sucesso!")
                except Exception as e:
                    print('Erro ao inserir dados no banco de dados:', e)



# Rota padrão
@app.route('/')
def index():
    return '<h1>Hello, World!<h1>'

# Rota para receber dados via POST e inseri-los no banco de dados
@app.route("/dadoscad", methods=["POST"])
def cria_dados():
    body = request.get_json()

    try:
        timestamp = datetime.strptime(body["timestamp"], '%Y-%m-%d %H:%M:%S')

        dados = esp32_data(sensor_esquerdo=body["sensor_esquerdo"], sensor_direito=body["sensor_direito"],
                           velocidade=body["velocidade"], distancia=body["distancia"], timestamp=timestamp)
        db.session.add(dados)
        db.session.commit()
        return gera_response(201, "dados", dados.to_json(), "Criado com sucesso")
    
    except Exception as e:
        print('Erro:', e)
        return gera_response(400, "dados", {}, "Erro ao cadastrar")

# Função auxiliar para gerar uma resposta JSON
def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if mensagem:
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")

# Iniciar a execução da aplicação Flask
if __name__ == '__main__':
    # Iniciar uma thread para verificar e inserir dados BLE
    import threading
    ble_thread = threading.Thread(target=verificar_e_inserir_dados_ble)
    ble_thread.start()
    
    # Iniciar a aplicação Flask
    app.run()

#conectar mysql shell: \connect nome_de_usuario@host:3306