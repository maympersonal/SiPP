from django.contrib import admin
from .models import Report, ActaConformidad


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_type', 'generated_by', 'orders_count', 'total_amount', 'created_at')
    list_filter = ('report_type', 'created_at')
    search_fields = ('title', 'generated_by__fullName', 'generated_by__email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


@admin.register(ActaConformidad)
class ActaConformidadAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'client_name', 'total', 'generated_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('project_name', 'client_name', 'project_code')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
