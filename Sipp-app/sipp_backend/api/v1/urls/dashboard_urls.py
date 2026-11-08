# api/v1/urls/dashboard_urls.py
from django.urls import path
from api.v1.views.dashboard_views import DashboardView

urlpatterns = [
    path('dashboard/stats/', DashboardView.as_view(), name='dashboard-stats'),
]