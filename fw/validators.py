# -*- coding: utf-8 -*-
import logging
from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError


AlphaNumericValidator = RegexValidator(r'^[a-zA-Z0-9]*$',
                                       message='Este campo debe ser alfanumérico.',
                                       code='Inválido')

AlphaNumericValidatorWithSpaces = RegexValidator(r'^[A-Za-zÑñáéíóúÁÉÍÓÚ0-9 \-\–]+$',
                                                 message='Este campo solo permite números, letras, guiones y espacios.',
                                                 code='Inválido')

NumericValidatorWithSpaces = RegexValidator(r'^[0-9]*$',
                                            message='Este campo debe ser numérico.',
                                            code='Inválido')

AlphaValidatorWithSpaces = RegexValidator(r'^[a-zA-Z- ñÑ-áéíóúÁÉÍÓÚ]+$',
                                          message='Este campo sólo permite letras.',
                                          code='Inválido')


@deconstructible
class FileSizeValidator:
    code = 'invalid'

    def __init__(self, max_size=None):
        if max_size:
            self.max_size = max_size
        else:
            raise AttributeError('Debe ingresar el máximo peso del archivo')

    def __call__(self, value):
        logging.info('Calling {}'.format(value))

        size = value.file.size

        if size > self.max_size*1024*1024:
            raise ValidationError("Tamaño máximo permitido es %sMB" % str(self.max_size))

    def __eq__(self, other):
        return (
                isinstance(other, FileSizeValidator) and
                (self.max_size == other.max_size) and
                (self.accept == other.accept)
        )
