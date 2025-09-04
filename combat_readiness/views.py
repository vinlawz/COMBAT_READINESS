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
from django.db.models import Count
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
import csv
from django.utils.encoding import smart_str, force_str, force_bytes
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from .utils import account_activation_token, send_verification_email
import logging

logger = logging.getLogger(__name__)

#  Register View
class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Deactivate account until email is verified
        user.is_verified = False
        user.save()
        
        # Send verification email
        try:
            send_verification_email(self.request, user)
            messages.info(
                self.request,
                'Registration successful! Please check your email to verify your account.'
            )
        except Exception as e:
            logger.error(f"Error sending verification email: {e}")
            messages.error(
                self.request,
                'There was an error sending the verification email. Please try again.'
            )
            return super().form_invalid(form)
            
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['soldiers'] = Soldier.objects.all()
        return context

from django.views import View
class BulkAssignEquipmentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        soldier_id = request.POST.get('soldier_id')
        selected_equipment = request.POST.get('selected_equipment', '')
        if not soldier_id or not selected_equipment:
            messages.error(request, 'Please select at least one equipment item and a soldier.')
            return redirect('equipment-list')
        try:
            soldier = Soldier.objects.get(id=soldier_id)
            equipment_ids = [int(eid) for eid in selected_equipment.split(',') if eid]
            updated = Equipment.objects.filter(id__in=equipment_ids).update(assigned_to=soldier)
            if updated:
                messages.success(request, f'{updated} equipment item(s) assigned to {soldier.name}.')
            else:
                messages.warning(request, 'No equipment was assigned.')
        except Soldier.DoesNotExist:
            messages.error(request, 'Selected soldier does not exist.')
        except Exception as e:
            messages.error(request, f'Error during assignment: {e}')
        return redirect('equipment-list')

