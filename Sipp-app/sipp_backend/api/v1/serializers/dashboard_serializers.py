from rest_framework import serializers
from apps.orders.models import Order
from apps.projects.models import Project
from apps.accounts.models import User


class DashboardStatsSerializer(serializers.Serializer):
    total_pedidos = serializers.IntegerField()
    pedidos_pendientes = serializers.IntegerField()
    pedidos_completados = serializers.IntegerField()
    pedidos_en_proceso = serializers.IntegerField()
    pedidos_denegados = serializers.IntegerField()
    presupuesto_total = serializers.DecimalField(max_digits=15, decimal_places=2)
    presupuesto_utilizado = serializers.DecimalField(max_digits=15, decimal_places=2)
    presupuesto_disponible = serializers.DecimalField(max_digits=15, decimal_places=2)
    usuarios_activos = serializers.IntegerField()
    proyectos_activos = serializers.IntegerField()
    total_usuarios = serializers.IntegerField()


class MonthlyTrendSerializer(serializers.Serializer):
    month = serializers.CharField()
    total_pedidos = serializers.IntegerField()
    completados = serializers.IntegerField()
    pendientes = serializers.IntegerField()
    monto_total = serializers.DecimalField(max_digits=15, decimal_places=2)


class TopProjectSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField()
    cost_center = serializers.CharField()
    pedidos = serializers.IntegerField()
    presupuesto = serializers.DecimalField(max_digits=15, decimal_places=2)
    gastado = serializers.DecimalField(max_digits=15, decimal_places=2)
    porcentaje = serializers.FloatField()


class RecentOrderSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.fullName')
    project_name = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user_name', 'project_name', 'order_type', 'status', 'total', 'created_at']

    def get_project_name(self, obj):
        if obj.project:
            return f'{obj.project.costCenter} - {obj.project.projectNumber}'
        return 'Pedido Extra'
