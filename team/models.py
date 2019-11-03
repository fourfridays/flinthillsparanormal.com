from django.db import models

from wagtail.core.models import Page

from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.blocks import RawHTMLBlock

from pages.blocks import TeamBlock


class TeamPage(Page):
    body = StreamField([
        ('team', TeamBlock()),
        ('raw_html', RawHTMLBlock()),
    ],default='')

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]