class EquipmentCreateView(LoginRequiredMixin, CreateView):
    model = Equipment
    template_name = 'Equipment/create.html'
    fields = ['name', 'category', 'condition', 'assigned_to']
    success_url = reverse_lazy('equipment-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Add form-control class to all form fields
        for field_name, field in form.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Equipment'
        return context

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
    if not request.user.is_authenticated:
        return redirect('login')
        
    user = request.user
    profile = user.profile
    
    if request.method == 'POST':
        user_form = UserProfileEditForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            try:
                # Handle file upload
                if 'profile_image' in request.FILES:
                    # Delete old file if it exists and is not the default
                    if profile.profile_image and 'default-avatar' not in str(profile.profile_image):
                        profile.profile_image.delete(save=False)
                
                # Save forms
                user = user_form.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
                
                messages.success(request, 'Your profile was updated successfully!')
                return redirect('profile')
                
            except Exception as e:
                messages.error(request, f'Error updating profile: {str(e)}')
        else:
            # Form validation failed
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
            for field, errors in profile_form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
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
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("You don't have permission to access this page.")
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

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        from .models import Soldier, Equipment, Mission, ReadinessReport, Notification
        context['num_soldiers'] = Soldier.objects.count()
        context['num_equipment'] = Equipment.objects.count()
        context['num_missions'] = Mission.objects.count()
        context['num_unread_notifications'] = Notification.objects.filter(recipient=user, is_read=False).count()
        context['recent_missions'] = Mission.objects.order_by('-start_date')[:5]
        context['recent_reports'] = ReadinessReport.objects.order_by('-last_training_date')[:5]
        context['recent_notifications'] = Notification.objects.filter(recipient=user).order_by('-created_at')[:5]
        context['user_role'] = getattr(user, 'role', 'user')
        # Upcoming missions (next 7 days)
        today = timezone.now().date()
        in_7_days = today + timezone.timedelta(days=7)
        context['upcoming_missions'] = Mission.objects.filter(start_date__gte=today, start_date__lte=in_7_days).order_by('start_date')
        # Equipment needing repair
        context['equipment_needing_repair'] = Equipment.objects.filter(condition='Needs Repair')
        # Soldiers with poor readiness (latest report)
        poor_soldiers = []
        for soldier in Soldier.objects.all():
            latest_report = ReadinessReport.objects.filter(soldier=soldier).order_by('-last_training_date').first()
            if latest_report and latest_report.overall_readiness == 'Poor':
                poor_soldiers.append(soldier)
        context['poor_soldiers'] = poor_soldiers
        return context

from django.views import View
class MarkAllNotificationsReadView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        from .models import Notification
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        return HttpResponseRedirect(reverse('dashboard'))

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
    
    if user is not None and account_activation_token.check_token(user, token):
        if user.is_verified:
            messages.info(request, 'Your account is already verified. Please log in.')
        else:
            user.is_verified = True
            user.is_active = True  # Activate the account
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
            # Resend verification email if not verified
            try:
                send_verification_email(self.request, user)
                messages.warning(
                    self.request,
                    'Your account is not verified. A new verification email has been sent. '\
                    'Please check your email and verify your account.'
                )
            except Exception as e:
                logger.error(f"Error resending verification email: {e}")
                messages.error(
                    self.request,
                    'Your account is not verified and we could not resend the verification email. '\
                    'Please contact support.'
                )
            return redirect('login')
            messages.error(self.request, 'Your account is not verified. Please check your email.')
            return redirect('login')
        return super().form_valid(form)

class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

from django.views import View
class MissionEventsJsonView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        from .models import Mission, TrainingEvent
        events = []
        status_colors = {
            'Planned': '#007bff',
            'Active': '#28a745',
            'Completed': '#6c757d',
            'Cancelled': '#dc3545',
        }
        for mission in Mission.objects.all():
            events.append({
                'id': f'mission-{mission.id}',
                'title': mission.name,
                'start': str(mission.start_date),
                'end': str(mission.end_date) if mission.end_date else str(mission.start_date),
                'status': mission.status,
                'color': status_colors.get(mission.status, '#ff00cc'),
                'url': f'/missions/{mission.id}/',
            })
        for training in TrainingEvent.objects.all():
            events.append({
                'id': f'training-{training.id}',
                'title': f'Training: {training.name}',
                'start': str(training.date),
                'end': str(training.date),
                'status': 'Training',
                'color': '#ffc107',
                'url': '#',
            })
        return JsonResponse(events, safe=False)

class AdvancedSearchView(LoginRequiredMixin, TemplateView):
    template_name = 'advanced_search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .models import Mission, Soldier, Equipment
        # Missions search
        mission_qs = Mission.objects.all()
        m_name = self.request.GET.get('m_name', '').strip()
        m_status = self.request.GET.get('m_status', '')
        m_priority = self.request.GET.get('m_priority', '')
        m_location = self.request.GET.get('m_location', '').strip()
        m_start = self.request.GET.get('m_start', '')
        m_end = self.request.GET.get('m_end', '')
        if m_name:
            mission_qs = mission_qs.filter(name__icontains=m_name)
        if m_status:
            mission_qs = mission_qs.filter(status=m_status)
        if m_priority:
            mission_qs = mission_qs.filter(priority=m_priority)
        if m_location:
            mission_qs = mission_qs.filter(location__icontains=m_location)
        if m_start:
            mission_qs = mission_qs.filter(start_date__gte=m_start)
        if m_end:
            mission_qs = mission_qs.filter(end_date__lte=m_end)
        context['mission_results'] = mission_qs
        # Soldiers search
        soldier_qs = Soldier.objects.all()
        s_name = self.request.GET.get('s_name', '').strip()
        s_rank = self.request.GET.get('s_rank', '')
        s_unit = self.request.GET.get('s_unit', '').strip()
        s_status = self.request.GET.get('s_status', '')
        if s_name:
            soldier_qs = soldier_qs.filter(name__icontains=s_name)
        if s_rank:
            soldier_qs = soldier_qs.filter(rank__icontains=s_rank)
        if s_unit:
            soldier_qs = soldier_qs.filter(unit__icontains=s_unit)
        if s_status:
            soldier_qs = soldier_qs.filter(status=s_status)
        context['soldier_results'] = soldier_qs
        # Equipment search
        equipment_qs = Equipment.objects.all()
        e_name = self.request.GET.get('e_name', '').strip()
        e_category = self.request.GET.get('e_category', '').strip()
        e_condition = self.request.GET.get('e_condition', '')
        e_assigned = self.request.GET.get('e_assigned', '').strip()
        if e_name:
            equipment_qs = equipment_qs.filter(name__icontains=e_name)
        if e_category:
            equipment_qs = equipment_qs.filter(category__icontains=e_category)
        if e_condition:
            equipment_qs = equipment_qs.filter(condition=e_condition)
        if e_assigned:
            equipment_qs = equipment_qs.filter(assigned_to__name__icontains=e_assigned)
        context['equipment_results'] = equipment_qs
        # For filter dropdowns
        context['mission_status_choices'] = Mission.STATUS_CHOICES
        context['mission_priority_choices'] = Mission.PRIORITY_CHOICES
        context['soldier_status_choices'] = Soldier._meta.get_field('status').choices
        context['equipment_condition_choices'] = Equipment._meta.get_field('condition').choices
        return context

class ExportMissionsCSVView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        from .models import Mission
        # Apply same filters as AdvancedSearchView
        mission_qs = Mission.objects.all()
        m_name = request.GET.get('m_name', '').strip()
        m_status = request.GET.get('m_status', '')
        m_priority = request.GET.get('m_priority', '')
        m_location = request.GET.get('m_location', '').strip()
        m_start = request.GET.get('m_start', '')
        m_end = request.GET.get('m_end', '')
        if m_name:
            mission_qs = mission_qs.filter(name__icontains=m_name)
        if m_status:
            mission_qs = mission_qs.filter(status=m_status)
        if m_priority:
            mission_qs = mission_qs.filter(priority=m_priority)
        if m_location:
            mission_qs = mission_qs.filter(location__icontains=m_location)
        if m_start:
            mission_qs = mission_qs.filter(start_date__gte=m_start)
        if m_end:
            mission_qs = mission_qs.filter(end_date__lte=m_end)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=missions.csv'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Status', 'Priority', 'Start Date', 'End Date', 'Location', 'Notes'])
        for m in mission_qs:
            writer.writerow([
                smart_str(m.name), m.status, m.priority, m.start_date, m.end_date or '', m.location, m.notes
            ])
        return response

