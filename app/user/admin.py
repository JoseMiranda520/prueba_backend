from django.contrib import admin
from django.utils.html import format_html
from fw.admin import BaseModelAdmin
from import_export.admin import ImportExportModelAdmin
from pyctivex.admin import CustomAdmin

from .models import *
from .resources import UserResource

admin.site.unregister(User)



class ProfileInline(admin.TabularInline):
    model = Profile
    fk_name = 'user'
    exclude = BaseModelAdmin.exclude
    extra = 1


@admin.register(User)
class UserAdmin(CustomAdmin, ImportExportModelAdmin):
    # resource_class = UserResource
    inlines = [ProfileInline]

    def get_fieldsets(self, request, obj=None):
        fieldset = super(UserAdmin, self).get_fieldsets(request, obj)
        if not obj:
            fieldset += ((
                             None, {'fields': ('groups',)}
                         ),)

        return fieldset


@admin.register(Profile)
class ProfileAdmin(BaseModelAdmin, ImportExportModelAdmin):
    list_display = ('user', 'avatar')

@admin.register(Vehiculos)
class VehiculosAdmin(BaseModelAdmin):
    list_display = ['user']

@admin.register(Pilot)
class PilotAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'get_url', 'created_at', 'created_by')

    exclude = BaseModelAdmin.exclude + ('get_url',)

    def get_url(self, obj):
        return format_html('<a href="{}" target="_blank">{}</a>'.format(obj.indicators_link, obj.indicators_link))

    get_url.allow_tags = True
    get_url.short_description = 'Enlace'
