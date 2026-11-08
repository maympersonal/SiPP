from django.contrib import admin
from .models import HelpRequest, FAQ


@admin.register(HelpRequest)
class HelpRequestAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'status', 'priority', 'created_at', 'resolved_at')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('subject', 'message', 'user__fullName', 'user__email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Información de la Solicitud', {'fields': ('user', 'subject', 'message')}),
        ('Estado y Prioridad', {'fields': ('status', 'priority')}),
        ('Respuesta', {'fields': ('admin_response', 'responded_by')}),
        ('Fechas', {'fields': ('created_at', 'updated_at', 'resolved_at')}),
    )

    def save_model(self, request, obj, form, change):
        if obj.admin_response and not obj.responded_by:
            obj.responded_by = request.user
        if obj.status == 'resuelto' and not obj.resolved_at:
            from django.utils import timezone
            obj.resolved_at = timezone.now()
        super().save_model(request, obj, form, change)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('question', 'answer')
    ordering = ('category', 'order')
    list_editable = ('order', 'is_active')
