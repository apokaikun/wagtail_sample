from django.db import models


from wagtail.admin.panels import (
    FieldPanel,
)
from wagtail.fields import StreamField
from wagtail.models import Collection, Page
from wagtail.search import index
from wagtail.images.models import Image

from lgucms.base.blocks import BaseStreamBlock


class GalleryPage(Page):
    """
    This is a page to list images from the selected Collection. We use a Q
    object to list any Collection created (/admin/collections/) even if they
    contain no items. 
    """

    introduction = models.TextField(
        help_text='Text to describe this page',
        blank=True)
    feature_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Select an image to feature.'
    )
    body = StreamField(
        BaseStreamBlock(),
        verbose_name="Page body",
        blank=True,
        use_json_field=True,
        help_text="Feeling creative? Word up and paint a better picture."
    )
    collection = models.ForeignKey(
        Collection,
        limit_choices_to=~models.Q(name__in=['Root']),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text='Select the image collection for this gallery.'
    )

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        FieldPanel('body'),
        FieldPanel('feature_image'),
        FieldPanel('collection'),
    ]

    # Defining what content type can sit under the parent. Since it's a blank
    # array no subpage can be added
    subpage_types = []

    def get_context(self, request):
        context = super().get_context(request)
        images = Image.objects.filter(
            collection=self.collection).prefetch_renditions("width-1080", "width-320")
        collection_name = self.collection.name

        context['collection_name'] = collection_name
        context['images'] = images
        return context

# Todo: Create an index page for galleries. Resize image to smaller sizes.
# Link gallery titles to gallery page.


class GalleryIndexPage(Page):
    subpage_type = ['GalleryPage']
