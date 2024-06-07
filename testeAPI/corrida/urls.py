# corrida/urls.py
from django.urls import path
from .views import receive_sensor_data, end_corrida

urlpatterns = [
    path('receive/', receive_sensor_data, name='receive_sensor_data'),
    path('end/<int:corrida_id>/', end_corrida, name='end_corrida'),
]
