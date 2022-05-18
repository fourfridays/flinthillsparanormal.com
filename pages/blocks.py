from django import forms

from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.blocks import (
    BooleanBlock, CharBlock, ChoiceBlock, DateBlock, FieldBlock, PageChooserBlock, RawHTMLBlock, RichTextBlock, StreamBlock, StructBlock, TextBlock, URLBlock
)
from wagtail.contrib.table_block.blocks import TableBlock


class AlignmentBlock(ChoiceBlock):
    choices = [
        ('left', 'Left'),
        ('center', 'Center'),
        ('right', 'Right')
    ]


class AlignedRAWHTMLBlock(StructBlock):
    html = RawHTMLBlock()
    alignment = AlignmentBlock(default='left')

    class Meta:
        template = 'blocks/aligned_raw_html_block.html'


class ButtonBlock(StructBlock):
    alignment = AlignmentBlock(default='left')
    size = ChoiceBlock([
        ('sm', 'Small'),
        ('md', 'Medium'),
        ('lg', 'Large')
    ])
    cta_text = CharBlock(max_length=25, help_text='25 character limit.')
    internal_link = PageChooserBlock(required=False)
    external_link = URLBlock(required=False)
    color = ChoiceBlock([
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('dark-brown', 'Dark Brown'),
        ('white-smoke', 'White Smoke'),
        ('concrete', 'Concrete'),
        ('aqua-island', 'Aqua Island'),

    ])

    class Meta:
        icon = 'pick'
        template = 'blocks/button_block.html'


class EmbedBlock(StructBlock):
    you_tube_embed = CharBlock(required=False, help_text='Insert the embed code e.g Pha7WiAuhw4 the part that follows https://youtu.be/')

    class Meta:
        template='blocks/embed_block.html'


class EquipmentBlock(StructBlock):
    image = ImageChooserBlock(help_text='Select or upload equipment image')
    title = CharBlock(help_text='Equipment title')
    description = TextBlock(help_text='Equipment description')

    class Meta:
        template = 'blocks/equipment_block.html'


class EvidenceBlock(StructBlock):
    title = CharBlock(help_text='Evidence title')
    date = DateBlock()
    sound = DocumentChooserBlock(required=False, help_text='Select or upload evidence sound clip')
    image = ImageChooserBlock(required=False, help_text='Select or upload evidence image')
    embed = EmbedBlock(required=False)

    class Meta:
        template = 'blocks/evidence_block.html'


class IconBlock(StructBlock):
    icon = ChoiceBlock([
        ('font-awesome', 'Font Awesome'),
        ('material-icon', 'Material Icon')
    ])
    name = CharBlock(max_length=25, help_text='25 character limit')
    size = ChoiceBlock(choices = [
        ('sm', 'Small'),
        ('md', 'Medium'),
        ('lg', 'Large'),
        ('xl', 'Extra Large')
    ])
    font_awesome_icon_choice = ChoiceBlock([
        ('solid', 'Solid'),
        ('regular', 'Regular'),
        ('light', 'Light'),
        ('brand', 'Brand')
    ], required=False)
    alignment = AlignmentBlock(default='left')

    class Meta:
        icon = 'wagtail'
        template = 'blocks/icon_block.html'


class ImageBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """
    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)
    attribution = CharBlock(required=False)
    alignment = AlignmentBlock(default='left', required=False)
    border = BooleanBlock(required=False, help_text='Adds border around image')

    class Meta:
        icon = 'image'
        template = 'blocks/image_block.html'


class ImageGridBlock(StreamBlock):
    grid = StructBlock([
        ('image', ImageChooserBlock(required=True, help_text='size: 800X450px')),
        ('caption', CharBlock(max_length=26, help_text='26 characters limit')),
        ('description', CharBlock(max_length=300, required=False, help_text='300 characters limit')),
        ('link', PageChooserBlock(required=False))
    ])

    class Meta:
        icon = 'image'
        template = 'blocks/image_grid_block.html'


class HeadingBlock(StructBlock):
    """
    Custom `StructBlock` that allows the user to select h2 - h6 sizes for headers
    """
    heading_text = CharBlock(classname="title", required=True)
    size = ChoiceBlock(choices=[
        ('', 'Select a header size'),
        ('h1', 'H1'),
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4'),
        ('h5', 'H5'),
        ('h6', 'H6')
    ], blank=True, required=False)
    alignment = AlignmentBlock(default='left', required=False)

    class Meta:
        icon = 'pilcrow'
        template = 'blocks/heading_block.html'


class TeamBlock(StructBlock):
    image = ImageChooserBlock()
    title = CharBlock(help_text='Name and title')
    bio = TextBlock()

    class Meta:
        template = 'blocks/team_block.html'


# StreamBlocks
class BaseStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """
    heading_block = HeadingBlock()
    paragraph_block = RichTextBlock(
        icon='pilcrow',
        template='blocks/paragraph_block.html'
    )
    image_block = ImageBlock()
    button_block = ButtonBlock()
    image_grid_block = ImageGridBlock()
    embed_block = EmbedBlock(icon='code')
    icon_block = IconBlock()
    table = TableBlock(template='includes/table.html')
    raw_html = AlignedRAWHTMLBlock()


class NewsStreamBlock(StreamBlock):
    heading = HeadingBlock()
    intro = RichTextBlock(icon='pilcrow', template='blocks/paragraph_block')
    paragraph = RichTextBlock(icon='pilcrow', template='blocks/paragraph_block')
    image = ImageBlock(label="Aligned image", icon="image")
    embed = EmbedBlock(icon='code')
    document = DocumentChooserBlock(icon="doc-full-inverse")
    raw_html = AlignedRAWHTMLBlock(icon="code", label='Raw HTML')


class SingleColumnBlock(StructBlock):
    column = BaseStreamBlock()
    alignment = AlignmentBlock(default='left')

    class Meta:
        label = 'Single Column'
        template = 'blocks/single_column_block.html'


class TwoColumnBlock(StructBlock):
    left_column = BaseStreamBlock()
    right_column = BaseStreamBlock()
    alignment = AlignmentBlock(default='left')

    class Meta:
        label = 'Two Columns'
        template = 'blocks/two_column_block.html'


class ThreeColumnBlock(StructBlock):
    left_column = BaseStreamBlock()
    middle_column = BaseStreamBlock()
    right_column = BaseStreamBlock()
    alignment = AlignmentBlock(default='left')

    class Meta:
        label = 'Three Columns'
        template = 'blocks/three_column_block.html'


class FourColumnBlock(StructBlock):
    left_column_1 = BaseStreamBlock()
    left_column_2 = BaseStreamBlock()
    right_column_1 = BaseStreamBlock()
    right_column_2 = BaseStreamBlock()
    alignment = AlignmentBlock(default='left')

    class Meta:
        label = 'Four Columns'
        template = 'blocks/four_column_block.html'