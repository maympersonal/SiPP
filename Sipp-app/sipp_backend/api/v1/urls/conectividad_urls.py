from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.v1.views.conectividad_views import ServicioConectividadViewSet

router = DefaultRouter()
router.register(r'conectividad', ServicioConectividadViewSet, basename='conectividad')

urlpatterns = [path('', include(router.urls))]
