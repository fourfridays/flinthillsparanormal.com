# Generated by Django 4.0.4 on 2022-05-18 22:25

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teampage',
            name='body',
            field=wagtail.fields.StreamField([('team', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('title', wagtail.blocks.CharBlock(help_text='Name and title')), ('bio', wagtail.blocks.TextBlock())])), ('raw_html', wagtail.blocks.RawHTMLBlock())], default='', use_json_field=True),
        ),
    ]
