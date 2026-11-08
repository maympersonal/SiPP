# notifications/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()

@receiver(post_save, sender='orders.Order')
def notify_order_changes(sender, instance, created, **kwargs):
    """Notificar cuando se crea o modifica un pedido"""
    if created:
        admins = User.objects.filter(role='admin', is_active=True)
        for admin in admins:
            Notification.objects.create(
                user=admin,
                notification_type='order_created',
                priority='high',
                title='Nuevo Pedido Recibido',
                message=f'Se ha creado un nuevo pedido.',
                link='/pedidos',
                source_id=instance.id,
                source_type='order'
            )
    else:
        # Notificar cambio de estado
        if hasattr(instance, 'tracker') and instance.tracker.has_changed('status'):
            if instance.status == 'Completado':
                for admin in User.objects.filter(role='admin', is_active=True):
                    Notification.objects.create(
                        user=admin,
                        notification_type='order_completed',
                        priority='medium',
                        title='Pedido Completado',
                        message=f'El pedido #{instance.id} ha sido completado.',
                        link='/pedidos',
                        source_id=instance.id,
                        source_type='order'
                    )


@receiver(post_save, sender='conectividad.ServicioConectividad')
def notify_conectividad_changes(sender, instance, created, **kwargs):
    """Notificar cambios en servicios de conectividad"""
    admins = User.objects.filter(role='admin', is_active=True)
    
    if created:
        for admin in admins:
            Notification.objects.create(
                user=admin,
                notification_type='conectividad_created',
                priority='medium',
                title='Nuevo Servicio de Conectividad',
                message=f'Se ha asignado {instance.tipo} para {instance.titular}.',
                link='/conectividad',
                source_id=instance.id,
                source_type='conectividad'
            )
    
    # Notificar cuando se marca como entregado
    if not created and instance.entregado:
        for admin in admins:
            Notification.objects.create(
                user=admin,
                notification_type='conectividad_delivered',
                priority='high',
                title='Servicio Entregado',
                message=f'{instance.tipo} para {instance.titular} ha sido entregado.',
                link='/conectividad',
                source_id=instance.id,
                source_type='conectividad'
            )