from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from .models import User, Area

# Formulario personalizado para User
class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cargar áreas agrupadas por tipo
        areas = Area.objects.all().order_by('area_type', 'name')
        choices = [('', '---------')]
        for area in areas:
            label = f'{area.get_area_type_display()} - {area.name}'
            choices.append((area.name, label))
        self.fields['area'].widget = forms.Select(choices=choices)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserAdminForm
    list_display = ('email', 'fullName', 'role', 'area', 'areaType', 'is_active', 'created_at')
    list_filter = ('role', 'areaType', 'is_active')
    search_fields = ('email', 'fullName', 'area')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Información Personal', {'fields': ('email', 'fullName', 'password')}),
        ('Rol y Área', {'fields': ('role', 'areaType', 'area')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('created_at', 'updated_at', 'last_login')}),
    )
    add_fieldsets = (
        ('Nuevo Usuario', {
            'classes': ('wide',),
            'fields': ('email', 'fullName', 'password1', 'password2', 'role', 'areaType', 'area'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'area_type')
    list_filter = ('area_type',)
    search_fields = ('name',)