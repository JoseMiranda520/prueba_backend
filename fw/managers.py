from django.db import models
from fw.querysets import BaseQuerySet


class BaseManager(models.Manager):
    def get_queryset(self):

        return BaseQuerySet(self.model, using=self._db).filter(deleted=False)


class AdminManager(models.Manager):
    def get_queryset(self):
        return BaseQuerySet(self.model, using=self._db)
