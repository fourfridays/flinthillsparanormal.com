from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.core.models import Page

from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import StreamFieldPanel

from wagtail.core.blocks import StructBlock, CharBlock,TextBlock
from wagtail.images.blocks import ImageChooserBlock


class EquipmentBlock(StructBlock):
    image = ImageChooserBlock(help_text='Select or upload equipment image')
    title = CharBlock(help_text='Equipment title')
    description = TextBlock(help_text='Equipment description')

    class Meta:
        template = 'equipment_block.html'


class EquipmentPage(Page):
    body = StreamField([
        ('equipment', EquipmentBlock()),
    ],default='')

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]