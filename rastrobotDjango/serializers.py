from rest_framework import serializers
from .models import ESP32Data

class ESP32DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ESP32Data
        fields = ['sensor_esquerdo', 'sensor_direito', 'velocidade', 'distancia', 'timestamp']
        read_only_fields = ['timestamp']