from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from api_v1.models import Game
from api_v1.serializers import GameSerializer
from api_v1.utils import mapUtils
from api_v1.utils.GameBoard import GameBoard
import json

class GameViewSet(viewsets.ModelViewSet):

    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def perform_create(self, serializer):
        map_state, map_original = mapUtils.getNewMap()
        name = self.request.data.get('name')
        uuid = self.request.data.get('uuid')
        if serializer.is_valid():
            serializer.save(
                name=name,
                uuid=uuid,
                map_state=json.dumps(map_state),
                map_original=json.dumps(map_original)
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=self.kwargs['pk'])

        response = {
            'name': user.name,
            'uuid': user.uuid,
            'map_state': json.loads(user.map_state)
        }

        return Response(response, status=status.HTTP_200_OK)


    @action(methods=['put'], detail=False)
    def move(self, request):
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=request.data.get('uuid'))
        serializer = GameSerializer(user, data=request.data)

        if serializer.is_valid():
            # get original map from database
            map_original = json.loads(user.map_original)

            # get map_state from database
            map_state = json.loads(user.map_state)

            # get next move from user
            move = request.data.get('move')

            gameBoard = GameBoard(map_state, map_original)
            gameBoard.makeMove(move)

            serializer.save(
                map_state=json.dumps(gameBoard.getMapState()),
                map_original=json.dumps(gameBoard.getMapOriginal())
            )

            response = {
                'user': request.data, 
                'new_map_state': gameBoard.getMapState(), 
                'hasLost': gameBoard.getHasLost(), 
                'hasWon': gameBoard.getHasWon()
            }

            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @action(methods=['put'], detail=False)
    def new(self, request):
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=request.data.get('uuid'))
        serializer = GameSerializer(user, data=request.data)

        new_map_state, new_map_original = mapUtils.getNewMap()
        
        if serializer.is_valid():
            serializer.save( 
                map_state=json.dumps(new_map_state),
                map_original=json.dumps(new_map_original)
            )

            response = {
                'new_map_state': new_map_state
            }

            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

