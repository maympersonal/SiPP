from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.v1.views.notifications_views import NotificationViewSet

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]