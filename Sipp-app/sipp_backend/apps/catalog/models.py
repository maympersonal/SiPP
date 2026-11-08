from django.db import models
from django.conf import settings


class Empresa(models.Model):
    nombre = models.CharField(max_length=255)
    encargado = models.CharField(max_length=255, blank=True, null=True)
    tipo_negocio = models.CharField(max_length=100, blank=True, null=True)  # NUEVO
    website = models.URLField(blank=True, null=True)
    moneda = models.CharField(max_length=10, default='CUP')  # NUEVO
    activo = models.BooleanField(default=True)
    contactos = models.JSONField(default=list, blank=True)  # NUEVO
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='productos')
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=100, blank=True, null=True)
    precio = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    caracteristicas = models.JSONField(default=list, blank=True)
    categoria = models.CharField(max_length=100, blank=True, null=True)  # <-- IMPORTANTE
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return f'{self.nombre} - {self.empresa.nombre}'


class Servicio(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='servicios')
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'

    def __str__(self):
        return f'{self.nombre} - {self.empresa.nombre}'


class PedidoExtra(models.Model):
    STATUS_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Aprobado', 'Aprobado'),
        ('Denegado', 'Denegado'),
    ]
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    proyecto = models.ForeignKey('projects.Project', on_delete=models.SET_NULL, null=True)
    tipo = models.CharField(max_length=20, choices=[('producto', 'Producto'), ('servicio', 'Servicio')])
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pendiente')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Pedido Extra'
        verbose_name_plural = 'Pedidos Extra'

    def __str__(self):
        return f'Pedido Extra #{self.id} - {self.usuario.fullName}'