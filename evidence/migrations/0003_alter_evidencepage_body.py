# Generated by Django 4.1 on 2022-09-01 01:02

from django.db import migrations
import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('evidence', '0002_auto_20191128_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evidencepage',
            name='body',
            field=wagtail.fields.StreamField([('evidence', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='Evidence title')), ('date', wagtail.blocks.DateBlock()), ('sound', wagtail.documents.blocks.DocumentChooserBlock(help_text='Select or upload evidence sound clip', required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='Select or upload evidence image', required=False)), ('embed', wagtail.blocks.StructBlock([('you_tube_embed', wagtail.blocks.CharBlock(help_text='Insert the embed code e.g Pha7WiAuhw4 the part that follows https://youtu.be/', required=False))], required=False))]))], default='', use_json_field=True),
        ),
    ]