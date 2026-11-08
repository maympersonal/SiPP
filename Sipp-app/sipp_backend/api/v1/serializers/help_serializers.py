from rest_framework import serializers
from apps.messages_app.models import HelpRequest, FAQ


class HelpRequestSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.fullName', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = HelpRequest
        fields = [
            'id', 'user', 'user_name', 'user_email', 'subject', 'message',
            'status', 'priority', 'admin_response', 'created_at', 'resolved_at'
        ]
        read_only_fields = ['id', 'user', 'status', 'admin_response', 'created_at', 'resolved_at']


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'category', 'order']
