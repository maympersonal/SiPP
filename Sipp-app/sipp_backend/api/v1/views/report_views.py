from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from django.utils import timezone
from apps.orders.models import Order
from apps.reports_app.models import Report, ActaConformidad
from api.v1.serializers.report_serializers import (
    OrderReportSerializer, ReportSerializer, ActaConformidadSerializer
)
import datetime

class OrderReportViewSet(viewsets.ModelViewSet):
    serializer_class = OrderReportSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'order_type']
    search_fields = ['user__fullName', 'user__email']
    ordering_fields = ['total', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Order.objects.select_related('user', 'project').all()

    @action(detail=True, methods=['patch'])
    def mark_completed(self, request, pk=None):
        order = self.get_object()
        order.status = 'Completado'
        order.completed_at = timezone.now()
        order.save()
        return Response({'status': 'Completado', 'message': 'Pedido marcado como completado'})

    @action(detail=False, methods=['get'])
    def stats(self, request):
        orders = self.get_queryset()
        return Response({
            'total': orders.count(),
            'completed': orders.filter(status='Completado').count(),
            'pending': orders.filter(status__in=['Pendiente', 'En proceso']).count(),
            'total_amount': float(orders.aggregate(Sum('total'))['total__sum'] or 0),
        })


    @action(detail=False, methods=['get'])
    def export(self, request):
        orders = self.get_queryset()
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Report.objects.filter(generated_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(generated_by=self.request.user)


class ActaConformidadViewSet(viewsets.ModelViewSet):
    serializer_class = ActaConformidadSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return ActaConformidad.objects.all()

    def perform_create(self, serializer):
        serializer.save()


