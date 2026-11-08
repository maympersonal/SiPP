from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.v1.views.help_views import HelpRequestViewSet, FAQViewSet

router = DefaultRouter()
router.register(r'help-requests', HelpRequestViewSet, basename='help-request')
router.register(r'faqs', FAQViewSet, basename='faq')

urlpatterns = [
    path('', include(router.urls)),
]
