from django.contrib import admin
from django.urls import path
from .views import soldier_list, equipment_list, home
from .views import (
    SoldierListCreateView, SoldierRetrieveUpdateDeleteView,
    EquipmentListCreateView, EquipmentRetrieveUpdateDeleteView,
    ReadinessReportListCreateView, ReadinessReportRetrieveUpdateDeleteView
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Home page route
    path('soldiers/', soldier_list, name='soldier_list'),
    path('equipment/', equipment_list, name='equipment_list'),

    # API Endpoints
    path('api/soldiers/', SoldierListCreateView.as_view(), name='soldier-list-create'),
    path('api/soldiers/<int:pk>/', SoldierRetrieveUpdateDeleteView.as_view(), name='soldier-detail'),

    path('api/equipment/', EquipmentListCreateView.as_view(), name='equipment-list-create'),
    path('api/equipment/<int:pk>/', EquipmentRetrieveUpdateDeleteView.as_view(), name='equipment-detail'),

    path('api/reports/', ReadinessReportListCreateView.as_view(), name='readiness-list-create'),
    path('api/reports/<int:pk>/', ReadinessReportRetrieveUpdateDeleteView.as_view(), name='readiness-detail'),

     path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
]
