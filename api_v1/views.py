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

    def perform_create(self, serializer):
        serializer.save(
            name=self.request.data.get('name'),
            uuid=self.request.data.get('uuid'),
            map_state=mapUtils.getNewMap()
        )