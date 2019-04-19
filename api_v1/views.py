from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

class MapViewSet(viewsets.ViewSet):

    def list(self, request):
        some_response = [
            'something cool',
            'another item',
            'just one more item'
        ]

        return Response({'message': 'Helloe!', 'data': some_response})