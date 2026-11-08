from django.db import models
from django.conf import settings
from apps.orders.models import Order


class Report(models.Model):
    REPORT_TYPE_CHOICES = [
        ('general', 'Reporte General'),
        ('selected', 'Reporte Seleccionado'),
        ('acta', 'Acta de Conformidad'),
    ]

    title = models.CharField(max_length=255)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES, default='general')
    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='reports',
        null=True,  
        blank=True 
    )
    filters_applied = models.JSONField(default=dict, blank=True)
    orders_count = models.IntegerField(default=0)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Reporte'
        verbose_name_plural = 'Reportes'
        ordering = ['-created_at']


class ActaConformidad(models.Model):
    project_name = models.CharField(max_length=255)
    project_code = models.CharField(max_length=100, blank=True, null=True)
    client_name = models.CharField(max_length=255)
    client_email = models.EmailField(blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    items = models.JSONField(default=list)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Acta de Conformidad'
        verbose_name_plural = 'Actas de Conformidad'
        ordering = ['-created_at']