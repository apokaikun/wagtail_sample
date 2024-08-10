from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from django.contrib import messages
from django.db import models
from django.shortcuts import redirect, render

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey

from taggit.models import Tag, TaggedItemBase

from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Page, Orderable
from wagtail.search import index

from .blocks import PageStream
from lgucms.base.models import StandardPage


class BulletinBoard(Page):
    """
    An index page to manually select different pages to feature.
    A subclass of the standard page to inheret the basic properties of a standard page 
    plus the addition to add multiple pages as features.
    """
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.',
        verbose_name='hero image'
    )

    feature_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='This image will be used when this page is shared or embedded in another page.',
        verbose_name='feature image'
    )

    body = StreamField(
        PageStream(),
        use_json_field=True,
        verbose_name='Bulletin Board Body'
    )

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('image'),
        FieldPanel('feature_image'),
    ]


class ProjectUpdatePersonnelRelationship(Orderable, models.Model):
    page = ParentalKey(
        'ProjectUpdatePage', related_name='projectupdate_person_relationship', on_delete=models.CASCADE
    )
    personnel = models.ForeignKey(
        'personnel.Personnel', related_name='person_projectupdate_relationship', on_delete=models.CASCADE
    )
    panels = [
        FieldPanel('personnel')
    ]


class ProjectUpdatePageTag(TaggedItemBase):
    content_object = ParentalKey(
        'ProjectUpdatePage', related_name='tagged_items', on_delete=models.CASCADE)


class ProjectUpdatePage(StandardPage):
    subtitle = models.CharField(blank=True, max_length=255)
    tags = ClusterTaggableManager(through=ProjectUpdatePageTag, blank=True)
    date_published = models.DateTimeField(
        "Date article published", blank=True, null=True
    )

    content_panels = StandardPage.content_panels + [
        FieldPanel('subtitle', classname="full"),
        FieldPanel('date_published'),
        InlinePanel(
            'projectupdate_person_relationship', label="Author(s)",
            panels=None),
        FieldPanel('tags'),
    ]

    search_fields = StandardPage.search_fields + [
        index.SearchField('body'),
    ]

    def authors(self):
        authors = [
            n.personnel for n in self.projectupdate_person_relationship.all()
        ]

        return authors

    def editor(self):
        return (" ").join([self.owner.first_name, self.owner.last_name])

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

    parent_page_types = ['ProjectUpdateIndexPage', ]

    subpage_types = []


class ProjectUpdateIndexPage(RoutablePageMixin, StandardPage):
    content_panels = StandardPage.content_panels

    subpages_types = ['bulletin.ProjectUpdatePage', ]

    def children(self):
        return self.get_children().specific().live()

    def get_latest(self):
        return ProjectUpdatePage.objects.descendant_of(
            self).live().order_by(
            '-date_published')

    def get_context(self, request):
        context = super(ProjectUpdateIndexPage, self).get_context(request)
        context['posts'] = ProjectUpdatePage.objects.descendant_of(
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
                msg = 'There are no project updates tagged with "{}"'.format(
                    tag)
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

    # Returns the child ProjectUpdatePage objects for this NewsPageIndex.
    # If a tag is used then it will filter the posts by tag.
    def get_posts(self, tag=None):
        posts = ProjectUpdatePage.objects.live().descendant_of(self)
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
