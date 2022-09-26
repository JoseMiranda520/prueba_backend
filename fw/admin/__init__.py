# ACTION_CHECKBOX_NAME is unused, but should stay since its import from here
# has been referenced in documentation.

from django.contrib.admin.sites import site
from django.utils.module_loading import autodiscover_modules
from fw.admin.options import BaseModelAdmin, BaseInlineMixin, BaseLogModelAdmin

__all__ = ['BaseModelAdmin', 'BaseInlineMixin', 'BaseLogModelAdmin']


def autodiscover():
    autodiscover_modules('admin', register_to=site)


default_app_config = 'django.contrib.admin.apps.AdminConfig'
