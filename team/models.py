from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page

from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel

from wagtail.wagtailcore.blocks import StructBlock, CharBlock, TextBlock, RawHTMLBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock


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