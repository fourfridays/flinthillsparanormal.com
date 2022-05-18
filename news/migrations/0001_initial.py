# Generated by Django 2.2.6 on 2019-11-03 14:30

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import news.models
import wagtail.blocks
import wagtail.fields
import wagtail.documents.blocks
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True, verbose_name='Category Name')),
                ('slug', models.SlugField(max_length=80, unique=True)),
                ('description', models.CharField(blank=True, max_length=500)),
                ('parent', models.ForeignKey(blank=True, help_text='Categories, unlike tags, can have a hierarchy. You might have a Jazz category, and under that have children categories for Bebop and Big Band. Totally optional.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='news.NewsCategory')),
            ],
            options={
                'verbose_name': 'News Category',
                'verbose_name_plural': 'NewsCategories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='NewsCategoryNewsPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='news.NewsCategory', verbose_name='Category')),
            ],
        ),
        migrations.CreateModel(
            name='NewsIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name': 'News index',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='NewsPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('date', models.DateField(default=datetime.datetime.today, help_text='This date may be displayed on the news post. It is not used to schedule posts to go live at a later date.', verbose_name='Post date')),
                ('body', wagtail.fields.StreamField([('heading', wagtail.blocks.StructBlock([('heading_text', wagtail.blocks.CharBlock(classname='title', required=True)), ('size', wagtail.blocks.ChoiceBlock(blank=True, choices=[('', 'Select a header size'), ('h1', 'H1'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4'), ('h5', 'H5'), ('h6', 'H6')], required=False)), ('alignment', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right')], required=False))])), ('intro', wagtail.blocks.RichTextBlock(icon='pilcrow', template='blocks/paragraph_block')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow', template='blocks/paragraph_block')), ('image', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('caption', wagtail.blocks.CharBlock(required=False)), ('attribution', wagtail.blocks.CharBlock(required=False)), ('alignment', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right')], required=False)), ('border', wagtail.blocks.BooleanBlock(help_text='Adds border around image', required=False))], icon='image', label='Aligned image')), ('embed', wagtail.embeds.blocks.EmbedBlock(help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks', icon='code', template='blocks/embed_block.html')), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse')), ('raw_html', wagtail.blocks.StructBlock([('html', wagtail.blocks.RawHTMLBlock()), ('alignment', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right')]))], icon='code', label='Raw HTML'))])),
                ('author', models.ForeignKey(blank=True, limit_choices_to=news.models.limit_author_choices, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author_pages', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('news_categories', models.ManyToManyField(blank=True, through='news.NewsCategoryNewsPage', to='news.NewsCategory')),
            ],
            options={
                'verbose_name': 'News Article',
                'verbose_name_plural': 'News Articles',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='NewsTag',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('taggit.tag',),
        ),
        migrations.CreateModel(
            name='NewsPageTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='news.NewsPage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news_newspagetag_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='newspage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='news.NewsPageTag', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='newscategorynewspage',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='news.NewsPage'),
        ),
    ]
