from django.db import models
from django.conf import settings


class HelpRequest(models.Model):
    STATUS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('resuelto', 'Resuelto'),
        ('cerrado', 'Cerrado'),
    ]
    PRIORITY_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='help_requests')
    subject = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendiente')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='media')
    admin_response = models.TextField(blank=True, null=True)
    responded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='responded_help_requests'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Solicitud de Ayuda'
        verbose_name_plural = 'Solicitudes de Ayuda'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.subject} - {self.user.fullName}'


class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ('navegacion', 'Navegación'),
        ('proyectos', 'Proyectos'),
        ('pedidos', 'Pedidos'),
        ('reportes', 'Reportes'),
        ('mensajes', 'Mensajes'),
        ('soporte', 'Soporte'),
        ('general', 'General'),
    ]

    question = models.CharField(max_length=500)
    answer = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='general')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
        ordering = ['category', 'order']

    def __str__(self):
        return self.question[:80]
