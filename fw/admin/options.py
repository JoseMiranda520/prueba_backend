from django.contrib import admin
from django.utils import timezone


class BaseModelAdmin(admin.ModelAdmin):

    list_filter = ('active',)

    date_hierarchy = 'created_at'

    readonly_fields = ('created_by', 'created_at', 'updated_at')

    exclude = ()

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super(BaseModelAdmin, self).save_model(request, obj, form, change)

    def get_list_display(self, request):
        list_display = super(BaseModelAdmin, self).get_list_display(request)

        if request.user.is_superuser:
            list_display += self.readonly_fields

        return list_display

    def get_exclude(self, request, obj=None):
        exclude = super(BaseModelAdmin, self).get_exclude(request)

        if not request.user.is_superuser:
            exclude += ('created_by', 'deleted', 'deleted_at')

        return exclude

    def get_list_filter(self, request):
        list_filter = super(BaseModelAdmin, self).get_list_filter(request)

        if request.user.is_superuser:
            list_filter += ('deleted',)

        return list_filter

    def get_queryset(self, request):
        if request.user.is_superuser:
            qs = self.model.admin_objects
        else:
            qs = self.model.objects

        ordering = self.get_ordering(request)

        if ordering:
            qs = qs.order_by(*ordering)

        return qs

    def get_search_results(self, request, queryset, search_term):
        """
        :param request: http.HttpRequest
        :param queryset: BaseQueryset
        :param search_term: str
        :return: Tuple[Any, bool]
        """
        if 'autocomplete' in request.path_info:
            queryset = queryset.filter(active=True)
        return super(BaseModelAdmin, self).get_search_results(request, queryset, search_term)


class BaseLogModelAdmin(admin.ModelAdmin):
    list_display = ('record', 'field', 'before_char', 'after_char', 'before_id', 'after_id', 'created_at')

    search_fields = ('before_char', 'after_char', 'field')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class BaseInlineMixin(object):
    exclude = BaseModelAdmin.exclude

    extra = 0
