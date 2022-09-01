from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel

from pages.blocks import EquipmentBlock


class EquipmentPage(Page):
    body = StreamField([
        ('equipment', EquipmentBlock()),
    ],use_json_field=True, default='')

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]