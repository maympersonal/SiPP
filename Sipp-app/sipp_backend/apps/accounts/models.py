from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('vicerrector', 'Vicerrector'),
        ('decano', 'Decano'),
        ('director_centro', 'Director de Centro de Investigación'),
        ('director_area', 'Director de Área Central'),
        ('comercial', 'Comercial'),
        ('user', 'Jefe de Proyecto'),
    ]
    AREA_TYPE_CHOICES = [
        ('facultad', 'Facultad'),
        ('centro_investigacion', 'Centro de Investigación'),
        ('departamento', 'Departamento'),
        ('direccion', 'Dirección'),
        ('unidad', 'Unidad'),
        ('otro', 'Otro'),
    ]

    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    fullName = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    area = models.CharField(max_length=255, blank=True, null=True)
    areaType = models.CharField(max_length=30, choices=AREA_TYPE_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullName']

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.fullName} ({self.email})'

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

# Agregar al final del archivo existente
class Area(models.Model):
    AREA_TYPE_CHOICES = [
        ('facultad', 'Facultad'),
        ('centro_investigacion', 'Centro de Investigación'),
        ('departamento', 'Departamento'),
        ('direccion', 'Dirección'),
        ('unidad', 'Unidad'),
        ('otro', 'Otro'),
    ]
    
    name = models.CharField(max_length=255)
    area_type = models.CharField(max_length=30, choices=AREA_TYPE_CHOICES)
    
    class Meta:
        verbose_name = 'Área'
        verbose_name_plural = 'Áreas'
        ordering = ['area_type', 'name']
        unique_together = ['name', 'area_type']
    
    def __str__(self):
        return f'{self.get_area_type_display()} - {self.name}'

