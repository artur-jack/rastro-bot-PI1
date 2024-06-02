from django.db import models
from django.utils import timezone

class ESP32Data(models.Model):
    sensor_esquerdo = models.CharField(max_length=100)
    sensor_direito = models.CharField(max_length=100)
    velocidade = models.FloatField(default=0.0)  # Adicionando o campo para a velocidade
    distancia = models.FloatField(default=0.0)   # Adicionando o campo para a distância
    timestamp = models.DateTimeField(default=timezone.now)  # Adicionando o campo para o timestamp

    def __str__(self):
        return f"Sensor Esquerdo: {self.sensor_esquerdo}, Sensor Direito: {self.sensor_direito}, Velocidade: {self.velocidade}, Distância: {self.distancia}, Timestamp: {self.timestamp}"


