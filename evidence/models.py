from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page

from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel

from wagtail.wagtailcore.blocks import StructBlock, CharBlock,  DateBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock


class EvidenceBlock(StructBlock):
    title = CharBlock(help_text='Evidence title')
    date = DateBlock()
    sound = DocumentChooserBlock(required=False, help_text='Select or upload evidence sound clip')
    image = ImageChooserBlock(required=False, help_text='Select or upload evidence image')
    document = DocumentChooserBlock(required=False, help_text='Select or upload evidence document')

    class Meta:
        template = 'evidence_block.html'


class EvidencePage(Page):
    body = StreamField([
        ('evidence', EvidenceBlock()),
    ],default='')

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]