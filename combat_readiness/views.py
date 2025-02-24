from django.shortcuts import render
from rest_framework import generics
from .models import Soldier, Equipment, ReadinessReport
from .serializers import SoldierSerializer, EquipmentSerializer, ReadinessReportSerializer
from django.shortcuts import render
from .decorators import role_required

# Function-Based Views
def soldier_list(request):
    soldiers = Soldier.objects.all()
    return render(request, 'soldiers/list.html', {'soldiers': soldiers})

def equipment_list(request):
    equipment = Equipment.objects.all()
    return render(request, 'equipment/list.html', {'equipment': equipment})

def home(request):
    return render(request, 'home.html')

# API Views for Soldier
class SoldierListCreateView(generics.ListCreateAPIView):
    queryset = Soldier.objects.all()
    serializer_class = SoldierSerializer

class SoldierRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Soldier.objects.all()
    serializer_class = SoldierSerializer

# API Views for Equipment
class EquipmentListCreateView(generics.ListCreateAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

class EquipmentRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

# API Views for ReadinessReport
class ReadinessReportListCreateView(generics.ListCreateAPIView):
    queryset = ReadinessReport.objects.all()
    serializer_class = ReadinessReportSerializer

class ReadinessReportRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReadinessReport.objects.all()
    serializer_class = ReadinessReportSerializer

@role_required(['Admin', 'Unit Leader'])
def soldier_list(request):
    # Only Admin & Unit Leaders can see this page
    return render(request, 'soldiers.html')

@role_required(['Medical Officer'])
def health_dashboard(request):
    # Only Medical Officers can access health data
    return render(request, 'health.html')
