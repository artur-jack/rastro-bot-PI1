import serial
from datetime import datetime, time, timedelta
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import pymysql
import json
import threading
from sqlalchemy import func

pymysql.install_as_MySQLdb()

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://leandro:123456789@localhost/teste'
db = SQLAlchemy(app)

# Definir a classe do modelo do banco de dados
class DADOS_CORRIDA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    distancia = db.Column(db.Float, default=0.0)
    velocidade = db.Column(db.Float, default=0.0)
    aceleracao = db.Column(db.Float, default=0.0)
    consumo = db.Column(db.Float, default=0.0)
    tempoColeta = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    idcorri = db.Column(db.Integer, default=1)  # Nova coluna

    def to_json(self):
        return {
            "id": self.id, 
            "distancia": self.distancia, 
            "velocidade": self.velocidade,
            "aceleracao": self.aceleracao,
            "consumo": self.consumo,
            "tempoColeta": self.tempoColeta.strftime('%Y-%m-%d %H:%M:%S'),
            "idcorri": self.idcorri  
        }

# Definir a classe do modelo do banco de dados
class CORRIDA(db.Model):
    idCorrida = db.Column(db.Integer, primary_key=True)
    inicio = db.Column(db.Time, default="00:00:00")
    fim = db.Column(db.Time, default="00:00:00")
    tempoTotal = db.Column(db.Time, default="00:00:00")
    trajetoTotal = db.Column(db.Float, default=0.0)
    consumoMedia = db.Column(db.Float, default=0.0)
    aceleracaoMedia = db.Column(db.Float, default=0.0)
    velocidadeMedia = db.Column(db.Float, default=0.0)

# Criar tabelas se ainda não existirem
with app.app_context():
    db.create_all()

# Variável para controlar a coleta de dados
collecting_data = True  # Iniciar como True
dados_pendentes = []  # Lista para armazenar os dados recebidos durante o "STOP"
inseriu_corrida = False  # Flag para controlar se já inseriu a corrida após parar
idcorri_incremento = 1  # Variável para controlar o incremento de idcorri

# Função para verificar os dados recebidos pela porta serial Bluetooth e adicionar ao banco de dados
def verificar_e_inserir_dados_ble():
    global collecting_data, dados_pendentes, inseriu_corrida, idcorri_incremento
    collecting_data_prev = False  # Variável para armazenar o estado anterior de coleta

    with app.app_context():  # Entrar no contexto da aplicação Flask
        # Configuração da porta serial Bluetooth
        porta_serial = serial.Serial('COM8', 115200)  # Substitua 'COM8' pelo nome da porta serial Bluetooth e 115200 pela mesma taxa de baud do código do ESP32
        print("Espere uma conexão Bluetooth...")

        while True:
            if collecting_data:
                # Se o estado anterior era 'STOP', limpar dados pendentes
                if not collecting_data_prev:
                    dados_pendentes = []
                
                # Marcar o estado anterior como coleta ativa
                collecting_data_prev = True

               
                # Verificar se há dados disponíveis na porta serial
                if porta_serial.in_waiting > 0:
                    # Ler os dados recebidos da porta serial
                    dados_ble = porta_serial.readline().decode().strip()
                    print("Dados recebidos via Bluetooth:", dados_ble)
                    
                    # Converter os dados para JSON
                    dados_ble_json = json.loads(dados_ble)

                    # Inserir os dados na tabela DADOS_CORRIDA apenas se collecting_data ainda for True
                    if collecting_data:
                        try:
                            # Usar a data e hora atuais do sistema
                            tempoColeta = datetime.now()
                            
                            dados = DADOS_CORRIDA(
                                distancia=dados_ble_json["distancia"], 
                                velocidade=dados_ble_json["velocidade"],
                                aceleracao=dados_ble_json["aceleracao"],
                                consumo=dados_ble_json["consumo"],
                                tempoColeta=tempoColeta,
                                idcorri=idcorri_incremento)  # Incrementar idcorri
                            
                            db.session.add(dados)
                            db.session.commit()
                            print("Dados inseridos na tabela DADOS_CORRIDA com sucesso!")
                        
                        except Exception as e:
                            print('Erro ao inserir dados na tabela DADOS_CORRIDA:', e)

            
            else:
                # Marcar o estado anterior como coleta inativa
                collecting_data_prev = False

                # Descartar dados pendentes durante o "STOP"
                if porta_serial.in_waiting > 0:
                    porta_serial.read(porta_serial.in_waiting)  # Descartar os dados do buffer da porta serial

                # Não fazer nada com os dados recebidos após o "STOP" para DADOS_CORRIDA

