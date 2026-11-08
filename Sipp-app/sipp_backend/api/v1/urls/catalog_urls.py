from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.v1.views.catalog_views import EmpresaViewSet, ProductoViewSet, ServicioViewSet, PedidoExtraViewSet

router = DefaultRouter()
router.register(r'empresas', EmpresaViewSet, basename='empresa')
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'servicios', ServicioViewSet, basename='servicio')
router.register(r'pedidos-extra', PedidoExtraViewSet, basename='pedido-extra')

urlpatterns = [
    path('', include(router.urls)),
]
