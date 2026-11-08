from django.contrib import admin
from .models import Empresa, Producto, Servicio, PedidoExtra


class ProductoInline(admin.TabularInline):
    model = Producto
    extra = 0


class ServicioInline(admin.TabularInline):
    model = Servicio
    extra = 0


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'encargado', 'activo', 'created_at')
    list_filter = ('activo',)
    search_fields = ('nombre',)
    inlines = [ProductoInline, ServicioInline]


@admin.register(PedidoExtra)
class PedidoExtraAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'proyecto', 'tipo', 'estado', 'created_at')
    list_filter = ('estado', 'tipo')
    search_fields = ('usuario__fullName', 'descripcion')