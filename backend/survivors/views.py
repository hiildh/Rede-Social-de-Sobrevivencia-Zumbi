from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import Survivor, Inventory
from .serializers import SurvivorSerializer, InventorySerializer


@api_view(['POST'])
def register_survivor(request):
    if request.method == 'POST':
        print("Dados recebidos:", request.data)  # Adicione este print para verificar os dados recebidos
        survivor_serializer = SurvivorSerializer(data=request.data)
        if survivor_serializer.is_valid():
            survivor = survivor_serializer.save()  # Salva o sobrevivente e obtém a instância
            inventory_data = request.data.get('inventory')  # Obtém os dados do inventário do request
            inventory_data['survivor'] = survivor.id  # Adiciona o ID do sobrevivente aos dados do inventário
            inventory_serializer = InventorySerializer(data=inventory_data)
            if inventory_serializer.is_valid():
                inventory_serializer.save()  # Salva o inventário
                return Response(survivor_serializer.data, status=201)
            survivor.delete()  # Se houver um erro no inventário, exclui o sobrevivente
            print("Erros no inventário:", inventory_serializer.errors)  # Adicione este print para verificar os erros no inventário
            return Response(inventory_serializer.errors, status=400)
        print("Erros no sobrevivente:", survivor_serializer.errors)  # Adicione este print para verificar os erros no sobrevivente
        return Response(survivor_serializer.errors, status=400)


class SurvivorViewSet(viewsets.ModelViewSet):
    queryset = Survivor.objects.all()
    serializer_class = SurvivorSerializer
    lookup_field = 'unique_code'

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
