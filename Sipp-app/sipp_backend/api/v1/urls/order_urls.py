# sipp_backend/api/v1/urls/order_urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.v1.views.order_views import OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]