class ExportReadinessCSVView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        from .models import ReadinessReport
        # Apply same filters as AdvancedSearchView (if any in future)
        report_qs = ReadinessReport.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=readiness_reports.csv'
        writer = csv.writer(response)
        writer.writerow(['Soldier', 'Fitness Score', 'Last Training Date', 'Overall Readiness'])
        for r in report_qs:
            writer.writerow([
                smart_str(r.soldier.name), r.fitness_score, r.last_training_date, r.overall_readiness
            ])
        return response

class AuditLogView(LoginRequiredMixin, TemplateView):
    template_name = 'audit_log.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .models import AuditLog
        logs = AuditLog.objects.all().order_by('-timestamp')
        model = self.request.GET.get('model', '').strip()
        action = self.request.GET.get('action', '').strip()
        user = self.request.GET.get('user', '').strip()
        if model:
            logs = logs.filter(model__icontains=model)
        if action:
            logs = logs.filter(action=action)
        if user:
            logs = logs.filter(user__username__icontains=user)
        context['audit_logs'] = logs[:200]  # Limit for performance
        return context

class NotificationsListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'registration/profile.html'  # notifications_list.html if you rename it
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-created_at')

from django.views import View
class BulkMarkNotificationsReadView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        notification_ids = request.POST.getlist('notification_ids')
        if not notification_ids:
            messages.error(request, 'Please select at least one notification.')
            return redirect('notifications-list')
        updated = Notification.objects.filter(id__in=notification_ids, recipient=request.user).update(is_read=True)
        if updated:
            messages.success(request, f'{updated} notification(s) marked as read.')
        else:
            messages.warning(request, 'No notifications were marked as read.')
        return redirect('notifications-list')

class NotificationsJsonView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        from .models import Notification
        user = request.user
        unread_count = Notification.objects.filter(recipient=user, is_read=False).count()
        recent = Notification.objects.filter(recipient=user).order_by('-created_at')[:5]
        notifications = [
            {
                'message': n.message,
                'created_at': n.created_at.strftime('%b %d, %H:%M'),
                'is_read': n.is_read,
                'link': n.link or '#',
            }
            for n in recent
        ]
        return JsonResponse({'unread_count': unread_count, 'recent_notifications': notifications})
