from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel

from pages.blocks import EvidenceBlock


class EvidencePage(Page):
    body = StreamField([
        ('evidence', EvidenceBlock()),
    ],default='')

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]