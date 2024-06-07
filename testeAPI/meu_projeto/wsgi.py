"""
WSGI config for meu_projeto project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

# meu_projeto/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meu_projeto.settings')

application = get_wsgi_application()

# Iniciar o cliente MQTT
from corrida.mqtt_client import client

