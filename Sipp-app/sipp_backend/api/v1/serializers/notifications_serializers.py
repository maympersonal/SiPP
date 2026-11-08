from rest_framework import serializers
from notifications.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    """Serializer para notificaciones"""
    
    notification_type_display = serializers.CharField(
        source='get_notification_type_display', 
        read_only=True
    )
    priority_display = serializers.CharField(
        source='get_priority_display', 
        read_only=True
    )
    time_ago = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'user_name', 'notification_type', 'notification_type_display',
            'priority', 'priority_display', 'title', 'message', 'link',
            'source_id', 'source_type', 'is_read', 'is_sent',
            'created_at', 'read_at', 'updated_at', 'time_ago'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'read_at']
    
    def get_time_ago(self, obj):
        """Calcular tiempo transcurrido en formato legible"""
        from django.utils import timezone
        import datetime
        
        now = timezone.now()
        diff = now - obj.created_at
        
        if diff < datetime.timedelta(minutes=1):
            return 'Ahora mismo'
        elif diff < datetime.timedelta(hours=1):
            minutes = int(diff.total_seconds() / 60)
            return f'Hace {minutes} min'
        elif diff < datetime.timedelta(days=1):
            hours = int(diff.total_seconds() / 3600)
            return f'Hace {hours} h'
        elif diff < datetime.timedelta(days=30):
            days = diff.days
            return f'Hace {days} día{"s" if days != 1 else ""}'
        else:
            return obj.created_at.strftime('%d/%m/%Y')
    
    def get_user_name(self, obj):
        """Obtener nombre del usuario"""
        if obj.user:
            return obj.user.get_full_name() or obj.user.username
        return None