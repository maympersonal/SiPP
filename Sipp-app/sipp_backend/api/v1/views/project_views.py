from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from apps.projects.models import Project, BudgetHistory
from api.v1.serializers.project_serializers import (
    ProjectListSerializer, ProjectDetailSerializer, ProjectCreateUpdateSerializer
)


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'areaType', 'area']
    search_fields = ['costCenter', 'projectNumber', 'name', 'owner__fullName']
    ordering_fields = ['costCenter', 'budget', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        elif self.action in ['retrieve', 'details']:
            return ProjectDetailSerializer
        return ProjectCreateUpdateSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Project.objects.select_related('owner').all()
        if user.role == 'admin':
            return Project.objects.select_related('owner').all()
        if user.role == 'user':
            return Project.objects.select_related('owner').filter(owner=user)
        return Project.objects.none()

    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        project = self.get_object()
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)