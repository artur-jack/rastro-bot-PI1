# corrida/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Corrida, DadosCorrida
from django.utils.timezone import now
from django.db.models import Avg
import json
import datetime

@csrf_exempt
def receive_sensor_data(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        
        # Cria uma nova corrida ou pega a corrida ativa
        corrida, created = Corrida.objects.get_or_create(estado='ativa', fim__isnull=True)

        # Cria novos dados de corrida
        DadosCorrida.objects.create(
            corrida=corrida,
            distancia=data['distancia'],
            velocidade=data['velocidade'],
            aceleracao=data['aceleracao'],
            consumo=data['consumo']
        )
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def end_corrida(request, corrida_id):
    corrida = get_object_or_404(Corrida, id=corrida_id)
    corrida.estado = 'finalizada'
    corrida.fim = now()
    corrida.save()

    # Calcula os dados médios
    dados = DadosCorrida.objects.filter(corrida=corrida)
    
    # Converte os tempos para segundos
    total_tempo = sum((d.tempo_coleta - datetime.datetime(1970, 1, 1, tzinfo=d.tempo_coleta.tzinfo)).total_seconds() for d in dados)
    
    total_trajeto = sum(dados.values_list('distancia', flat=True))
    media_velocidade = dados.aggregate(Avg('velocidade'))['velocidade__avg']
    media_aceleracao = dados.aggregate(Avg('aceleracao'))['aceleracao__avg']
    media_consumo = dados.aggregate(Avg('consumo'))['consumo__avg']

    corrida.tempo_total = total_tempo
    corrida.trajeto_total = total_trajeto
    corrida.media_velocidade = media_velocidade
    corrida.media_aceleracao = media_aceleracao
    corrida.media_consumo = media_consumo

    corrida.save()

    return JsonResponse({'status': 'corrida finalizada com sucesso'})