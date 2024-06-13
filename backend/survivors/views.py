from django.forms import FloatField, IntegerField
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count, Sum
from django.db.models.functions import Coalesce
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import InfectionReport, Survivor, Inventory
from .serializers import SurvivorSerializer, InventorySerializer

@api_view(['POST'])
def register_survivor(request):
    if request.method == 'POST':
        name = request.data.get('name')
        if Survivor.objects.filter(name=name).exists():
            return Response({'error': 'Já existe um sobrevivente com este nome.'}, status=status.HTTP_400_BAD_REQUEST)

        survivor_serializer = SurvivorSerializer(data=request.data)
        if survivor_serializer.is_valid():
            survivor = survivor_serializer.save()
            inventory_data = request.data.get('inventory', {})
            inventory_data['survivor'] = survivor.id
            inventory_serializer = InventorySerializer(data=inventory_data)
            if inventory_serializer.is_valid():
                inventory_serializer.save()
                return Response(survivor_serializer.data, status=status.HTTP_201_CREATED)
            survivor.delete()
            return Response(inventory_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(survivor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def current_survivor(request):
    survivor = Survivor.objects.first()  
    serializer = SurvivorSerializer(survivor)
    return Response(serializer.data)


@api_view(['GET'])
def get_survivor_by_name(request):
    name = request.query_params.get('name')
    if name:
        survivors = Survivor.objects.filter(name=name)
        inventory = Inventory.objects.filter(survivor_id=survivors[0].id)
        if survivors.exists():
            serializer = SurvivorSerializer(survivors, many=True)
            serializer_inventory = InventorySerializer(inventory, many=True)
            survivor_dict = serializer.data[0]
            inventory_dict = serializer_inventory.data[0]
            if survivors[0].infected:
                return Response({'error': 'Sobrevivente infectado'}, status=401)
            return Response({'survivor': survivor_dict, 'inventory': inventory_dict}, status=200)
        return Response({'error': 'Sobrevivente não encontrado'}, status=404)
    return Response({'error': 'Parâmetro "Nome" é obrigatório'}, status=400)

@api_view(['POST'])
def report_infection(request):
    reporter_name = request.data.get('reporter_name')
    reported_survivor_name = request.data.get('reported_survivor_name')

    if not reporter_name or not reported_survivor_name:
        return Response({'error': 'O nome do repórter e o nome do sobrevivente relatado são obrigatórios'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        reporter = Survivor.objects.get(name=reporter_name)
        reported_survivor = Survivor.objects.get(name=reported_survivor_name)
    except Survivor.DoesNotExist:
        return Response({'error': 'Sobrevivente não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    if reporter == reported_survivor:
        return Response({'error': 'O repórter e o sobrevivente relatado não podem ser os mesmos'}, status=status.HTTP_400_BAD_REQUEST)

    if InfectionReport.objects.filter(reporter=reporter, reported_survivor=reported_survivor).exists():
        return Response({'error': 'Você já relatou este sobrevivente'}, status=status.HTTP_400_BAD_REQUEST)

    InfectionReport.objects.create(reporter=reporter, reported_survivor=reported_survivor)

    reports_count = reported_survivor.reports.count()
    if reports_count >= 3:
        reported_survivor.infected = True
        reported_survivor.save()
        return Response({'status': 'Sobrevivente marcado como infectado'}, status=status.HTTP_200_OK)

    return Response({'status': 'Infecção reportada'}, status=status.HTTP_201_CREATED)


class SurvivorViewSet(viewsets.ModelViewSet):
    queryset = Survivor.objects.all()
    serializer_class = SurvivorSerializer
    lookup_field = 'name'

    @action(detail=True, methods=['patch'])
    def update_location(self, request, name=None):
        survivor = self.get_object()
        survivor.last_location = request.data.get('last_location')
        survivor.save()
        return Response({'status': 'Localização atualizada'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def mark_infected(self, request, name=None):
        survivor = self.get_object()
        
        if survivor.infected:
            return Response({'error': 'Sobrevivente já infectado'}, status=status.HTTP_400_BAD_REQUEST)
        
        reporter_name = request.data.get('reporter_name')
        reported_survivor_name = survivor.name

        if not reporter_name:
            return Response({'error': 'Nome do repórter obrigatório'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            reporter = Survivor.objects.get(name=reporter_name)
        except Survivor.DoesNotExist:
            return Response({'error': 'Reportér não encontrado'}, status=status.HTTP_404_NOT_FOUND)

        if reporter == survivor:
            return Response({'error': 'O repórter e o sobrevivente relatado não podem ser os mesmos'}, status=status.HTTP_400_BAD_REQUEST)

        if InfectionReport.objects.filter(reporter=reporter, reported_survivor=survivor).exists():
            return Response({'error': 'Você já relatou este sobrevivente'}, status=status.HTTP_400_BAD_REQUEST)

        InfectionReport.objects.create(reporter=reporter, reported_survivor=survivor)

        reports_count = survivor.reports.count()
        if reports_count >= 3:
            survivor.infected = True
            survivor.save()
            return Response({'status': 'Sobrevivente marcado como infectado'}, status=status.HTTP_200_OK)
        return Response({'status': 'Infecção reportada'}, status=status.HTTP_201_CREATED)


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    lookup_field = 'survivor'

    @action(detail=True, methods=['post'])
    def trade(self, request, survivor=None):
        current_survivor = get_object_or_404(Survivor, name=survivor)
        current_inventory = Inventory.objects.get(survivor=current_survivor)
        other_survivor_username = request.data.get('other_inventory')
        other_survivor = get_object_or_404(Survivor, name=other_survivor_username)
        other_inventory = Inventory.objects.get(survivor=other_survivor)

        offered_items = request.data.get('offered_items', {})
        requested_items = request.data.get('requested_items', {})

        success, message = current_inventory.trade_items_with(other_inventory, offered_items, requested_items)
        if success:
            return Response({'status': message}, status=status.HTTP_200_OK)
        else:
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
        


@api_view(['GET'])
def reports(request):
    total_survivors = Survivor.objects.count()
    infected_count = Survivor.objects.filter(infected=True).count()
    uninfected_count = total_survivors - infected_count
    infected_percentage = (infected_count / total_survivors) * 100 if total_survivors > 0 else 0
    uninfected_percentage = 100 - infected_percentage

    inventories = Inventory.objects.select_related('survivor').all()

    total_water = total_food = total_medication = total_ammunition = 0
    for inventory in inventories:
        total_water += inventory.water
        total_food += inventory.food
        total_medication += inventory.medication
        total_ammunition += inventory.ammunition

    if total_survivors > 0:
        avg_water = total_water / total_survivors
        avg_food = total_food / total_survivors
        avg_medication = total_medication / total_survivors
        avg_ammunition = total_ammunition / total_survivors
    else:
        avg_water = avg_food = avg_medication = avg_ammunition = 0

    infected_points_lost = Inventory.objects.filter(survivor__infected=True).aggregate(
        total_points_lost=Sum('water') * 4 + Sum('food') * 3 + Sum('medication') * 2 + Sum('ammunition')
    )['total_points_lost'] or 0

    report_data = {
        'infected_percentage': infected_percentage,
        'uninfected_percentage': uninfected_percentage,
        'avg_water': avg_water,
        'avg_food': avg_food,
        'avg_medication': avg_medication,
        'avg_ammunition': avg_ammunition,
        'infected_points_lost': infected_points_lost
    }

    return Response(report_data)