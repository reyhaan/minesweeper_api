from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .models import Game
from .serializers import GameSerializer
from api_v1.utils import mapUtils
import json

class GameViewSet(viewsets.ModelViewSet):

    queryset = Game.objects.all()
    serializer_class = GameSerializer
    
    @action(methods=['put'], detail=False)
    def move(self, request):
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=request.data.get('uuid'))
        serializer = GameSerializer(user, data=request.data)
        if serializer.is_valid():
            move = request.data.get('move')
            new_map_state = mapUtils.makeMove(move, request.data.get('map_state'))
            serializer.save( 
                map_state=new_map_state
            )
            return Response({'map': new_map_state})
        else:
            return Response({'error': 'some error'})

    def perform_create(self, serializer):
        serializer.save(
            name=self.request.data.get('name'),
            uuid=self.request.data.get('uuid'),
            map_state=json.dumps(mapUtils.getNewMap())
        )