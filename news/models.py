from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django import forms

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, StreamFieldPanel)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.search import index

from wagtail.core.blocks import TextBlock, StructBlock, StreamBlock, FieldBlock, CharBlock, RichTextBlock, RawHTMLBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock

from taggit.models import TaggedItemBase, Tag

from modelcluster.tags import ClusterTaggableManager
from modelcluster.fields import ParentalKey

from pages.blocks import NewsStreamBlock

import datetime


#News Index Page
class NewsIndexPage(Page):
    @property
    def news(self):
        # Get list of news pages that are descendants of this page
        news = NewsPage.objects.descendant_of(self).live()
        news = news.order_by(
            '-date'
        ).select_related('owner').prefetch_related(
            'tagged_items__tag',
            'categories',
            'categories__category',
        )
        return news

    def get_context(self, request, tag=None, category=None, author=None, *args,
                    **kwargs):
        context = super(NewsIndexPage, self).get_context(
            request, *args, **kwargs)
        news = self.news

        if tag is None:
            tag = request.GET.get('tag')
        if tag:
            news = news.filter(tags__slug=tag)
        if category is None:  # Not coming from category_view in views.py
            if request.GET.get('category'):
                category = get_object_or_404(
                    NewsCategory, slug=request.GET.get('category'))
        if category:
            if not request.GET.get('category'):
                category = get_object_or_404(NewsCategory, slug=category)
            news = news.filter(categories__category__name=category)
        if author:
            if isinstance(author, str) and not author.isdigit():
                news = news.filter(author__username=author)
            else:
                news = news.filter(author_id=author)

        # Pagination
        page = request.GET.get('page')
        page_size = None
        if hasattr(settings, 'NEWS_PAGINATION_PER_PAGE'):
            page_size = settings.NEWS_PAGINATION_PER_PAGE

        if page_size is not None:
            paginator = Paginator(news, page_size)  # Show 10 blogs per page
            try:
                news = paginator.page(page)
            except PageNotAnInteger:
                news = paginator.page(1)
            except EmptyPage:
                news = paginator.page(paginator.num_pages)

        context['news'] = news
        context['category'] = category
        context['tag'] = tag
        context['author'] = author
        context = get_news_context(context)

        return context

    class Meta:
        verbose_name = _('News index')
        #subpage_types = ['blog.BlogPage']


def get_news_context(context):
    """ Get context data useful on all blog related pages """
    context['authors'] = get_user_model().objects.filter(
        owned_pages__live=True,
        owned_pages__content_type__model='newspage'
    ).annotate(Count('owned_pages')).order_by('-owned_pages__count')
    context['all_categories'] = NewsCategory.objects.all()
    context['root_categories'] = NewsCategory.objects.filter(
        parent=None,
    ).prefetch_related(
        'children',
    ).annotate(
        news_count=Count('newspage'),
    )
    return context


@register_snippet
class NewsCategory(models.Model):
    name = models.CharField(
        max_length=80, unique=True, verbose_name=_('Category Name'))
    slug = models.SlugField(unique=True, max_length=80)
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name="children",
        help_text=_(
            'Categories, unlike tags, can have a hierarchy. You might have a '
            'Jazz category, and under that have children categories for Bebop'
            ' and Big Band. Totally optional.'),
        on_delete=models.CASCADE
    )
    description = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = _("News Category")
        verbose_name_plural = _("NewsCategories")

    panels = [
        FieldPanel('name'),
        FieldPanel('parent'),
        FieldPanel('description'),
    ]

    def __str__(self):
        return self.name

    def clean(self):
        if self.parent:
            parent = self.parent
            if self.parent == self:
                raise ValidationError('Parent category cannot be self.')
            if parent.parent and parent.parent == self:
                raise ValidationError('Cannot have circular Parents.')

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            count = NewsCategory.objects.filter(slug=slug).count()
            if count > 0:
                slug = '{}-{}'.format(slug, count)
            self.slug = slug
        return super(NewsCategory, self).save(*args, **kwargs)


class NewsCategoryNewsPage(models.Model):
    category = models.ForeignKey(
        NewsCategory, related_name="+", verbose_name=_('Category'), on_delete=models.CASCADE)
    page = ParentalKey('NewsPage', related_name='categories')
    panels = [
        FieldPanel('category'),
    ]


class NewsPageTag(TaggedItemBase):
    content_object = ParentalKey('NewsPage', related_name='tagged_items', on_delete=models.CASCADE)


@register_snippet
class NewsTag(Tag):
    class Meta:
        proxy = True


def limit_author_choices():
    """ Limit choices in blog author field based on config settings """
    LIMIT_AUTHOR_CHOICES = getattr(settings, 'NEWS_LIMIT_AUTHOR_CHOICES_GROUP', 'Editors')
    if LIMIT_AUTHOR_CHOICES:
        if isinstance(LIMIT_AUTHOR_CHOICES, str):
            limit = Q(groups__name=LIMIT_AUTHOR_CHOICES)
        else:
            limit = Q()
            for s in LIMIT_AUTHOR_CHOICES:
                limit = limit | Q(groups__name=s)
        if getattr(settings, 'NEWS_LIMIT_AUTHOR_CHOICES_ADMIN', False):
            limit = limit | Q(is_staff=True)
    else:
        limit = {'is_staff': True}
    return limit


#News Page
class NewsPage(Page):
    date = models.DateField(
        _("Post date"), default=datetime.datetime.today,
        help_text=_("This date may be displayed on the news post. It is not used to schedule posts to go live at a later date.")
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True, null=True,
        limit_choices_to=limit_author_choices,
        verbose_name=_('Author'),
        on_delete=models.SET_NULL,
        related_name='author_pages',
    )


    body = StreamField(NewsStreamBlock())

    news_categories = models.ManyToManyField(
        NewsCategory, through=NewsCategoryNewsPage, blank=True)
    
    tags = ClusterTaggableManager(through=NewsPageTag, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    def save_revision(self, *args, **kwargs):
        if not self.author:
            self.author = self.owner
        return super(NewsPage, self).save_revision(*args, **kwargs)

    def get_absolute_url(self):
        return self.url

    def get_context(self, request, *args, **kwargs):
        context = super(NewsPage, self).get_context(request, *args, **kwargs)
        context = get_news_context(context)
        return context

    class Meta:
        verbose_name = _('News Article')
        verbose_name_plural = _('News Articles')

NewsPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('date'),
    FieldPanel('author'),
    StreamFieldPanel('body'),
    MultiFieldPanel([
        FieldPanel('tags'),
        InlinePanel('categories', label=_("Categories")),
    ]),
]