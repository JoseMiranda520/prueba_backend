
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from rest_framework.documentation import include_docs_urls


from app.user.views import UserViewSet, GroupViewSet, PilotViewSet, ProfileViewSet, Login, GroupNameViewSet




admin.site.site_title = 'usuarios'
admin.site.site_header = 'gestión de usuarios'

router = DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'users/sac_off', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'groups_name', GroupNameViewSet, basename='groups_name')
router.register(r'pilots', PilotViewSet)
router.register(r'profile', ProfileViewSet)




urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/login/', view=Login.as_view(), name='login'),
    path('api-token-refresh/', refresh_jwt_token),
    path('api/check-token/', verify_jwt_token),
    path('docs/', include_docs_urls(title=admin.site.site_header, description=admin.site.site_title)),
    path('admin/', admin.site.urls),
]
