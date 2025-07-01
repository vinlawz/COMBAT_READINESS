# urls.py

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import (
    SoldierListView, SoldierCreateView, SoldierRetrieveUpdateDeleteView,
    EquipmentListView, EquipmentCreateView, EquipmentRetrieveUpdateDeleteView,
    ReadinessReportListView, ReadinessReportCreateView, ReadinessReportRetrieveUpdateDeleteView,
    HomeView, RegisterView, ProfileView, profile_edit_view, AdminDashboardView, MedicalOfficerDashboardView,
    dashboard_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),

    # 🔰 Soldier URLs
    path('soldiers/', SoldierListView.as_view(), name='soldier-list'),  # List soldiers
    path('soldiers/create/', SoldierCreateView.as_view(), name='soldier-create'),  # Create soldier
    path('soldiers/<int:pk>/', SoldierRetrieveUpdateDeleteView.as_view(), name='soldier-detail'),  # Soldier detail

    # 🔰 Equipment URLs
    path('equipment/', EquipmentListView.as_view(), name='equipment-list'),  # List equipment
    path('equipment/create/', EquipmentCreateView.as_view(), name='equipment-create'),  # Create equipment
    path('equipment/<int:pk>/', EquipmentRetrieveUpdateDeleteView.as_view(), name='equipment-detail'),  # Equipment detail

    # 🔰 Readiness Report URLs
    path('reports/', ReadinessReportListView.as_view(), name='readiness-list'),  # List reports
    path('reports/create/', ReadinessReportCreateView.as_view(), name='readiness-create'),  # Create report
    path('reports/<int:pk>/', ReadinessReportRetrieveUpdateDeleteView.as_view(), name='readiness-detail'),  # Report detail

    # 🔐 Authentication URLs
    path("accounts/login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),

    # 🔐 Password Reset URLs
    path("accounts/password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("accounts/password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("accounts/reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("accounts/reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    # 📝 Registration URL
    path('accounts/register/', RegisterView.as_view(), name='register'),

    # 🔐 Profile URLs
    path('accounts/profile/', ProfileView.as_view(), name='profile'),  # View profile
    path('accounts/profile/edit/', profile_edit_view, name='profile-edit'),  # Edit profile

    # 🚨 Role-based Access Control (RBAC) URLs
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),  # Admin Dashboard (Admin role required)
    path('medical-officer/dashboard/', MedicalOfficerDashboardView.as_view(), name='medical-officer-dashboard'),  # Medical Officer Dashboard (Medical Officer role required)

    path('dashboard/', dashboard_view, name='dashboard'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
