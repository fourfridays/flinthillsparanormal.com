# -*- coding: utf-8 -*-
from django.conf.urls import url, include, re_path
from django.urls import path
from django.contrib import admin
from wagtail.core import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from aldryn_django.utils import i18n_patterns
import aldryn_addons.urls


urlpatterns = [
    # add your own patterns here
    path('django-admin/', admin.site.urls),
] + aldryn_addons.urls.patterns() + i18n_patterns(
    # add your own i18n patterns here
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    re_path(r'', include(wagtail_urls)),
    *aldryn_addons.urls.i18n_patterns()  # MUST be the last entry!
)
