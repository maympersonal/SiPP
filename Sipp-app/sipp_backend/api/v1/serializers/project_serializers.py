from rest_framework import serializers
from apps.projects.models import Project, BudgetHistory


class BudgetHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetHistory
        fields = ['id', 'budget', 'period', 'periodEnd', 'syncedAt']


from rest_framework import serializers
from apps.projects.models import Project, BudgetHistory


class ProjectListSerializer(serializers.ModelSerializer):
    owner_name = serializers.SerializerMethodField()
    owner_email = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'costCenter', 'projectNumber', 'budget',
            'area', 'areaType', 'status', 'endDate', 'renewalDate',
            'budgetPeriod', 'owner', 'owner_name', 'owner_email',
            'created_at', 'updated_at'
        ]

    def get_owner_name(self, obj):
        return obj.owner.fullName if obj.owner else 'Sin asignar'

    def get_owner_email(self, obj):
        return obj.owner.email if obj.owner else ''


class ProjectDetailSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.fullName', read_only=True)
    owner_email = serializers.CharField(source='owner.email', read_only=True)
    budget_history = BudgetHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


class ProjectCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'name', 'description', 'costCenter', 'projectNumber',
            'budget', 'area', 'areaType', 'status', 'endDate',
            'renewalDate', 'budgetPeriod', 'owner'
        ]
