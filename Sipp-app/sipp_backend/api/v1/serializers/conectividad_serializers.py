# api/v1/serializers/conectividad_serializers.py
from rest_framework import serializers
from conectividad.models import ServicioConectividad

class ServicioConectividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicioConectividad
        fields = '__all__'