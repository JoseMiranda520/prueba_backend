from django.contrib.auth import get_user_model
from fw.import_export.defs import get_verbose_name_headers
from import_export import resources

User = get_user_model()


class UserResource(resources.ModelResource):
    def get_export_headers(self):
        return get_verbose_name_headers(self.get_fields(), User)

    def dehydrate_is_active(self, model) -> str:
        """
        :param model: django.db.models.Model
        :return: str
        """
        return 'si' if model.is_active else 'no'

    dehydrate_is_active.DEFAULT_RESOURCE_FIELD = 'is_active'

    def dehydrate_is_staff(self, model) -> str:
        """
        :param model: django.db.models.Model
        :return: str
        """
        return 'si' if model.is_staff else 'no'

    dehydrate_is_staff.DEFAULT_RESOURCE_FIELD = 'is_staff'

    class Meta:
        model = User
        fields = ('document', 'username', 'is_active', 'login_type', 'is_staff', 'last_login', 'date_joined')
