from rest_framework import viewsets, filters, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from apps.messages_app.models import HelpRequest, FAQ
from api.v1.serializers.help_serializers import HelpRequestSerializer, FAQSerializer


class HelpRequestViewSet(viewsets.ModelViewSet):
    serializer_class = HelpRequestSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority']
    search_fields = ['subject', 'message']
    ordering = ['-created_at']

    def get_queryset(self):
        return HelpRequest.objects.select_related('user').all()

    def perform_create(self, serializer):
        serializer.save()


class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FAQSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['question', 'answer']
    ordering = ['category', 'order']

    def get_queryset(self):
        return FAQ.objects.filter(is_active=True)