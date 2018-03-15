from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.core.models import Page

from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import StreamFieldPanel

from wagtail.core.blocks import StructBlock, CharBlock,  DateBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock


class EvidenceBlock(StructBlock):
    title = CharBlock(help_text='Evidence title')
    date = DateBlock()
    sound = DocumentChooserBlock(required=False, help_text='Select or upload evidence sound clip')
    image = ImageChooserBlock(required=False, help_text='Select or upload evidence image')
    embed = EmbedBlock(required=False)

    class Meta:
        template = 'evidence_block.html'


class EvidencePage(Page):
    body = StreamField([
        ('evidence', EvidenceBlock()),
    ],default='')

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]