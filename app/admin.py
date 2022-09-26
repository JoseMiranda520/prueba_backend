from django.contrib import admin
from pyctivex.admin import CustomAdmin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.contrib.auth import get_user_model
from .models import Profile, Pilot, Sale, Commissions, Indicator, Publish, Link, Script, Ecard, Target, Quiz_result, Alert, Media
from fw.admin import BaseModelAdmin
from django.utils.html import format_html
from django.utils.translation import gettext, gettext_lazy as _

@admin.register(Target)
class Target(BaseModelAdmin):
    list_display = ('cross', 'ups', 'pilot') 


@admin.register(Alert)
class Alert(BaseModelAdmin):
    list_display = ('name', 'content', 'status', 'date',) 



@admin.register(Quiz_result)
class Quiz_result(BaseModelAdmin):
    list_display = ('id', 'user', 'quiz', 'pilot', 'answers', 'result', 'schedule',) 


@admin.register(Ecard)
class Ecard(BaseModelAdmin):
    list_display = ('title', 'detail', 'link', 'card', 'pilot') 


@admin.register(Script)
class Script(BaseModelAdmin):
    list_display = ('title', 'text', 'pilot')  


@admin.register(Link)
class Link(BaseModelAdmin):
    list_display = ('title', 'link')


@admin.register(Publish)
class Publish(BaseModelAdmin):
    list_display = ('title', 'short_description', 'description', 'link', 'created_at', 'update_at', 'assign_byPilot')


@admin.register(Pilot)
class PilotAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'get_url', 'created_at', 'created_by')

    exclude = BaseModelAdmin.exclude + ('get_url',)

    def get_url(self, obj):
        return format_html('<a href="{}" target="_blank">{}</a>'.format(obj.indicators_link, obj.indicators_link))
    get_url.allow_tags = True
    get_url.short_description = 'Enlace'


@admin.register(Commissions)
class CommissionAdmin(BaseModelAdmin):
    list_display = ('name', 'value')


User = get_user_model()
class UserResource(resources.ModelResource):

    class Meta:
        model = User 
        fields = ('id', 'document', 'username', 'is_active', 'login_type')


admin.site.unregister(User)


class ProfileInline(admin.TabularInline):
    model = Profile
    fk_name = 'user'
    exclude  = BaseModelAdmin.exclude
    extra = 1

@admin.register(User)
class UserAdmin(CustomAdmin, ImportExportModelAdmin):
    resource_class = UserResource
    inlines = [ProfileInline]

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (('username', 'document', 'login_type'), 'password1', 'password2', 'groups'),
        }),
    )
    
    def get_fieldsets(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return (
                (None, {'fields': ('username', 'password')}),
                (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
                (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
                (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
            )
        return super(CustomAdmin, self).get_fieldsets(request, obj)



@admin.register(Profile)
class ProfileAdmin(BaseModelAdmin, ImportExportModelAdmin):
    list_display = ('user', 'avatar')
        

@admin.register(Sale)
class SaleAdmin(BaseModelAdmin):
    list_display = ('order', 'offer', 'user', 'status')

    search_fields = ('order', 'offer', 'user__first_name', 'user__email', 'user__last_name', 'user__username')
    
    date_hierarchy = 'entry'

    autocomplete_fields = ('user',)

    empty_value_display = '-'

    readonly_fields = BaseModelAdmin.readonly_fields + ('value',)

    list_select_related = ('user',)

    list_filter = ('status', 'cto', 'cba', 'ctv', 'uto', 'uba', 'utv')
    
    def get_form(self, request, obj=None, **kwargs):
        if not request.user.is_superuser:
            self.exclude += ('user',)
        return super(SaleAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        if obj.user and not change:
            obj.user = request.user
        obj.save()
    
    def get_queryset(self, request):
        qs = super(SaleAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

