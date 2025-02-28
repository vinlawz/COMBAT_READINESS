from django.contrib import admin
from django.urls import path
from .views import (
    SoldierListView, SoldierCreateView, SoldierRetrieveUpdateDeleteView,
    EquipmentListView, EquipmentCreateView, EquipmentRetrieveUpdateDeleteView,
    ReadinessReportListView, ReadinessReportCreateView, ReadinessReportRetrieveUpdateDeleteView,
    HomeView
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),  # Home page route

    # Soldier URLs
    path('api/soldiers/', SoldierListView.as_view(), name='soldier-list'),
    path('api/soldiers/create/', SoldierCreateView.as_view(), name='soldier-create'),
    path('api/soldiers/<int:pk>/', SoldierRetrieveUpdateDeleteView.as_view(), name='soldier-detail'),

    # Equipment URLs
    path('api/equipment/', EquipmentListView.as_view(), name='equipment-list'),
    path('api/equipment/create/', EquipmentCreateView.as_view(), name='equipment-create'),
    path('api/equipment/<int:pk>/', EquipmentRetrieveUpdateDeleteView.as_view(), name='equipment-detail'),

    # Readiness Report URLs
    path('api/reports/', ReadinessReportListView.as_view(), name='readiness-list'),
    path('api/reports/create/', ReadinessReportCreateView.as_view(), name='readiness-create'),
    path('api/reports/<int:pk>/', ReadinessReportRetrieveUpdateDeleteView.as_view(), name='readiness-detail'),

    # Authentication URLs
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
]