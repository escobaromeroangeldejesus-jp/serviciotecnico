from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Equipo(models.Model):
    TIPOS_EQUIPO = [
        ('PC', 'PC de Escritorio'),
        ('NOTEBOOK', 'Notebook'),
        ('NETBOOK', 'Netbook'),
        ('IMPRESORA', 'Impresora'),
        ('OTRO', 'Otro'),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='equipos'
    )

    tipo = models.CharField(max_length=20, choices=TIPOS_EQUIPO)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=100)
    numero_serie = models.CharField(max_length=100, blank=True)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"{self.tipo} - {self.marca} {self.modelo}"


class Tecnico(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    especialidad = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Reparacion(models.Model):

    ESTADOS = [
        ('INGRESADO', 'Ingresado'),
        ('DIAGNOSTICO', 'En diagnóstico'),
        ('REPARANDO', 'En reparación'),
        ('ESPERA', 'Esperando repuesto'),
        ('FINALIZADO', 'Finalizado'),
        ('ENTREGADO', 'Entregado'),
    ]

    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        related_name='reparaciones'
    )

    tecnico = models.ForeignKey(
        Tecnico,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reparaciones'
    )

    fecha_ingreso = models.DateField()
    fecha_entrega = models.DateField(null=True, blank=True)

    problema_reportado = models.TextField()
    diagnostico = models.TextField(blank=True)
    solucion = models.TextField(blank=True)

    costo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='INGRESADO'
    )

    def __str__(self):
        return f"Reparación #{self.id} - {self.equipo}"



    
class Opinion(models.Model):
    reparacion = models.OneToOneField(
        Reparacion,
        on_delete=models.CASCADE,
        related_name='opinion'
    )
    estrellas = models.PositiveSmallIntegerField(
        choices=[
            (1, '★'),
            (2, '★★'),
            (3, '★★★'),
            (4, '★★★★'),
            (5, '★★★★★'),
        ]
    )
    comentario = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Opinión de reparación #{self.reparacion.id} - {self.estrellas} estrellas"