# corrida/mqtt_client.py
import json
import paho.mqtt.client as mqtt
from django.utils import timezone
from .models import Corrida, DadosCorrida

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("esp32/data")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    data = json.loads(msg.payload)

    # Supomos que você tenha uma corrida ativa
    corrida = Corrida.objects.filter(estado='ativa').first()
    if not corrida:
        corrida = Corrida.objects.create(estado='ativa')

    DadosCorrida.objects.create(
        corrida=corrida,
        distancia=data['distancia'],
        velocidade=data['velocidade'],
        aceleracao=data.get('aceleracao', 0),  # Supondo que a aceleração esteja no payload
        consumo=data.get('consumo', 0)  # Supondo que o consumo esteja no payload
    )

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_start()
