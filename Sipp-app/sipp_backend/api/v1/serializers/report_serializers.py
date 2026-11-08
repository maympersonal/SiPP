from rest_framework import serializers
from apps.reports_app.models import Report, ActaConformidad
from apps.orders.models import Order


class OrderReportSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.fullName', read_only=True)
    project_name = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()
    services = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'user_name', 'project', 'project_name',
            'order_type', 'status', 'products', 'services', 'items', 'total', 'notes',
            'completed_at', 'created_at', 'updated_at'
        ]

    def get_project_name(self, obj):
        if obj.project:
            return f'{obj.project.costCenter} - {obj.project.projectNumber}: {obj.project.name}'
        return 'Pedido Extra'
    
    def get_products(self, obj):
        """Retorna solo los items de tipo producto"""
        items = obj.items if isinstance(obj.items, list) else []
        return [item for item in items if item.get('type') == 'product']
    
    def get_services(self, obj):
        """Retorna solo los items de tipo servicio"""
        items = obj.items if isinstance(obj.items, list) else []
        return [item for item in items if item.get('type') == 'service']


class ReportSerializer(serializers.ModelSerializer):
    generated_by_name = serializers.CharField(source='generated_by.fullName', read_only=True)

    class Meta:
        model = Report
        fields = '__all__'


class ActaConformidadSerializer(serializers.ModelSerializer):
    generated_by_name = serializers.CharField(source='generated_by.fullName', read_only=True)

    class Meta:
        model = ActaConformidad
        fields = '__all__'