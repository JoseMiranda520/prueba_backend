# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.utils import timezone


def delete_selected(instance, request, queryset):
    """
    :param instance: django.contrib.admin.ModelAdmin
    :param request: urllib.request.Request
    :param queryset: django.db.models.query.Queryset
    :return:
    """
    logging.info("delete_selected {}, {}".format(instance.__str__(), request.user.__str__()))
    queryset.update(deleted=True, deleted_at=timezone.now())


delete_selected.__name__ = 'Eliminar seleccionados'
delete_selected.short_description = 'Eliminar seleccionados'


def activate_selected(instance, request, queryset):
    """
    :param instance: django.contrib.admin.ModelAdmin
    :param request: urllib.request.Request
    :param queryset: django.db.models.query.Queryset
    :return:
    """
    logging.info("activate_selected {}, {}".format(instance.__str__(), request.user.__str__()))
    queryset.update(active=True)


activate_selected.__name__ = 'Activar seleccionados'
activate_selected.short_description = 'Activar seleccionados'


def inactivate_selected(instance, request, queryset):
    """
    :param instance: django.contrib.admin.ModelAdmin
    :param request: urllib.request.Request
    :param queryset: django.db.models.query.Queryset
    :return:
    """
    logging.info("inactivate_selected {}, {}".format(instance.__str__(), request.user.__str__()))
    queryset.update(active=False)


inactivate_selected.__name__ = 'Inactivar seleccionados'
inactivate_selected.short_description = 'Inactivar seleccionados'
