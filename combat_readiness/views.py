from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Soldier, Equipment, ReadinessReport

# 🚀 Home Page View
class HomeView(TemplateView):
    template_name = 'home.html'

# 🚀 Soldier Views
class SoldierListView(LoginRequiredMixin, ListView):
    model = Soldier
    template_name = 'soldiers/list.html'
    context_object_name = 'soldiers'

class SoldierCreateView(CreateView):
    model = Soldier
    template_name = 'soldiers/create.html'
    fields = ['name', 'rank', 'unit']
    success_url = reverse_lazy('soldier-list')  # Ensure correct URL name

class SoldierRetrieveUpdateDeleteView(LoginRequiredMixin, DetailView, UpdateView, DeleteView):
    model = Soldier
    template_name = 'soldiers/detail.html'
    fields = ['name', 'rank', 'unit']
    success_url = reverse_lazy('soldier-list')  # Fixed!

# 🚀 Equipment Views
class EquipmentListView(LoginRequiredMixin, ListView):
    model = Equipment
    template_name = 'equipment/list.html'
    context_object_name = 'equipment'

class EquipmentCreateView(LoginRequiredMixin, CreateView):
    model = Equipment
    template_name = 'equipment/create.html'
    fields = ['name', 'category', 'condition', 'assigned_to']
    success_url = reverse_lazy('equipment-list')  # Fixed!

class EquipmentRetrieveUpdateDeleteView(LoginRequiredMixin, DetailView, UpdateView, DeleteView):
    model = Equipment
    template_name = 'equipment/detail.html'
    fields = ['name', 'category', 'condition', 'assigned_to']
    success_url = reverse_lazy('equipment-list')  # Fixed!

# 🚀 Readiness Reports
class ReadinessReportListView(LoginRequiredMixin, ListView):
    model = ReadinessReport
    template_name = 'reports/list.html'
    context_object_name = 'reports'

class ReadinessReportCreateView(LoginRequiredMixin, CreateView):
    model = ReadinessReport
    template_name = 'reports/create.html'
    fields = ['soldier', 'fitness_score', 'last_training_date', 'overall_readiness']
    success_url = reverse_lazy('readiness-list')  # Fixed!

class ReadinessReportRetrieveUpdateDeleteView(LoginRequiredMixin, DetailView, UpdateView, DeleteView):
    model = ReadinessReport
    template_name = 'reports/detail.html'
    fields = ['soldier', 'fitness_score', 'last_training_date', 'overall_readiness']
    success_url = reverse_lazy('readiness-list')  # Fixed!