def inserir_corrida():
    global inseriu_corrida
    if not inseriu_corrida:
        try:
            media_velocidade = calcular_media_velocidade()
            media_aceleracao = calcular_media_aceleracao()
            media_consumo = calcular_media_consumo()
            inicio_corrida =  obter_tempo_inicio_corrida()
            fim_corrida = obter_tempo_fim_corrida()
            tempo_total = calcular_tempo()
            trajeto_total = calcular_trajeto()

            if media_velocidade is not None:
                
                # Inserir uma nova entrada na tabela CORRIDA com os valores calculados e aleatórios
                nova_corrida = CORRIDA(
                    inicio=inicio_corrida,
                    fim=fim_corrida,
                    tempoTotal=tempo_total,
                    trajetoTotal=trajeto_total,
                    consumoMedia=media_consumo,
                    aceleracaoMedia=media_aceleracao,
                    velocidadeMedia=media_velocidade
                )
                db.session.add(nova_corrida)
                db.session.commit()
                print(f"Nova corrida inserida na tabela CORRIDA com valores aleatórios e velocidade média {media_velocidade}")
                inseriu_corrida = True
            
        except Exception as e:
            print('Erro ao calcular média de velocidade ou inserir nova corrida na tabela CORRIDA:', e)

# CALCULANDO AS MEDIAS

def calcular_media_velocidade():
    with app.app_context():
        media = db.session.query(func.avg(DADOS_CORRIDA.velocidade)).filter(DADOS_CORRIDA.idcorri == idcorri_incremento).scalar()
        return media

def calcular_media_aceleracao():
    with app.app_context():
        media = db.session.query(func.avg(DADOS_CORRIDA.aceleracao)).filter(DADOS_CORRIDA.idcorri == idcorri_incremento).scalar()
        return media

def calcular_media_consumo():
    with app.app_context():
        media = db.session.query(func.avg(DADOS_CORRIDA.consumo)).filter(DADOS_CORRIDA.idcorri == idcorri_incremento).scalar()
        return media
    
def calcular_media_consumo():
    with app.app_context():
        media = db.session.query(func.avg(DADOS_CORRIDA.consumo)).filter(DADOS_CORRIDA.idcorri == idcorri_incremento).scalar()
        return media

def obter_tempo_inicio_corrida():
    with app.app_context():
        tempo_inicio_corrida = db.session.query(func.min(DADOS_CORRIDA.tempoColeta)).filter(DADOS_CORRIDA.idcorri == idcorri_incremento).scalar()
        
        return tempo_inicio_corrida
    
def obter_tempo_fim_corrida():
    with app.app_context():
        tempo_fim_corrida = db.session.query(func.max(DADOS_CORRIDA.tempoColeta)).filter(DADOS_CORRIDA.idcorri == idcorri_incremento).scalar()
        
        return tempo_fim_corrida

def calcular_tempo():
    with app.app_context():
        tempo_inicio = db.session.query(func.min(DADOS_CORRIDA.tempoColeta)).filter(DADOS_CORRIDA.idcorri == idcorri_incremento).scalar()
        tempo_fim = db.session.query(func.max(DADOS_CORRIDA.tempoColeta)).filter(DADOS_CORRIDA.idcorri == idcorri_incremento).scalar()
        
        if tempo_inicio and tempo_fim:
            duracao = tempo_fim - tempo_inicio
        else:
            duracao = timedelta(seconds=0)
        
        return duracao
    
def calcular_trajeto():
    with app.app_context():
        trajeto = db.session.query(DADOS_CORRIDA.distancia)\
                            .filter(DADOS_CORRIDA.idcorri == idcorri_incremento)\
                            .order_by(DADOS_CORRIDA.tempoColeta.desc())\
                            .first()
        
        if trajeto:
            trajeto = trajeto[0]  
        
        return trajeto

# Rota padrão
@app.route('/')
def index():
    html = '''
    <h1>Controle de Coleta de Dados</h1>
    <form action="/start" method="POST">
        <input type="submit" value="START">
    </form>
    <form action="/stop" method="POST">
        <input type="submit" value="STOP">
    </form>
    '''
    return html

# Variável para controlar o incremento de idcorri
idcorri_incremento = 1  

# Recuperar o último valor de idcorri do banco de dados ao iniciar a aplicação
with app.app_context():
    ultimo_idcorri = db.session.query(func.max(DADOS_CORRIDA.idcorri)).scalar()
    if ultimo_idcorri is not None:
        idcorri_incremento = ultimo_idcorri + 1

# Rota para iniciar a coleta de dados
@app.route('/start', methods=['POST'])
def start_collecting():
    global collecting_data, inseriu_corrida, idcorri_incremento

    # Incrementar o valor de idcorri para os novos dados
    idcorri_incremento += 1  

    collecting_data = True
    inseriu_corrida = False  # Reiniciar a flag ao iniciar a coleta

    return gera_response(200, "status", "Coleta de dados iniciada")

# Rota para parar a coleta de dados
@app.route('/stop', methods=['POST'])
def stop_collecting():
    global collecting_data

    collecting_data = False

    # Inserir corrida se ainda não inseriu
    inserir_corrida()

    # Limpar dados pendentes durante o "STOP"
    global dados_pendentes
    dados_pendentes = []

    return gera_response(200, "status", "Coleta de dados parada")

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
    ble_thread = threading.Thread(target=verificar_e_inserir_dados_ble)
    ble_thread.start()
    
    # Iniciar a aplicação Flask
    app.run()
