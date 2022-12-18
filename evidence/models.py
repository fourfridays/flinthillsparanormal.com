from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel

from pages.blocks import EvidenceBlock


class EvidencePage(Page):
    body = StreamField(
        [
            ("evidence", EvidenceBlock()),
        ],
        use_json_field=True,
        default="",
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
