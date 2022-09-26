#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from datetime import datetime
from fw.models import BaseModel, LogModel
import os
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class Pilot(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    indicators_link = models.URLField('Link', max_length=100, blank=True, null=True, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Piloto'
        verbose_name_plural='pilotos'
        ordering = ['name']


class Media(models.Model):
    '''
    Modelo de archivos
    '''
    title = models.CharField(blank=True, null=True, max_length=150)
    #description = models.TextField(max_length=500, blank=True)
    file = models.FileField(
        'Archivo', 
        upload_to='app/media/%Y/%m/%d/', 
        max_length=150, 
        unique=True
    )

    class Meta:
        verbose_name='Media'
        verbose_name_plural='Medias'
        ordering = ['-id']
    
    def __unicode__(self):
        return self.title

    def __str__(self):
        return str("{0} - {1}".format(self.id, self.title))


class Link(BaseModel):
    title = models.CharField('Titulo', max_length=150, unique=True)
    link = models.URLField('Link', blank=True, null=True, unique=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name='Link'
        verbose_name_plural='Links'
        ordering = ['title']


class Tag(BaseModel):
    name = models.CharField('Etiqueta', max_length=150, unique=True, null=False, blank=False)

    def __str__(self):
        return self.name  
    
    class Meta:
        verbose_name='Etiqueta'
        verbose_name_plural='Etiquetas'
        ordering = ['name']


def validate_file_extension(value):
    ext = value.file.content_type
    valid_extensions = ['image/gif','image/png','image/jpeg']
    if not ext in valid_extensions:
        raise ValidationError('Formato no permitido.')

# esta función es llamada por Profile para darle nombre a la imágen
def update_filename(instance, filename):
    profile = Profile.objects.get(id=instance.id)
    validate_file_extension(instance.avatar)
    # saca el nombre y extensión de la imágen uploaded
    name, extension = os.path.splitext(filename)
    # Se cambiara el nombre del nombre de la imágen de ", name, " al nombre del usuario: ", instance.user
    new_name = str(instance.user) + str(datetime.timestamp(datetime.now())) + str(extension)
    path = "avatars"
    route = os.path.join(path, new_name)
    old_avatar = str(profile.avatar)
    
    """ En este bloque se hace la validación de si el archivo definido en 'route' ya existe.
    Si existe se procede a eliminarle; si no se eliminara se crearía uno con el nombre en route
    pero para no sobreescribirlo añade un código 'aleatorio' al final del nombre """
    deletePath = os.path.join(settings.MEDIA_ROOT, old_avatar)

    if os.path.exists(deletePath):
        os.remove(deletePath)
        # Se elimina el avatar anterior y se creará el nuevo.
        # Se creará un nuevo avatar para este usuario.
        # este return es el que define el nombre de la imágen.
        pass
    return route


class Profile(BaseModel):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    avatar = models.FileField(upload_to=update_filename, default="camara.jpg")
    pilot = models.ManyToManyField('Pilot')
    notepad = models.TextField('Bloc de Notas', blank=True, null=True, default='')

    def __str__(self):
        return "{}{}".format(self.user, "'s Profile")
    
    class Meta:
        verbose_name='Perfile'
        verbose_name_plural='Perfiles'
        ordering = ['-id']


class Publish(BaseModel):
    active = models.BooleanField(default=False)
    title = models.CharField('Titulo', max_length=150, unique=True, blank=False, null=False)
    short_description = models.CharField('Descripcion Corta', max_length=350, null=True, blank=True)
    description = models.TextField('Contenido', max_length=5000, blank=True)
    link = models.OneToOneField(Link, blank=False, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    assign_byPilot = models.ForeignKey(
        Pilot, 
        on_delete=models.CASCADE, 
        verbose_name='Piloto asignado', 
        related_name='%(app_label)s_%(class)s_created_by', 
        null=True
    )
    media = models.OneToOneField(Media, null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name='Publicacion'
        verbose_name_plural='Publicaciones'
        ordering = ['-id']

    def __str__(self):
        return self.title


class Alert(BaseModel):
    name = models.CharField(verbose_name='Nombre', null=False, max_length=50)
    content = models.CharField(verbose_name='Contenido', null=False, max_length=500)
    pilot = models.ManyToManyField('Pilot')
    status = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return self.name

    class Meta:
        verbose_name='Alerta'
        verbose_name_plural='Alertas'
        ordering = ['-date']


class Question(BaseModel):
    texto = models.CharField(verbose_name='Texto de la pregunta', null=False, max_length=1000)
    multiple = models.BooleanField(default=False)
    option_list = models.CharField(verbose_name='Dos o más respuestas opcionales en formato json', null=False, max_length=300)
    correct_option = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.texto

    class Meta:
        verbose_name='Pregunta'
        verbose_name_plural='Preguntas'
        ordering = ['-id']


class Quiz(BaseModel):
    name = models.CharField(verbose_name='Nombre del Quiz', null=False, max_length=300)
    description = models.CharField(verbose_name='Descripción general', null=False, max_length=300)
    questions = models.ManyToManyField(Question, blank=True)
    finish_date = models.DateTimeField()
    assign_byPilot = models.ManyToManyField('Pilot')

    def __str__(self):
        return str("{0} - {1}".format('Quiz', self.id))

    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

    class Meta:
        verbose_name='Quiz'
        verbose_name_plural='Quizs'
        ordering = ['-id']


class Quiz_result(BaseModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='User', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='Quiz', on_delete=models.CASCADE)
    pilot = models.ForeignKey(Pilot, on_delete=models.CASCADE)
    answers = models.CharField(verbose_name='Respuestas enviadas por el usuario', blank=True, null=True, max_length=300)
    result = models.PositiveIntegerField(verbose_name='Nota entre 0 y 100, calculada con base a las respuestas enviadas', blank=True, null=True)
    schedule = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.id.__str__()

    class Meta:
        ordering = ['-id']


class SaleLog(LogModel):
    """Log modelo de ventas"""
    record = models.ForeignKey('Sale', verbose_name='Ventas', on_delete=models.PROTECT)


class Sale(BaseModel):

    ESTADO = (
        ('CR', 'Creado'),
        ('PE', 'Pendiente'),
        ('AG', 'Agendado'),
        ('RE', 'Reagendado'),
        ('CU', 'Cumplido-ANS'),
        ('CE', 'Cerrado'),
        ('EX', 'Excepcion/Escalado'),
        ('AN', 'Anulado')
    )
    user = models.ForeignKey(User, default=None, related_name='sales', on_delete=models.CASCADE)
    offer = models.CharField(max_length=300)
    order = models.CharField(max_length=300, null=True, blank=True)
    entry = models.DateField(blank=True, null=True)
    schedule = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=2, choices=ESTADO)
    cto =  models.BooleanField(default=False)
    cba =  models.BooleanField(default=False)
    ctv =  models.BooleanField(default=False)
    uto =  models.BooleanField(default=False)
    uba =  models.BooleanField(default=False)
    utv =  models.BooleanField(default=False)
    value = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    
    log_class = SaleLog

    def __str_(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.status == 'CE' and self.value == 0:
            date = datetime.now()
            commissions = Commissions.objects.filter(date_end__gte=date, date_star__lte=date,  active=True)
            total = 0
            for commision in commissions:
                if self.cto and commision.name == 'cto':
                    total += commision.value
                elif self.cba and commision.name == 'cba':
                    total += commision.value
                elif self.ctv and commision.name == 'ctv':
                    total += commision.value
                elif self.uba and commision.name == 'uba':
                    total += commision.value
                elif self.uto and commision.name == 'uto':
                    total += commision.value
                elif self.utv and commision.name == 'utv':
                    total += commision.value
            self.value = total
        
        super(Sale, self).save(*args, **kwargs)
    
    
    class Meta:
        verbose_name='Venta'
        verbose_name_plural='Ventas'
        ordering = ['-id']

class Target(BaseModel):
    cross = models.IntegerField(default=0) 
    ups = models.IntegerField(default=0)
    pilot = models.OneToOneField(Pilot, related_name='Piloto_target', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name='Meta'
        verbose_name_plural='Metas'
        ordering = ['-id']


class Script(BaseModel):
    title = models.CharField(verbose_name='Nombre del guión', null=False, max_length=300)
    text = models.CharField(verbose_name='Contenido del guión', null=False, max_length=1000)
    pilot = models.ForeignKey(
        Pilot, 
        related_name='Piloto_script', 
        verbose_name='Piloto al que aplica éste guión', 
        null=True, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name='Guión'
        verbose_name_plural='Guiones'
        ordering = ['-id']

    def __str__(self):
        return self.title


class Ecard(BaseModel):
    title = models.CharField(blank=False, null=False, max_length=150)
    detail = models.CharField(blank=True, null=True, max_length=500)
    link = models.URLField('Link', blank=True, null=True, unique=True)
    card = models.ImageField(
        'Archivo', 
        upload_to='app/media/%Y/%m/%d/', 
        max_length=150, 
        unique=True
    )
    pilot = models.ForeignKey(
        Pilot, 
        related_name='Piloto_ecard', 
        verbose_name='Piloto al que aplica ésta e-card', 
        null=True, 
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name='Ecard'
        verbose_name_plural='Ecards'
        ordering = ['-id']


class Commissions(BaseModel):

    TYPE = (
        ('cto', 'Cto'),
        ('cba', 'Cba'),
        ('ctv', 'Ctv'),
        ('uto', 'Uto'),
        ('uba', 'Uba'),
        ('utv', 'Utv'),
    )

    name = models.CharField(max_length=3, choices=TYPE)
    value = models.DecimalField(max_digits=16, decimal_places=2)
    description = models.CharField(max_length=300)
    date_star = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=False)
    producto = models.CharField(max_length=3, choices=TYPE)
    
    
    class Meta:
        verbose_name='comisión'
        verbose_name_plural='comisiones'
        ordering = ['-id']

    def __str_(self):
        return str(self.id)



# Depurar campos
class Indicator(BaseModel):
    identification = models.CharField(max_length=80)
    login = models.CharField(max_length=80)
    name = models.CharField(max_length=80)
    supervisor = models.CharField(max_length=80)
    status = models.CharField(max_length=80)
    type_advisor = models.CharField(max_length=80)
    team = models.CharField(max_length=80)
    calls_answered = models.CharField(max_length=80)
    goal_aht = models.CharField(max_length=80)
    aht = models.CharField(max_length=80)
    diference_aht = models.CharField(max_length=80)
    typing = models.CharField(max_length=80)
    adh = models.CharField(max_length=80)
    penc = models.CharField(max_length=80)  
    pecu = models.CharField(max_length=80)
    pecn = models.CharField(max_length=80)
    pecc = models.CharField(max_length=80)
    general_frc = models.CharField(max_length=80)
    sat = models.CharField(max_length=80)
    nps = models.CharField(max_length=80)
    fcr = models.CharField(max_length=80)
    knowledge_assessment = models.CharField(max_length=80)
    absences = models.CharField(max_length=80)
    rgu = models.CharField(max_length=80)
    final_weighted = models.CharField(max_length=80)
    performance = models.CharField(max_length=80)

    class Meta:
        ordering = ['login']


class Indicators_tip(BaseModel):
    aht = models.CharField(max_length=400, null=True)
    adh = models.CharField(max_length=400, null=True)
    penc = models.CharField(max_length=400, null=True)  
    pecu = models.CharField(max_length=400, null=True)
    pecn = models.CharField(max_length=400, null=True)
    pecc = models.CharField(max_length=400, null=True)
    sat = models.CharField(max_length=400, null=True)
    nps = models.CharField(max_length=400, null=True)
    fcr = models.CharField(max_length=400, null=True)
    rgu = models.CharField(max_length=400, null=True)

    def save(self, *args, **kwargs):
        if Indicators_tip.objects.exists() and not self.pk:
        # we check a new instance is not being created 
        # otherwhise we raise ValidationError
            raise ValidationError('Sólo debe haber una instancia para los tips')
        return super(Indicators_tip, self).save(*args, **kwargs)


