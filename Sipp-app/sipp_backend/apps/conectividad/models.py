from django.db import models

class ServicioConectividad(models.Model):
    TIPO_CHOICES = [
        ('nauta_hogar', 'Nauta Hogar'),
        ('sim', 'Tarjeta SIM'),
    ]
    entregado = models.BooleanField(
        default=False,
        verbose_name='Entregado'
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    titular = models.CharField(max_length=255)
    cargo = models.CharField(max_length=255, blank=True, null=True)
    area = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_asignacion = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Servicio de Conectividad'
        verbose_name_plural = 'Servicios de Conectividad'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.titular}'
