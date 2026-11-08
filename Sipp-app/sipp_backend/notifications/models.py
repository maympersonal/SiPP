from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Notification(models.Model):
    """Modelo principal de notificaciones del sistema"""
    
    NOTIFICATION_TYPES = [
        ('order_created', 'Pedido Creado'),
        ('order_completed', 'Pedido Completado'),
        ('order_denied', 'Pedido Denegado'),
        ('order_updated', 'Pedido Actualizado'),
        ('conectividad_created', 'Servicio de Conectividad Creado'),
        ('conectividad_updated', 'Servicio de Conectividad Actualizado'),
        ('conectividad_delivered', 'Servicio Entregado'),
        ('project_created', 'Proyecto Creado'),
        ('project_updated', 'Proyecto Actualizado'),
        ('user_registered', 'Usuario Registrado'),
        ('user_updated', 'Usuario Actualizado'),
        ('system', 'Notificación del Sistema'),
        ('warning', 'Advertencia'),
        ('info', 'Información'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta'),
        ('urgent', 'Urgente'),
    ]
    
    # Usuario destinatario
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='notifications',
        verbose_name='Usuario'
    )
    
    # Tipo de notificación
    notification_type = models.CharField(
        max_length=50, 
        choices=NOTIFICATION_TYPES,
        default='info',
        verbose_name='Tipo'
    )
    
    # Prioridad
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
        verbose_name='Prioridad'
    )
    
    # Contenido
    title = models.CharField(max_length=255, verbose_name='Título')
    message = models.TextField(verbose_name='Mensaje')
    
    # Metadatos
    link = models.CharField(max_length=500, blank=True, null=True, verbose_name='Enlace')
    source_id = models.IntegerField(blank=True, null=True, verbose_name='ID de Origen')
    source_type = models.CharField(max_length=50, blank=True, null=True, verbose_name='Tipo de Origen')
    
    # Estados
    is_read = models.BooleanField(default=False, verbose_name='Leído')
    is_sent = models.BooleanField(default=False, verbose_name='Enviado')
    
    # Marcas de tiempo
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    read_at = models.DateTimeField(blank=True, null=True, verbose_name='Leído en')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado')
    
    class Meta:
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['notification_type']),
        ]
    
    def __str__(self):
        return f'{self.get_notification_type_display()} - {self.user.username}'
    
    def mark_as_read(self):
        """Marcar notificación como leída"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
    
    @classmethod
    def create_notification(cls, user, notification_type, title, message, 
                           priority='medium', link=None, source_id=None, 
                           source_type=None):
        """Método factory para crear notificaciones"""
        notification = cls.objects.create(
            user=user,
            notification_type=notification_type,
            priority=priority,
            title=title,
            message=message,
            link=link,
            source_id=source_id,
            source_type=source_type
        )
        return notification