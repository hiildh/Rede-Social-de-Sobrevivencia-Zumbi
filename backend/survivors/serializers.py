from rest_framework import serializers
from .models import Survivor, Inventory

class SurvivorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survivor
        exclude = ('unique_code',)

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'
