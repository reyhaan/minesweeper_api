from rest_framework import serializers
from .models import Game

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ( 'name', 'uuid', 'map_state', 'has_lost', 'has_won' )
