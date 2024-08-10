from __future__ import unicode_literals
from wagtail.search import index

from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
)
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.snippets.models import register_snippet

from .blocks import BaseStreamBlock, ImageBlock, PageBlock


# Start of snippet section.
# Snippets Sections: Allows Administrator to set standard Header and Footer.
@register_snippet
class FooterText(models.Model):
    """
    This provides editable text for the site footer. Again it uses the decorator
    `register_snippet` to allow it to be accessible via the admin. It is made
    accessible on the template via a template tag defined in base/templatetags/
    navigation_tags.py
    """

    body = RichTextField()

    panels = [
        FieldPanel('body'),
    ]

    def __str__(self):
        return "Footer text"

    class Meta:
        verbose_name_plural = 'Footer Text'


@register_snippet
class HeaderText(models.Model):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.',
        verbose_name='hero image'
    )

    panels = [
        FieldPanel('image')
    ]

    def __str__(self):
        return "Footer text"

    class Meta:
        verbose_name_plural = 'Header Text'

# End of snippets section.

# Base model for a standar page.


class StandardPage(Page):
    """
    A generic content page. On this demo site we use it for an about page but
    it could be used for any type of page content that only needs a title,
    image, introduction and body field
    Fields: 
        introduction - short description of the page
        image - an image used to override the standard header image.
        feature_image - page's featured image, displayed in column's max width.
            - this image is also referenced in index pages or feature pages.
    """

    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True,
        verbose_name='Introduction or Summary')

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
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.',
        verbose_name='feature image'
    )

    body = StreamField(
        BaseStreamBlock(),
        verbose_name="Page body",
        blank=True,
        use_json_field=True,
    )
    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        FieldPanel('body'),
        FieldPanel('image'),
        FieldPanel('feature_image'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('title', partial_match=True),
        index.SearchField('introduction', partial_match=True),
        index.SearchField('body', partial_match=True)
    ]


class FeaturePage(Page):
    """
    An index page to manually select different pages to feature.
    A subclass of the standard page to inheret the basic properties of a standard page 
    plus the addition to add multiple pages as features.
    """
    name = 'featurepage'

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.',
        verbose_name='hero image'
    )

    body = StreamField(
        PageBlock(),
        use_json_field=True,
        verbose_name='Feature page'
    )

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('image'),
    ]


class HomePage(Page):
    """
    The Home Page. This looks slightly more complicated than it is. You can
    see if you visit your site and edit the homepage that it is split between
    a:
    - Hero area
    - Body area
    - A promotional area
    - Moveable featured site sections
    """

    # Hero section of HomePage
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Homepage image'
    )
    hero_text = models.CharField(
        max_length=255,
        help_text='Write an introduction for the site',
        default=""
    )
    hero_cta = models.CharField(
        verbose_name='Hero CTA',
        max_length=255,
        help_text="Text to display on Hero's Call to Action",
        default="Read More"
    )
    hero_cta_link = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Hero CTA link',
        help_text="Choose a page to link to for the Hero's Call to Action"
    )

    # Body section of the HomePage
    body = StreamField(
        BaseStreamBlock(), verbose_name="Home content block", blank=True, use_json_field=True
    )

    body_cta = models.CharField(
        verbose_name='Body CTA',
        max_length=255,
        help_text="Text to display on Body's Call to Action",
        default="Read More"
    )

    body_cta_link = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Body CTA link',
        help_text="Choose a page to link to for the Body's Call to Action"
    )

    # Promo section of the HomePage

    promo = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Section to display important messages.',
        verbose_name='Special Section'
    )

    # Featured sections on the HomePage
    # You will see on templates/base/home_page.html that these are treated
    # in different ways, and displayed in different areas of the page.
    # Each list their children items that we access via the children function
    # that we define on the individual Page models e.g. NewsIndexPage

    # Featured Section 1
    # Appears at the left side of Promo section.
    featured_section_1_title = models.CharField(
        blank=True,
        max_length=255,
        help_text='Title to display above the promo copy'
    )
    featured_section_1 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='First featured section for the homepage. Will display up to '
        'three child items.',
        verbose_name='Featured section 1'
    )

    featured_section_2_title = models.CharField(
        blank=True,
        max_length=255,
        help_text='Title to display above the promo copy'
    )
    featured_section_2 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Second featured section for the homepage. Will display up to '
        'three child items.',
        verbose_name='Featured section 2'
    )

    featured_section_3_title = models.CharField(
        blank=True,
        max_length=255,
        help_text='Title to display above the promo copy'
    )
    featured_section_3 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Third featured section for the homepage. Will display up to '
        'six child items.',
        verbose_name='Featured section 3'
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('image'),
            FieldPanel('hero_text', classname="full"),
            MultiFieldPanel([
                FieldPanel('hero_cta'),
                FieldPanel('hero_cta_link'),
            ]),
        ], heading="Hero section"),
        MultiFieldPanel([
            # FieldPanel('promo_image'),
            # FieldPanel('promo_title'),
            # FieldPanel('promo_text'),
            FieldPanel('promo')
        ], heading="Promo section"),
        MultiFieldPanel([
            FieldPanel('body'),
            FieldPanel('body_cta'),
            FieldPanel('body_cta_link'),
        ], heading="Homepage's Body sections"),
        MultiFieldPanel([
            MultiFieldPanel([
                FieldPanel('featured_section_1_title'),
                FieldPanel('featured_section_1'),
            ]),
            MultiFieldPanel([
                FieldPanel('featured_section_2_title'),
                FieldPanel('featured_section_2'),
            ]),
            MultiFieldPanel([
                FieldPanel('featured_section_3_title'),
                FieldPanel('featured_section_3'),
            ]),
        ], heading="Featured homepage sections", classname="collapsible")
    ]

    def __str__(self):
        return self.title


class FormField(AbstractFormField):
    """
    Wagtailforms is a module to introduce simple forms on a Wagtail site. It
    isn't intended as a replacement to Django's form support but as a quick way
    to generate a general purpose data-collection form or contact form
    without having to write code. We use it on the site for a contact form. You
    can read more about Wagtail forms at:
    https://docs.wagtail.org/en/stable/reference/contrib/forms/index.html
    """
    page = ParentalKey('FormPage', related_name='form_fields',
                       on_delete=models.CASCADE)


class FormPage(AbstractEmailForm):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField(BaseStreamBlock(), use_json_field=True)
    thank_you_text = RichTextField(blank=True)

    # Note how we include the FormField object via an InlinePanel using the
    # related_name value
    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('image'),
        FieldPanel('body'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]
