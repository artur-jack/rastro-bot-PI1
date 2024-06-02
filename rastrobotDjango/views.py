from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ESP32Data
from .serializers import ESP32DataSerializer

class ESP32DataView(APIView):
    def post(self, request, format=None):
        # Aqui você pode processar os dados recebidos da ESP32
        data = request.data

        # Serialize os dados recebidos
        serializer = ESP32DataSerializer(data=data)
        
        # Verifique se os dados são válidos
        if serializer.is_valid():
            # Salve os dados no banco de dados
            serializer.save()
            # Salvar no banco de dados ou fazer outras operações
            return Response({'message': 'Dados recebidos com sucesso!'}, status=status.HTTP_201_CREATED)

        # Se os dados não forem válidos, retorne uma resposta de erro com os detalhes dos erros de validação
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ESP32DataListView(APIView):
    def get(self, request, format=None):
        queryset = ESP32Data.objects.all()
        serializer = ESP32DataSerializer(queryset, many=True)
        return Response(serializer.data)

class ESP32DataDeleteView(APIView):
    def delete(self, request, format=None):
        # Excluir todas as requisições no banco de dados
        ESP32Data.objects.all().delete()
        return Response({'message': 'Todas as requisições excluídas com sucesso!'}, status=status.HTTP_204_NO_CONTENT)

