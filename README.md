# API_Flask_ESP32_Bluetooth

Esta API, desenvolvida em Python utilizando o Flask, recebe dados via Bluetooth da ESP32-WROOM-32D e os armazena em um banco de dados MySQL local. Foi projetada com o propósito de ser utilizada em um carrinho seguidor de linha para coletar dados durante uma corrida.

# Requisitos

```bash
$ pip install Flask Flask-SQLAlchemy 
$ pip install mysql-connector-python
$ pip install requests
$ pip install pymysql
$ pip install pyserial

```

# Configurando
Abra o seu Mysql local e crie um banco de dados chamado rastrobotdb2.
```
CREATE DATABASE rastrobotdb2;
```

Na linha 19 do arquivo app.py insira o seu login e senha do Mysql.

```
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://LOGIN:SENHA@localhost/rastrobotdb2'
```

Na linha 39 do arquivo app.py insira a porta de saída de dados do bluetooth da ESP32.

```
porta_serial = serial.Serial('PORTA', 115200)
```

# Rodar a API
```bash
$ flask run
```
