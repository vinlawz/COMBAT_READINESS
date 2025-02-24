from rest_framework import serializers
from .models import Soldier, Equipment, ReadinessReport  # Import the correct models

class SoldierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Soldier
        fields = '__all__'

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'

class ReadinessReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadinessReport
        fields = '__all__'
