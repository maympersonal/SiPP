from django.db import models
from django.conf import settings


class Project(models.Model):
    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('paused', 'En pausa'),
        ('completed', 'Completado'),
    ]
    AREA_TYPE_CHOICES = [
        ('facultad', 'Facultad'),
        ('centro_investigacion', 'Centro de Investigación'),
        ('departamento', 'Departamento'),
        ('direccion', 'Dirección'),
        ('unidad', 'Unidad'),
        ('otro', 'Otro'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    costCenter = models.CharField(max_length=50, verbose_name='Centro de Costo')
    projectNumber = models.CharField(max_length=50, verbose_name='Número de Proyecto')
    budget = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    area = models.CharField(max_length=255, blank=True, null=True)
    areaType = models.CharField(max_length=30, choices=AREA_TYPE_CHOICES, default='facultad')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    endDate = models.DateField(blank=True, null=True, verbose_name='Fecha de Fin')
    renewalDate = models.DateField(blank=True, null=True, verbose_name='Fecha de Renovación')
    budgetPeriod = models.CharField(max_length=20, blank=True, null=True, verbose_name='Período Presupuestario')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_projects'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
        ordering = ['-created_at']
        unique_together = [['costCenter', 'projectNumber']]

    def __str__(self):
        return f'{self.costCenter} - {self.projectNumber}: {self.name}'


class BudgetHistory(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='budget_history')
    budget = models.DecimalField(max_digits=15, decimal_places=2)
    period = models.CharField(max_length=20)
    periodEnd = models.DateField()
    syncedAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Historial de Presupuesto'
        verbose_name_plural = 'Historiales de Presupuesto'
        ordering = ['-syncedAt']

    def __str__(self):
        return f'{self.project.costCenter} - {self.period}: {self.budget} CUP'
