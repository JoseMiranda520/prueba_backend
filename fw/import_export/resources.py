from django.contrib.auth import get_user_model
from import_export import resources, fields, widgets
from .widgets import TzDateTimeWidget
from .defs import get_verbose_name_headers

User = get_user_model()


class BaseResource(resources.ModelResource):
    def __init__(self, model=None, display_fields=None, exclude=None, append_exclude=()):
        super().__init__()

        if model:
            self.Meta.model = model

        if display_fields:
            self.Meta.fields = display_fields

        if hasattr(self.Meta, 'exclude'):
            if exclude:
                self.Meta.exclude = exclude

            self.Meta.exclude += append_exclude

    created_by = fields.Field(
        attribute="created_by",
        column_name="Creado por",
        readonly=True,
        widget=widgets.ForeignKeyWidget(User, "username")
    )

    created_at = fields.Field(column_name="Creado el", readonly=True,
                              widget=TzDateTimeWidget(), attribute='created_at')

    updated_at = fields.Field(column_name="Actualizado el", readonly=True,
                              widget=TzDateTimeWidget(), attribute='updated_at')

    def dehydrate_active(self, model) -> str:
        """
        :param model: django.db.models.Model
        :return: str
        """
        return 'si' if model.active else 'no'
    dehydrate_active.DEFAULT_RESOURCE_FIELD = 'active'

    def dehydrate_deleted(self, model) -> str:
        """
        :param model: django.db.models.Model
        :return: str
        """
        return 'si' if model.deleted else 'no'
    dehydrate_deleted.DEFAULT_RESOURCE_FIELD = 'deleted'

    def get_export_headers(self):
        return get_verbose_name_headers(self.get_fields(), self.Meta.model)

    class Meta:
        exclude = ('deleted', 'deleted_at')

        model = None
