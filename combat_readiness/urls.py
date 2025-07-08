# urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import (
    SoldierListView, SoldierCreateView, SoldierDetailView, SoldierUpdateView, SoldierDeleteView,
    EquipmentListView, EquipmentCreateView, EquipmentRetrieveUpdateDeleteView,
    ReadinessReportListView, ReadinessReportCreateView, ReadinessReportRetrieveUpdateDeleteView,
    HomeView, RegisterView, ProfileView, profile_edit_view, AdminDashboardView, MedicalOfficerDashboardView,
    dashboard_view, MissionListView, MissionDetailView, MissionCreateView, MissionUpdateView, MissionDeleteView,
    verify_view, CustomLoginView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),

    #  Soldier URLs
    path('soldiers/', SoldierListView.as_view(), name='soldier-list'),  # List soldiers
    path('soldiers/create/', SoldierCreateView.as_view(), name='soldier-create'),  # Create soldier
    path('soldiers/<int:pk>/', SoldierDetailView.as_view(), name='soldier-detail'),  # Soldier detail
    path('soldiers/<int:pk>/edit/', SoldierUpdateView.as_view(), name='soldier-edit'),  # Soldier update
    path('soldiers/<int:pk>/delete/', SoldierDeleteView.as_view(), name='soldier-delete'),  # Soldier delete

    #  Equipment URLs
    path('equipment/', EquipmentListView.as_view(), name='equipment-list'),  # List equipment
    path('equipment/create/', EquipmentCreateView.as_view(), name='equipment-create'),  # Create equipment
    path('equipment/<int:pk>/', EquipmentRetrieveUpdateDeleteView.as_view(), name='equipment-detail'),  # Equipment detail

    #  Readiness Report URLs
    path('reports/', ReadinessReportListView.as_view(), name='readiness-list'),  # List reports
    path('reports/create/', ReadinessReportCreateView.as_view(), name='readiness-create'),  # Create report
    path('reports/<int:pk>/', ReadinessReportRetrieveUpdateDeleteView.as_view(), name='readiness-detail'),  # Report detail

    #  Authentication URLs
    path("accounts/login/", CustomLoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),

    #  Password Reset URLs
    path("accounts/password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("accounts/password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("accounts/reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("accounts/reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    #  Password Change URLs
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),

    #  Registration URL
    path('accounts/register/', RegisterView.as_view(), name='register'),

    # Profile URLs
    path('accounts/profile/', ProfileView.as_view(), name='profile'),  # View profile
    path('accounts/profile/edit/', profile_edit_view, name='profile-edit'),  # Edit profile

    #  Role-based Access Control (RBAC) URLs
    path('dashboard/admin/', AdminDashboardView.as_view(), name='admin-dashboard'),  # Admin Dashboard (Admin role required)
    path('medical-officer/dashboard/', MedicalOfficerDashboardView.as_view(), name='medical-officer-dashboard'),  # Medical Officer Dashboard (Medical Officer role required)

    path('dashboard/', dashboard_view, name='dashboard'),

    # Mission URLs
    path('missions/', MissionListView.as_view(), name='mission-list'),
    path('missions/create/', MissionCreateView.as_view(), name='mission-create'),
    path('missions/<int:pk>/', MissionDetailView.as_view(), name='mission-detail'),
    path('missions/<int:pk>/edit/', MissionUpdateView.as_view(), name='mission-edit'),
    path('missions/<int:pk>/delete/', MissionDeleteView.as_view(), name='mission-delete'),

    # Readiness URLs
    path('readiness/', include(('readiness.urls', 'readiness'), namespace='readiness')),
    path('verify/<uidb64>/<token>/', verify_view, name='verify'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
