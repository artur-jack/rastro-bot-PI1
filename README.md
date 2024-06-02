Até o momento foi criado o arquivo Django com um banco de dados teste utilizando MySQL e Django-Rest-Framework para a API, porém na hora de conectar a URL do servidor Django, foi necessário criar um 'túnel' para 
executar o servidor Django na máquina local para desenvolvimento, se não, a ESP32 não poderá se conectar diretamente à API. Isso porque o ESP32 precisa de um endereço IP acessível pela rede para comunicação, utilizando, assim, o ngrok.

No Vscode:

![image](https://github.com/gustavofbs/django-mysql/assets/61592832/cb9cd0cb-eefe-4bad-8401-af2a0a3ffa5d)

No Arduino-IDE:
![image](https://github.com/gustavofbs/django-mysql/assets/61592832/4ccc28cb-0859-451c-a4a3-22689c6d6b66)

Para o ngrok conhecer as urls a partir da porta 8000, foi necessário o seguinte código:

``` Python
./ngrok http 8000 
  --forwards "http://localhost:8000/api/esp32/ -> /api/esp32/" \
  --forwards "http://localhost:8000/api/esp32/data/ -> /api/esp32/data/" \
  --forwards "http://localhost:8000/api/esp32/data/delete/ -> /api/esp32/data/delete/"
```
