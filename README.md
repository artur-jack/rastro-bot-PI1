# API_Flask
Esta API, desenvolvida em Python utilizando o Flask, recebe dados via MQTT da ESP32 e os armazena em um banco de dados MySQL local. Foi projetada com o propósito de ser utilizada em um carrinho seguidor de linha para coletar dados durante uma corrida.

# Requisitos

```bash
$ pip install Flask Flask-SQLAlchemy 
$ pip install mysql-connector-python
$ pip install Flask-MQTT
$ pip install requests
$ sudo apt-get install mosquitto-clients
$ pip install mysqlclient
```
# Testar MQTT
```bash
mosquitto_pub -h broker.emqx.io -t "/flaskk/mqtt" -m '{"sensor_esquerdo": 1, "sensor_direito": 1, "velocidade": 10, "distancia": 20, "timestamp": "2024-06-15 11:30:00"}'
```
Obs: A api deve estar rodando para que isso funcione.

# Rodar a API
```bash
$ flask run
```
