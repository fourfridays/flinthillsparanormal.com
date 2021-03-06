# Generated by Django 3.0.13 on 2021-03-14 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_auto_20191230_2150'),
    ]

    operations = [
        migrations.AddField(
            model_name='formfield',
            name='clean_name',
            field=models.CharField(blank=True, default='', help_text='Safe name of the form field, the label converted to ascii_snake_case', max_length=255, verbose_name='name'),
        ),
    ]
