from __future__ import unicode_literals
from email.policy import default

from django.contrib import messages
from django.db import models
from django.shortcuts import redirect, render

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey

from taggit.models import Tag, TaggedItemBase

from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import StreamField
from wagtail.models import Page, Orderable
from wagtail.search import index

from lgucms.base.models import StandardPage


class NewsPersonnelRelationship(Orderable, models.Model):
    page = ParentalKey(
        'NewsPage', related_name='news_person_relationship', on_delete=models.CASCADE
    )
    personnel = models.ForeignKey(
        'personnel.Personnel', related_name='person_news_relationship', on_delete=models.CASCADE
    )
    panels = [
        FieldPanel('personnel')
    ]


class NewsPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'NewsPage', related_name='tagged_items', on_delete=models.CASCADE)


class NewsPage(StandardPage):
    subtitle = models.CharField(blank=True, max_length=255)
    tags = ClusterTaggableManager(through=NewsPageTag, blank=True)
    date_published = models.DateTimeField(
        "Date article published", blank=True, null=True
    )

    content_panels = StandardPage.content_panels + [
        FieldPanel('subtitle', classname="full"),
        FieldPanel('date_published'),
        InlinePanel(
            'news_person_relationship', label="Author(s)",
            panels=None, min_num=1),
        FieldPanel('tags'),
    ]

    search_fields = StandardPage.search_fields + [
        index.SearchField('body'),
    ]

    def authors(self):
        authors = [self.owner, ]
        authors += [
            n.personnel for n in self.news_person_relationship.all()
        ]

        return authors

    @property
    def get_tags(self):
        tags = self.tags.all()
        for tag in tags:
            tag.url = '/' + '/'.join(s.strip('/') for s in [
                self.get_parent().url,
                'tags',
                tag.slug
            ])
        return tags

    parent_page_types = ['NewsIndexPage']

    subpage_types = []


class NewsIndexPage(RoutablePageMixin, StandardPage):
    content_panels = StandardPage.content_panels

    subpages_types = ['NewsPage']

    def children(self):
        return self.get_children().specific().live()

    def get_latest(self):
        return NewsPage.objects.descendant_of(
            self).live().order_by(
            '-date_published')

    def get_context(self, request):
        context = super(NewsIndexPage, self).get_context(request)
        context['posts'] = NewsPage.objects.descendant_of(
            self).live().order_by(
            '-date_published')
        return context

    @route(r'^tags/$', name='tag_archive')
    @route(r'^tags/([\w-]+)/$', name='tag_archive')
    def tag_archive(self, request, tag=None):

        try:
            tag = Tag.objects.get(slug=tag)
        except Tag.DoesNotExist:
            if tag:
                msg = 'There are no news articles tagged with "{}"'.format(tag)
                messages.add_message(request, messages.INFO, msg)
            return redirect(self.url)

        posts = self.get_posts(tag=tag)
        context = {
            'tag': tag,
            'posts': posts
        }
        return render(request, 'news/news_index_page.html', context)

    def serve_preview(self, request, mode_name):
        # Needed for previews to work
        return self.serve(request)

    # Returns the child NewsPage objects for this NewsPageIndex.
    # If a tag is used then it will filter the posts by tag.
    def get_posts(self, tag=None):
        posts = NewsPage.objects.live().descendant_of(self)
        if tag:
            posts = posts.filter(tags=tag)
        return posts

    # Returns the list of Tags for all child posts of this NewsPage.
    def get_child_tags(self):
        tags = []
        for post in self.get_posts():
            # Not tags.append() because we don't want a list of lists
            tags += post.get_tags
        tags = sorted(set(tags))
        return tags
