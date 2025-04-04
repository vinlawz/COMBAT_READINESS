from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import Soldier, Equipment, ReadinessReport, CustomUser

# 🚀 Register View
class RegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')  # Redirect to home after successful registration

    def form_valid(self, form):
        # Auto-login user after registration
        response = super().form_valid(form)
        login(self.request, form.save())
        return response

# 🚀 Home Page View
class HomeView(TemplateView):
    template_name = 'home.html'

# 🚀 Soldier Views
class SoldierListView(LoginRequiredMixin, ListView):
    model = Soldier
    template_name = 'soldiers/list.html'
    context_object_name = 'soldiers'

class SoldierCreateView(LoginRequiredMixin, CreateView):
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

# 🚀 Profile View (Display User Profile)
class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'profile.html'
    context_object_name = 'user'

    def get_object(self):
        # Return the logged-in user's profile
        return self.request.user

# 🚀 Profile Edit View (Edit User Profile)
class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'profile_edit.html'
    fields = ['username', 'email', 'role']  # Fields you want the user to edit
    success_url = reverse_lazy('profile')

    def get_object(self):
        # Ensure that the profile being edited belongs to the logged-in user
        return self.request.user

# 🚀 Role-based Access Control (RBAC) Mixins
class AdminRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.role == 'admin':
            return redirect('home')  # Redirect to home or another page if not admin
        return super().dispatch(request, *args, **kwargs)

class MedicalOfficerRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.role == 'medical_officer':
            return redirect('home')  # Redirect to home or another page if not medical officer
        return super().dispatch(request, *args, **kwargs)

# Example of Restricting Access to Admin Views
class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'admin_dashboard.html'

# Example of Restricting Access to Medical Officer Views
class MedicalOfficerDashboardView(MedicalOfficerRequiredMixin, TemplateView):
    template_name = 'medical_officer_dashboard.html'
