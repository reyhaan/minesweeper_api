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
            new_map_state = mapUtils.makeMove(move, json.loads(request.data.get('map_state')), json.loads(user.map_original))
            serializer.save(
                map_state=new_map_state,
                map_original=user.map_original
            )
            return Response({'user': request.data, 'new_map_state': new_map_state})
        else:
            return Response({'error': 'some error'})
    
    @action(methods=['put'], detail=False)
    def new(self, request):
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=request.data.get('uuid'))
        serializer = GameSerializer(user, data=request.data)
        new_map_state = json.dumps(mapUtils.getNewMap())
        if serializer.is_valid():
            serializer.save( 
                map_state=new_map_state
            )
            return Response({'user': request.data, 'new_map_state': json.loads(new_map_state)})
        else:
            return Response({'error': 'some error'})
    
    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=self.kwargs['pk'])
        serializer = GameSerializer(user, data=request.data)
        if serializer.is_valid():
            move = request.data.get('move')
            new_map_state = mapUtils.makeMove(move, json.loads(request.data.get('map_state')))
            serializer.save( 
                map_state=new_map_state
            )
            return Response({'new_map_state': new_map_state})
        else:
            return Response({'error': 'some error'})

    def perform_create(self, serializer):
        map_state, map_original = mapUtils.getNewMap()
        serializer.save(
            name=self.request.data.get('name'),
            uuid=self.request.data.get('uuid'),
            map_state=json.dumps(map_state),
            map_original=json.dumps(map_original)
        )
