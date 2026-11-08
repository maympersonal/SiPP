from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from apps.accounts.models import User
from api.v1.serializers.user_serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'areaType', 'is_active']
    search_fields = ['email', 'fullName', 'area']
    ordering_fields = ['fullName', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        # Si el usuario es anónimo (no autenticado), devolver todos los usuarios
        if not user.is_authenticated:
            return User.objects.filter(role='user')
        if user.role == 'admin':
            return User.objects.filter(role='user')
        return User.objects.filter(id=user.id)
        

    def perform_create(self, serializer):
        serializer.save(role='user')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.role == 'admin':
            return Response(
                {'error': 'No se puede eliminar un administrador'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
