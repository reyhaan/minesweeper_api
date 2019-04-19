from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from . import serializers

# Create your views here.
class GameView(APIView):

    serializer_class = serializers.GameSerializer

    def get(self, request, format=None):
        return Response({'data': 'something'})

    def post(self, request):
        serializer = serializers.GameSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            return Response({'message': name})
        else:
            return Response({'error': 'Oops!'})
