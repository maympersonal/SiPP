from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'project', 'order_type', 'status', 'total', 'created_at')
    list_filter = ('status', 'order_type', 'created_at')
    search_fields = ('user__fullName', 'user__email', 'project__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Información del Pedido', {'fields': ('user', 'project', 'order_type', 'status')}),
        ('Detalles', {'fields': ('items', 'total', 'notes')}),
        ('Fechas', {'fields': ('completed_at', 'created_at', 'updated_at')}),
    )
