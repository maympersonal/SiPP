# apps/accounts/urls.py
from django.urls import path
from .views import (
    LoginView, 
    LogoutView, 
    MeView, 
    CsrfTokenView, 
    HealthCheckView,
    UserListView,
    UserDetailView
)

urlpatterns = [
    # Autenticación
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),
    path('csrf/', CsrfTokenView.as_view(), name='csrf'),
    path('health/', HealthCheckView.as_view(), name='health'),
    
    # Usuarios
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]