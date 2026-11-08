from rest_framework import serializers
from apps.catalog.models import Empresa, Producto, Servicio, PedidoExtra


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'


class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'


class EmpresaSerializer(serializers.ModelSerializer):
    productos = ProductoSerializer(many=True, read_only=True)
    servicios = ServicioSerializer(many=True, read_only=True)

    class Meta:
        model = Empresa
        fields = '__all__'


class PedidoExtraSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.fullName', read_only=True)
    proyecto_nombre = serializers.SerializerMethodField()

    class Meta:
        model = PedidoExtra
        fields = '__all__'

    def get_proyecto_nombre(self, obj):
        if obj.proyecto:
            return f'{obj.proyecto.costCenter} - {obj.proyecto.projectNumber}'
        return 'N/A'
