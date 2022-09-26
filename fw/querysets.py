from django.conf import settings
from django.utils import timezone
from django.db.models.query import QuerySet


class BaseQuerySet(QuerySet):

    def delete(self):
        if settings.DEBUG:
            return super().delete()
        return self.update(deleted=True, deleted_at=timezone.now())
