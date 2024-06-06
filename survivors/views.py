from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Survivor, Inventory
from .serializers import SurvivorSerializer, InventorySerializer

class SurvivorViewSet(viewsets.ModelViewSet):
    queryset = Survivor.objects.all()
    serializer_class = SurvivorSerializer

    @action(detail=True, methods=['post'])
    def update_location(self, request, pk=None):
        survivor = self.get_object()
        survivor.last_location = request.data.get('last_location')
        survivor.save()
        return Response({'status': 'location updated'})

    @action(detail=True, methods=['post'])
    def mark_infected(self, request, pk=None):
        survivor = self.get_object()
        survivor.infected = True
        survivor.save()
        return Response({'status': 'marked as infected'})

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
