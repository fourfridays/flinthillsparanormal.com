from __future__ import absolute_import, unicode_literals

from django.db import models
from django import forms
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template.response import TemplateResponse

from wagtail.wagtailcore.models import Page

from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel

from wagtail.contrib.table_block.blocks import TableBlock

from wagtail.wagtailcore.blocks import TextBlock, StructBlock, StreamBlock, FieldBlock, CharBlock, RichTextBlock, RawHTMLBlock, BooleanBlock, ChoiceBlock, PageChooserBlock, ListBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock

from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField

from modelcluster.fields import ParentalKey


class AlignmentChoiceBlock(ChoiceBlock):
    choices = [
        ('normal', 'Normal'),
        ('text-left', 'Left'),
        ('text-center', 'Center'),
        ('text-right', 'Right'),
        ('text-justify', 'Justify'),
        ('text-nowrap', 'No Wrap')
    ]


class AlignedRAWHTMLBlock(StructBlock):
    html = RawHTMLBlock()
    alignment = AlignmentChoiceBlock(default='normal')

class AlignedH1Block(StructBlock):
    h1 = CharBlock(classname='title', help_text='Always use only one H1 per page')
    alignment = AlignmentChoiceBlock(default='normal')

class AlignedH2Block(StructBlock):
    h2 = CharBlock(classname='title')
    alignment = AlignmentChoiceBlock(default='normal')

class AlignedH3Block(StructBlock):
    h3 = CharBlock(classname='title')
    alignment = AlignmentChoiceBlock(default='normal')


class FontAwesomeIconSizeBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('lg', 'fa-lg'), 
        ('2x', 'fa-2x'),
        ('3x', 'fa-3x'),
        ('4x', 'fa-4x'),
        ('5x', 'fa-5x'),
    ))


class MaterialIconSizeBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('18', '18'), 
        ('24', '24'),
        ('36', '36'),
        ('48', '48'),
        ('60', '60'),
        ('72', '72'),
        ('84', '84'),
        ('96', '96'),
        ('108', '108'),
        ('120', '120'),
    ))


class PullQuoteBlock(StructBlock):
    quote = TextBlock('quote title')
    attribution = CharBlock()

    class Meta:
        icon = 'openquote'


class IconBlock(StructBlock):
    font_awesome_icon_name = CharBlock(required=False)
    font_awesome_icon_size = FontAwesomeIconSizeBlock()
    material_icon_name = CharBlock(required=False)
    material_icon_size = MaterialIconSizeBlock()
    alignment = AlignmentChoiceBlock(default='normal')

    class Meta:
        label = 'Icon'


class HtmlFormatBlock(StreamBlock):
    h1 = AlignedH1Block()
    h2 = AlignedH2Block()
    h3 = AlignedH3Block()
    h4 = CharBlock(classname='title')
    paragraph = RichTextBlock()
    table = TableBlock(template='includes/table.html')
    image = ImageChooserBlock()
    document = DocumentChooserBlock(icon='doc-full-inverse')
    embedded_video = EmbedBlock()
    lead_body = CharBlock(classname='lead')
    small_text = CharBlock(classname='small')
    blockquote = CharBlock(classname='blockquote')
    pull_quote = PullQuoteBlock()
    icon = IconBlock()
    raw_html = AlignedRAWHTMLBlock()


class SingleColumnBlock(StructBlock):
    column = HtmlFormatBlock()

    class Meta:
        template = 'single_column_block.html'
        label = 'Single Column'


class TwoColumnBlock(StructBlock):
    left_column = HtmlFormatBlock()
    right_column = HtmlFormatBlock()

    class Meta:
        template = 'two_column_block.html'
        label = 'Two Columns'


class ThreeColumnBlock(StructBlock):
    left_column = HtmlFormatBlock()
    center_column = HtmlFormatBlock()
    right_column = HtmlFormatBlock()

    class Meta:
        template = 'three_column_block.html'
        label = 'Three Columns'


class FourColumnBlock(StructBlock):
    left_column_1 = HtmlFormatBlock()
    left_column_2 = HtmlFormatBlock()
    right_column_1 = HtmlFormatBlock()
    right_column_2 = HtmlFormatBlock()

    class Meta:
        template = 'four_column_block.html'
        label = 'Four Columns'


class HeroImageBlock(StructBlock):
    image = ImageChooserBlock(required=True)
    alternate_text = CharBlock(help_text='Text for screen readers')
    caption = CharBlock(required=False, max_length=120, help_text='Caption will be shown below the image')
    fine_print = CharBlock(required=False, max_length=120, help_text='Fine Print will be shown below caption')
    overlay_text = BooleanBlock(required=False, help_text='If checked, caption is overlayed on image')
    photo_credit = CharBlock(required=False, max_length=80, help_text='This will show bottom right on the image')

    class Meta:
        template = 'hero_image_block.html'


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='form_fields')


class FormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Form fields", classname='form-group'),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]


class Pages(Page):
    body = StreamField([
        ('single_column', SingleColumnBlock(group='COLUMNS')),
        ('two_columns', TwoColumnBlock(group='COLUMNS')),
        ('three_columns', ThreeColumnBlock(group='COLUMNS')),
        ('four_columns', FourColumnBlock(group='COLUMNS')),
        ('hero_image', HeroImageBlock(icon='image')),
    ],default='')

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]