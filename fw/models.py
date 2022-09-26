# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from copy import deepcopy
from django.db import models
from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from django.utils import timezone
from fw.managers import BaseManager, AdminManager

User = get_user_model()
CAN_EXPORT = 'can_export'


class _Model(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Creado el')

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Creado por',
                                   null=True, blank=True, related_name='%(app_label)s_%(class)s_created_by')
    
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Actualizado por',
                                   null=True, blank=True, related_name='%(app_label)s_%(class)s_updated_by')

    deleted = models.BooleanField('Eliminado', default=False)

    deleted_at = models.DateTimeField('Eliminado el', null=True, blank=True)

    def save(self, *args, **kwargs):
        request = kwargs.pop('request', False)

        if request and self.created_by is None:
            self.created_by = request.user
            self.updated_by = request.user
        super(_Model, self).save()

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.deleted_at = timezone.now()
        self.save(*args, **kwargs)

    class Meta:
        abstract = True


class BaseModel(_Model):
    """
    ;log_class: LogModel define una clase para log la cual debe extender de LogModel
    """

    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado el')

    active = models.BooleanField('Activo', default=True, help_text='Indica si el modelo está operativo')

    objects = BaseManager()

    admin_objects = AdminManager()

    log_class = None

    EXCLUDES = ['created_by', 'created_at', 'updated_at', 'updated_by']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.log_class:
            self.__initial = deepcopy(self)

    def save(self, *args, **kwargs):
        super(BaseModel, self).save(*args, **kwargs)

        adding = self._state.adding

        # Preguntar si el modelo tiene o no clase para dejar logs de cambios.
        if not self.log_class or adding:
            return

        current = model_to_dict(self)
        initial = model_to_dict(self.__initial)

        for field in self._meta.fields:
            if field.name in self.EXCLUDES or field.name not in current:
                continue

            # Preguntar si el valor del campo cambio
            if current[field.name] != initial[field.name]:
                if isinstance(field, models.TextField):
                    before_text = None
                    after_text = None

                    if getattr(self.__initial, field.name):
                        before_text = str(getattr(self.__initial, field.name))
                    if getattr(self, field.name):
                        after_text = str(getattr(self, field.name))

                    # Agregar el registro con el cambio a la clase de logs.
                    log_class = self.log_class(field=field.name,
                                               before_text=before_text,
                                               after_text=after_text,
                                               record=self)
                else:
                    before_char = None
                    after_char = None

                    if hasattr(self.__initial, field.name):
                        try:
                            before_char = str(getattr(self.__initial, 'get_' + field.name + '_display')())
                        except AttributeError:
                            before_char = str(getattr(self.__initial, field.name))

                    if hasattr(self, field.name):
                        try:
                            after_char = str(getattr(self, 'get_' + field.name + '_display')())
                        except AttributeError:
                            after_char = str(getattr(self, field.name))

                    # Agregar el registro con el cambio a la clase de logs.
                    log_class = self.log_class(field=field.name,
                                               created_by=self.created_by,
                                               updated_by=self.updated_by,
                                               before_char=before_char,
                                               after_char=after_char,
                                               record=self)
                log_class.save()

        self.__initial = deepcopy(self)

    class Meta:
        abstract = True

        permissions = (
            (CAN_EXPORT, 'Puede exportar'),
        )


class LogModel(_Model):
    """
    Clase base para todos los modelos del aplicativo
    """
    field = models.CharField('Campo', max_length=150, null=True)
    before_char = models.CharField('Texto anterior', max_length=500, null=True, blank=True)
    after_char = models.CharField('Texto posterior', max_length=500, null=True, blank=True)
    before_text = models.TextField('Texto largo anterior', null=True, blank=True)
    after_text = models.TextField('Texto largo posterior', null=True, blank=True)
    before_id = models.IntegerField('Id anterior', null=True, blank=True)
    after_id = models.IntegerField('Id posterior', null=True, blank=True)

    objects = BaseManager()

    class Meta:
        abstract = True
