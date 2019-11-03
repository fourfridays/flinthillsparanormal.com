from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel

from pages.blocks import EquipmentBlock


class EquipmentPage(Page):
    body = StreamField([
        ('equipment', EquipmentBlock()),
    ],default='')

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]