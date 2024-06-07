# corrida/models.py
from django.db import models

class Corrida(models.Model):
    inicio = models.DateTimeField(auto_now_add=True)
    fim = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20)
    tempo_total = models.FloatField(null=True, blank=True)
    trajeto_total = models.FloatField(null=True, blank=True)
    consumo_medio = models.FloatField(null=True, blank=True)
    aceleracao_media = models.FloatField(null=True, blank=True)
    velocidade_media = models.FloatField(null=True, blank=True)

class DadosCorrida(models.Model):
    corrida = models.ForeignKey(Corrida, on_delete=models.CASCADE)
    tempo_coleta = models.DateTimeField(auto_now_add=True)
    distancia = models.FloatField()
    velocidade = models.FloatField()
    aceleracao = models.FloatField()
    consumo = models.FloatField()
