from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from django.utils import timezone
from notifications.models import Notification
from api.v1.serializers.notifications_serializers import NotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        print(f"DEBUG - User: {user}, Authenticated: {user.is_authenticated}, Email: {getattr(user, 'email', 'N/A')}")
        
        if not user.is_authenticated:
            return Notification.objects.none()
        
        # Si es admin, ver todas
        if hasattr(user, 'role') and user.role == 'admin':
            return Notification.objects.all().order_by('-created_at')
        
        return Notification.objects.filter(user=user).order_by('-created_at')
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        user = request.user
        print(f"DEBUG unread_count - User: {user}, Auth: {user.is_authenticated}")
        
        if not user.is_authenticated:
            return Response({'unread_count': 0})
        
        if hasattr(user, 'role') and user.role == 'admin':
            count = Notification.objects.filter(is_read=False).count()
        else:
            count = Notification.objects.filter(user=user, is_read=False).count()
        
        return Response({'unread_count': count})
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save(update_fields=['is_read', 'read_at'])
        return Response({'status': 'ok'})
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'status': 'error'}, status=403)
        
        if hasattr(user, 'role') and user.role == 'admin':
            Notification.objects.all().update(is_read=True, read_at=timezone.now())
        else:
            Notification.objects.filter(user=user, is_read=False).update(
                is_read=True, read_at=timezone.now()
            )
        
        return Response({'status': 'ok'})