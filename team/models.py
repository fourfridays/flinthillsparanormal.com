from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.core.models import Page

from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import StreamFieldPanel

from wagtail.core.blocks import StructBlock, CharBlock, TextBlock, RawHTMLBlock
from wagtail.images.blocks import ImageChooserBlock


class TeamBlock(StructBlock):
    image = ImageChooserBlock()
    title = CharBlock(help_text='Name and title')
    bio = TextBlock()

    class Meta:
        template = 'team_block.html'


class TeamPage(Page):
    body = StreamField([
        ('team', TeamBlock()),
        ('raw_html', RawHTMLBlock()),
    ],default='')

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]