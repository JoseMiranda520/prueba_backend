from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from fw.models import BaseModel

from app.defs import media_upload_to

User = get_user_model()
ESTADOS_CHOICES = ( 
    ("Disponible", "Disponible"), 
    ("Ocupado", "Ocupado"), 
    ("Fuera de servicio", "Fuera de servicio"), 
) 

class Pilot(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    indicators_link = models.URLField('Link', max_length=100, blank=True, null=True, unique=True)
    approved = models.PositiveSmallIntegerField('Porcentaje de aprobado', help_text='> 0', default=1,
                                                validators=[MinValueValidator(1)])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Piloto'
        ordering = ['name']


class Profile(BaseModel):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=media_upload_to, default="camara.jpg")
    pilot = models.ManyToManyField('Pilot')
    notepad = models.TextField('Bloc de Notas', blank=True, null=True, default='')

    class Meta:
        verbose_name = 'Perfile'
        ordering = ['-id']



class Vehiculos(BaseModel):
    id = models.AutoField(primary_key=True)
    cilindraje = models.CharField(max_length=10)
    capacidad = models.CharField(max_length=50)
    user = models.ForeignKey(User, related_name='propietario', on_delete=models.CASCADE)
    placa = models.CharField(max_length=320)
    fecha_soat = models.DateTimeField()
    fecha_tarjeta_operacion = models.DateTimeField()
    estado = models.CharField(max_length=50, choices = ESTADOS_CHOICES)

    class Meta:
        verbose_name = 'Vehiculo'
        ordering = ['-id']

class Viajes(BaseModel):
    id = models.AutoField(primary_key=True)
    punto_salida = models.CharField(max_length=50)
    punto_llegada = models.CharField(max_length=50)
    nombre_del_cliente = models.CharField(max_length=50)
    placa_vehiculo = models.CharField(max_length=5, null=True)
    estado = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Viaje'
        ordering = ['-id']