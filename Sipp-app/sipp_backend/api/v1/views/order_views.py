# sipp_backend/api/v1/views/order_views.py
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from apps.orders.models import Order
from api.v1.serializers.order_serializers import (
    OrderCreateSerializer,
    OrderDetailSerializer,
)


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar pedidos (Orders)
    """
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'order_type', 'user']
    search_fields = ['user__fullName', 'user__email', 'project__name', 'notes']
    ordering_fields = ['created_at', 'total', 'status']
    ordering = ['-created_at']

    def get_queryset(self):
        """Obtener queryset con relaciones optimizadas"""
        return Order.objects.select_related('user', 'project').all()

    def get_serializer_class(self):
        """Usar diferente serializador según la acción"""
        if self.action in ['create', 'update', 'partial_update']:
            return OrderCreateSerializer
        return OrderDetailSerializer

    def create(self, request, *args, **kwargs):
        """
        Crear un nuevo pedido
        """
        # Copiar datos del request
        data = request.data.copy()

        # Si no se envía user, usar el usuario autenticado
        if 'user' not in data:
            if request.user and request.user.is_authenticated:
                data['user'] = request.user.id
            else:
                # Para pruebas sin autenticación, usar el primer usuario disponible
                from django.contrib.auth import get_user_model
                User = get_user_model()
                first_user = User.objects.first()
                if first_user:
                    data['user'] = first_user.id
                else:
                    return Response(
                        {'error': 'No hay usuario disponible para crear el pedido'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            order = serializer.save()
            return Response(
                OrderDetailSerializer(order).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """
        Actualizar el estado de un pedido
        """
        order = self.get_object()
        new_status = request.data.get('status')

        if not new_status:
            return Response(
                {'error': 'El campo status es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )

        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return Response(
                {'error': f'Estado inválido. Opciones: {", ".join(valid_statuses)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        if new_status == 'Completado':
            from django.utils import timezone
            order.completed_at = timezone.now()
        order.save()

        return Response(
            OrderDetailSerializer(order).data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['delete'])
    def delete_order(self, request, pk=None):
        """
        Eliminar un pedido (soft delete opcional)
        """
        order = self.get_object()
        order.delete()
        return Response(
            {'message': 'Pedido eliminado correctamente'},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        """
        Obtener pedidos del usuario autenticado
        """
        if not request.user or not request.user.is_authenticated:
            return Response(
                {'error': 'Usuario no autenticado'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        orders = Order.objects.filter(user=request.user).select_related('user', 'project')
        serializer = OrderDetailSerializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """
        Obtener pedidos pendientes
        """
        orders = self.get_queryset().filter(status='Pendiente')
        serializer = OrderDetailSerializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Obtener estadísticas de pedidos
        """
        total = Order.objects.count()
        pending = Order.objects.filter(status='Pendiente').count()
        in_progress = Order.objects.filter(status='En proceso').count()
        completed = Order.objects.filter(status='Completado').count()
        denied = Order.objects.filter(status='Denegado').count()

        # Total por tipo
        regular = Order.objects.filter(order_type='regular').count()
        special = Order.objects.filter(order_type='special').count()

        # Total por moneda (si tienes campo moneda)
        # Si no tienes campo moneda, puedes omitirlo

        return Response({
            'total': total,
            'pending': pending,
            'in_progress': in_progress,
            'completed': completed,
            'denied': denied,
            'by_type': {
                'regular': regular,
                'special': special,
            },
        })