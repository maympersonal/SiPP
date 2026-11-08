# sipp_backend/api/v1/serializers/order_serializers.py
from rest_framework import serializers
from apps.orders.models import Order


class OrderItemSerializer(serializers.Serializer):
    """Serializador para items individuales del pedido"""
    id = serializers.IntegerField(required=False)
    type = serializers.ChoiceField(choices=[('product', 'Producto'), ('service', 'Servicio')], required=True)
    name = serializers.CharField(max_length=255)
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    currency = serializers.CharField(max_length=10, required=False, default='CUP')

    def validate(self, data):
        quantity = data.get('quantity', 1)
        price = data.get('price', 0)
        data['subtotal'] = float(quantity) * float(price)
        return data


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializador para crear pedidos con productos y servicios separados"""
    items = serializers.ListField(child=serializers.DictField())
    project_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'project_id', 'order_type', 'status',
            'items', 'total', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'status', 'total', 'created_at']

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("El pedido debe tener al menos un item")

        validated_items = []
        for item in items:
            if 'type' not in item:
                raise serializers.ValidationError("Cada item debe tener un tipo (product/service)")
            if item['type'] not in ['product', 'service']:
                raise serializers.ValidationError("Tipo inválido. Debe ser 'product' o 'service'")
            if 'name' not in item or not item['name']:
                raise serializers.ValidationError("Cada item debe tener un nombre")
            if 'quantity' not in item or item['quantity'] < 1:
                raise serializers.ValidationError("La cantidad debe ser al menos 1")
            if 'price' not in item or float(item['price']) < 0:
                raise serializers.ValidationError("El precio debe ser mayor o igual a 0")

            # Calcular subtotal
            item['subtotal'] = float(item['quantity']) * float(item['price'])
            validated_items.append(item)

        return validated_items

    def create(self, validated_data):
        items = validated_data.pop('items')
        project_id = validated_data.pop('project_id', None)

        # Calcular total
        total = sum(float(item['subtotal']) for item in items)

        # Determinar order_type basado en los items
        has_products = any(item['type'] == 'product' for item in items)
        has_services = any(item['type'] == 'service' for item in items)

        if has_products and has_services:
            order_type = 'special'
        elif has_services:
            order_type = 'special'
        else:
            order_type = 'regular'

        validated_data['order_type'] = order_type
        validated_data['total'] = total

        # Manejar proyecto
        if project_id:
            from apps.projects.models import Project
            try:
                validated_data['project'] = Project.objects.get(id=project_id)
            except Project.DoesNotExist:
                validated_data['project'] = None
        else:
            validated_data['project'] = None

        # El usuario se asigna desde la vista
        user = validated_data.pop('user', None)

        order = Order.objects.create(**validated_data, user=user)
        order.items = items
        order.save()

        return order


class OrderDetailSerializer(serializers.ModelSerializer):
    """Serializador para mostrar detalles del pedido"""
    user_name = serializers.CharField(source='user.fullName', read_only=True)
    project_name = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()
    services = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'user_name', 'project', 'project_name',
            'order_type', 'status', 'products', 'services',
            'total', 'currency', 'notes', 'completed_at', 'created_at', 'updated_at'
        ]

    def get_project_name(self, obj):
        if obj.project:
            return f'{obj.project.costCenter} - {obj.project.projectNumber}: {obj.project.name}'
        return 'Pedido Extra'

    def get_products(self, obj):
        """Retorna solo los items de tipo producto"""
        if isinstance(obj.items, list):
            return [item for item in obj.items if item.get('type') == 'product']
        return []

    def get_services(self, obj):
        """Retorna solo los items de tipo servicio"""
        if isinstance(obj.items, list):
            return [item for item in obj.items if item.get('type') == 'service']
        return []

    def get_currency(self, obj):
        """Obtener moneda del primer item o default"""
        if isinstance(obj.items, list) and obj.items:
            return obj.items[0].get('currency', 'CUP')
        return 'CUP'