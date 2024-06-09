from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import Survivor, Inventory
from .serializers import SurvivorSerializer, InventorySerializer

@api_view(['POST'])
def register_survivor(request):
    if request.method == 'POST':
        print("Dados recebidos:", request.data) 
        survivor_serializer = SurvivorSerializer(data=request.data)
        if survivor_serializer.is_valid():
            survivor = survivor_serializer.save()  
            inventory_data = request.data.get('inventory') 
            inventory_data['survivor'] = survivor.id  
            inventory_serializer = InventorySerializer(data=inventory_data)
            if inventory_serializer.is_valid():
                inventory_serializer.save()  
                return Response(survivor_serializer.data, status=201)
            survivor.delete()  
            print("Erros no inventário:", inventory_serializer.errors)  
            return Response(inventory_serializer.errors, status=400)
        print("Erros no sobrevivente:", survivor_serializer.errors)  
        return Response(survivor_serializer.errors, status=400)

@api_view(['GET'])
def current_survivor(request):
    survivor = Survivor.objects.first()  
    serializer = SurvivorSerializer(survivor)
    return Response(serializer.data)

@api_view(['GET'])
def survivor_inventory(request, survivor_id):
    try:
        inventory = Inventory.objects.get(survivor_id=survivor_id)
        serializer = InventorySerializer(inventory)
        return Response(serializer.data)
    except Inventory.DoesNotExist:
        return Response({'error': 'Inventory not found'}, status=404)

@api_view(['GET'])
def get_survivor_by_name(request):
    print("Parâmetros recebidos:", request.query_params)
    name = request.query_params.get('name')
    if name:
        survivors = Survivor.objects.filter(name=name)
        inventory = Inventory.objects.filter(survivor_id=survivors[0].id)
        if survivors.exists():
            serializer = SurvivorSerializer(survivors, many=True)
            serializer_inventory = InventorySerializer(inventory, many=True)
            survivor_dict = serializer.data[0]
            inventory_dict = serializer_inventory.data[0]
            return Response({'survivor': survivor_dict, 'inventory': inventory_dict}, status=200)
        return Response({'error': 'Survivor not found'}, status=404)
    return Response({'error': 'Name parameter is required'}, status=400)

class SurvivorViewSet(viewsets.ModelViewSet):
    queryset = Survivor.objects.all()
    serializer_class = SurvivorSerializer
    lookup_field = 'name'

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
