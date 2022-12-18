from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import RawHTMLBlock

from pages.blocks import TeamBlock


class TeamPage(Page):
    body = StreamField(
        [
            ("team", TeamBlock()),
            ("raw_html", RawHTMLBlock()),
        ],
        use_json_field=True,
        default="",
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
