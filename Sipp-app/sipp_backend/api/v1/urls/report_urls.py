from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.v1.views.report_views import OrderReportViewSet, ReportViewSet, ActaConformidadViewSet

router = DefaultRouter()
router.register(r'orders', OrderReportViewSet, basename='order-report')
router.register(r'reports', ReportViewSet, basename='report')
router.register(r'actas', ActaConformidadViewSet, basename='acta')

urlpatterns = [
    path('', include(router.urls)),
]
