from django.utils.timezone import localtime
from import_export.widgets import DateTimeWidget
from django.conf import settings


class TzDateTimeWidget(DateTimeWidget):

    def render(self, value, obj=None):
        if settings.USE_TZ:
            value = localtime(value)
        return super(TzDateTimeWidget, self).render(value, obj)
