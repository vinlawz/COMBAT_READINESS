from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import Soldier, Equipment, ReadinessReport, CustomUser, Mission, Notification
from django.contrib.auth.decorators import login_required
from .fprms import UserProfileEditForm, UserProfileForm, MissionForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm

#  Register View
class RegisterView(CreateView):
    model = CustomUser
    
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')  # Redirect to login after registration

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_verified = False
        user.save()
        # Send verification email (mock)
        current_site = get_current_site(self.request)
        subject = 'Verify your account'
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        verification_link = self.request.build_absolute_uri(
            reverse('verify', kwargs={'uidb64': uid, 'token': token})
        )
        message = f'Click the link to verify your account: {verification_link}'
        send_mail(subject, message, 'noreply@combatreadiness.com', [user.email], fail_silently=True)
        messages.info(self.request, 'Registration successful! Please check your email to verify your account.')
        return redirect('login')

#  Home Page View
class HomeView(TemplateView):
    template_name = 'home.html'

#  Soldier Views
class SoldierListView(LoginRequiredMixin, ListView):
    model = Soldier
    template_name = 'soldiers/list.html'
    context_object_name = 'soldiers'

class SoldierCreateView(LoginRequiredMixin, CreateView):
    model = Soldier
    template_name = 'soldiers/create.html'
    fields = ['name', 'rank', 'unit']
    success_url = reverse_lazy('soldier-list')  # Ensure correct URL name

class SoldierDetailView(LoginRequiredMixin, DetailView):
    model = Soldier
    template_name = 'soldiers/detail.html'
    context_object_name = 'soldier'

class SoldierUpdateView(LoginRequiredMixin, UpdateView):
    model = Soldier
    template_name = 'soldiers/edit.html'
    fields = ['name', 'rank', 'unit']
    success_url = reverse_lazy('soldier-list')

class SoldierDeleteView(LoginRequiredMixin, DeleteView):
    model = Soldier
    template_name = 'soldiers/delete.html'
    success_url = reverse_lazy('soldier-list')

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
    template_name = 'registration/profile.html'
    context_object_name = 'user'

    def get_object(self):
        # Return the logged-in user's profile
        return self.request.user

# 🚀 Profile Edit View (Edit User Profile)
def profile_edit_view(request):
    user = request.user
    profile = user.profile
    if request.method == 'POST':
        user_form = UserProfileEditForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was updated successfully!')
            return redirect('profile')
    else:
        user_form = UserProfileEditForm(instance=user)
        profile_form = UserProfileForm(instance=profile)
    return render(request, 'profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

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

@login_required
def dashboard_view(request):
    from .models import Soldier, Equipment, ReadinessReport, Mission
    # Total counts
    soldier_count = Soldier.objects.count()
    equipment_count = Equipment.objects.count()

    # Soldiers by status
    soldier_status_counts = {
        status: Soldier.objects.filter(status=status).count()
        for status in ['Active', 'Reserve', 'Retired']
    }

    # Equipment by condition
    equipment_condition_counts = {
        condition: Equipment.objects.filter(condition=condition).count()
        for condition in ['New', 'Good', 'Needs Repair']
    }

    # 5 most recent soldiers
    recent_soldiers = Soldier.objects.order_by('-id')[:5]

    # 5 most recent equipment
    recent_equipment = Equipment.objects.order_by('-id')[:5]

    # Readiness report breakdown
    readiness_breakdown = {
        status: ReadinessReport.objects.filter(overall_readiness=status).count()
        for status in ['Excellent', 'Good', 'Fair', 'Poor']
    }

    # Up to 3 current/planned missions
    dashboard_missions = Mission.objects.filter(status__in=['Active', 'Planned']).order_by('start_date')[:3]

    return render(request, 'dashboard.html', {
        'soldier_count': soldier_count,
        'equipment_count': equipment_count,
        'soldier_status_counts': soldier_status_counts,
        'equipment_condition_counts': equipment_condition_counts,
        'recent_soldiers': recent_soldiers,
        'recent_equipment': recent_equipment,
        'readiness_breakdown': readiness_breakdown,
        'dashboard_missions': dashboard_missions,
    })

# 🚀 Mission Views
class MissionListView(LoginRequiredMixin, ListView):
    model = Mission
    template_name = 'missions/list.html'
    context_object_name = 'missions'
    queryset = Mission.objects.order_by('-start_date')

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')
        search = self.request.GET.get('search')
        if status:
            qs = qs.filter(status=status)
        if priority:
            qs = qs.filter(priority=priority)
        if search:
            qs = qs.filter(models.Q(name__icontains=search) | models.Q(location__icontains=search))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_status'] = self.request.GET.get('status', '')
        context['filter_priority'] = self.request.GET.get('priority', '')
        context['filter_search'] = self.request.GET.get('search', '')
        context['status_choices'] = Mission.STATUS_CHOICES
        context['priority_choices'] = Mission.PRIORITY_CHOICES
        return context

class MissionDetailView(LoginRequiredMixin, DetailView):
    model = Mission
    template_name = 'missions/detail.html'
    context_object_name = 'mission'

class MissionCreateView(LoginRequiredMixin, CreateView):
    model = Mission
    form_class = MissionForm
    template_name = 'missions/create.html'
    success_url = reverse_lazy('mission-list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.role in ['admin', 'unit_leader', 'medical_officer']:
            return redirect('mission-list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        # Notify assigned soldiers
        mission = self.object
        for soldier in mission.assigned_soldiers.all():
            if soldier.user:
                Notification.objects.create(
                    recipient=soldier.user,
                    message=f'You have been assigned to the mission: {mission.name}',
                    link=reverse('mission-detail', args=[mission.pk]),
                    type='info'
                )
        messages.success(self.request, 'Mission created successfully!')
        return response

class MissionUpdateView(LoginRequiredMixin, UpdateView):
    model = Mission
    form_class = MissionForm
    template_name = 'missions/edit.html'
    success_url = reverse_lazy('mission-list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.role in ['admin', 'unit_leader', 'medical_officer']:
            return redirect('mission-list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        mission = self.object
        # Notify newly assigned soldiers only
        old_soldiers = set(mission.assigned_soldiers.model.objects.filter(missions=mission.pk))
        new_soldiers = set(form.cleaned_data['assigned_soldiers'])
        for soldier in new_soldiers - old_soldiers:
            if soldier.user:
                Notification.objects.create(
                    recipient=soldier.user,
                    message=f'You have been assigned to the mission: {mission.name}',
                    link=reverse('mission-detail', args=[mission.pk]),
                    type='info'
                )
        messages.success(self.request, 'Mission updated successfully!')
        return response

class MissionDeleteView(LoginRequiredMixin, DeleteView):
    model = Mission
    template_name = 'missions/delete.html'
    success_url = reverse_lazy('mission-list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.role in ['admin', 'unit_leader', 'medical_officer']:
            return redirect('mission-list')
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Mission deleted successfully!')
        return super().delete(request, *args, **kwargs)

def notifications_context(request):
    if request.user.is_authenticated:
        unread_count = request.user.notifications.filter(is_read=False).count()
        recent_notifications = request.user.notifications.all()[:5]
    else:
        unread_count = 0
        recent_notifications = []
    return {
        'unread_count': unread_count,
        'recent_notifications': recent_notifications,
    }

def verify_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
        messages.success(request, 'Your account has been verified! You can now log in.')
        return redirect('login')
    else:
        return HttpResponse('Verification link is invalid or expired.', status=400)

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_verified:
            messages.error(self.request, 'Your account is not verified. Please check your email.')
            return redirect('login')
        return super().form_valid(form)
