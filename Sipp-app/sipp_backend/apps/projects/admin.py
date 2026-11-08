from django.contrib import admin
from django import forms
from .models import Project, BudgetHistory
from apps.accounts.models import Area

class ProjectAdminForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cargar áreas disponibles
        areas = Area.objects.all().order_by('area_type', 'name')
        choices = [('', '---------')]
        for area in areas:
            label = f'{area.get_area_type_display()} - {area.name}'
            choices.append((area.name, label))
        self.fields['area'].widget = forms.Select(choices=choices)


class BudgetHistoryInline(admin.TabularInline):
    model = BudgetHistory
    extra = 0
    readonly_fields = ('budget', 'period', 'periodEnd', 'syncedAt')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    list_display = ('costCenter', 'projectNumber', 'name', 'owner', 'budget', 'area', 'status')
    list_filter = ('status', 'areaType', 'area')
    search_fields = ('costCenter', 'projectNumber', 'name', 'owner__fullName')
    inlines = [BudgetHistoryInline]
    readonly_fields = ('created_at', 'updated_at')