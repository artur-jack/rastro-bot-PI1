# Passos para Configurar a API
## Configurar o Ambiente Django:

Instale o Django se ainda não estiver instalado: pip install django

## Configurar o Banco de Dados:

mudar no arquivo testeAPI/meu_projeto/settings.py:

colocar a senha do seu usuário root do mysql

onde tiver:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'rastrinho',
        'USER': 'root',
        'PASSWORD': 'root',   <--- MUDAR
        'HOST': 'localhost',
        'PORT': '3306',
}}

### Aplique as migrações do banco de dados:

python manage.py makemigrations
python manage.py migrate

## Inicie o servidor Django:

python manage.py runserver

## Fazer Requisições para a API

Usando curl no Terminal:

### Enviar Dados do Sensor:

curl -X POST http://127.0.0.1:8000/api/receive/ -H "Content-Type: application/json" -d '{"distancia": 100.0, "velocidade": 60.0, "aceleracao": 5.0, "consumo": 10.0}'

### Finalizar Corrida:

curl -X POST http://127.0.0.1:8000/api/end/1/
