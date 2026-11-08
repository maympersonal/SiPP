from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from apps.conectividad.models import ServicioConectividad
from api.v1.serializers.conectividad_serializers import ServicioConectividadSerializer

class ServicioConectividadViewSet(viewsets.ModelViewSet):
    serializer_class = ServicioConectividadSerializer
    permission_classes = [AllowAny]
    queryset = ServicioConectividad.objects.all()
