from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .models import Game
from .serializers import GameSerializer
from api_v1.utils import mapUtils

class GameViewSet(viewsets.ModelViewSet):

    queryset = Game.objects.all()
    serializer_class = GameSerializer

    @action(methods=['post'], detail=False)
    def move(self, request):
        return Response({'message': 'Helloe!', 'data': request.data})


    # def retrieve(self, request, pk=None):
        
    #     serializer = GameSerializer(data=request.data)

    #     if serializer.is_valid():
    #         name = serializer.data.get('name')
    #     else:
    #         name = "not assigned"
        
    #     return Response({'message': 'Helloe!', 'data': name})

    # def create(self, request):

    #     serializer = GameSerializer(data=request.data)

    #     if serializer.is_valid():
    #         new_game = Game.objects.create(
    #             name=serializer.data.get('name'),
    #             uuid=serializer.data.get('uuid'),
    #             mapState=serializer.data.get('mapState')
    #         )
    #     return Response({'message': 'CREATE_EVENT', 'data': request.data})