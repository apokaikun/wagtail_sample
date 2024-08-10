from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    TextBlock,
    PageChooserBlock,
    ListBlock,
    URLBlock,
)


class PageBlock(StructBlock):
    # This title is used to override the referenced page's original title.
    title = CharBlock(max_length=255,
                      blank=True,
                      required=False,
                      help_text='Specify an altername title of the document.')
    page = PageChooserBlock(required=True)

    # class Meta:
    #     icon = 'page'
    #     # template = 'blocks/feature_block.html'


class PageStream(StreamBlock):
    section_title = CharBlock(max_length=255,
                              blank=True,
                              required=True,
                              help_text='Specify the title of this section.')
    pages = PageBlock()


class ImageBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """
    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)
    attribution = CharBlock(required=False)

    class Meta:
        icon = 'image'
        template = "blocks/image_block.html"


class HeadingBlock(StructBlock):
    """
    Custom `StructBlock` that allows the user to select h2 - h4 sizes for headers
    """
    heading_text = CharBlock(classname="title", required=True)
    size = ChoiceBlock(choices=[
        ('', 'Select a header size'),
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4')
    ], blank=True, required=False)

    class Meta:
        icon = "title"
        template = "blocks/heading_block.html"


class BlockQuote(StructBlock):
    """
    Custom `StructBlock` that allows the user to attribute a quote to the author
    """
    text = TextBlock()
    attribute_name = CharBlock(
        blank=True, required=False, label='e.g. Mary Berry')

    class Meta:
        icon = "fa-quote-left"
        template = "blocks/blockquote.html"


class HighlightItemsBlock(StreamBlock):
    """
    Custom Structblock that allows user to created highlights or summaries for the page.
    """
    text = ListBlock(child_block=CharBlock(
        max_length=512
    ),
        blank=True,
        required=True)


class HighlightsBlock(StructBlock):
    format = ChoiceBlock(choices=[
        ('normal', 'regular'),
        ('font-style : italic;', 'italic'),
        ('font-weight: bold;', 'bold'),
        ('font-style : italic; font-weight: bold;', 'bold-italic'),
    ], blank=True, required=True)
    highlight_items = HighlightItemsBlock()

    class Meta:
        icon = "list"
        template = "blocks/highlight.html"


class MultiColumnBlock(StreamBlock):
    paragraph_block = RichTextBlock(
        icon="fa-paragraph",
        template="blocks/paragraph_block.html"
    )
    image_block = ImageBlock()
    block_quote = BlockQuote()
    embed_block = EmbedBlock(
        help_text='Insert an embed URL like a video from Youtube.',
        icon="fa-s15",
        template="blocks/embed_block.html")

    class Meta:
        icon = 'fa-columns'
        template = "blocks/multi_block.html"

# StreamBlocks


class BaseStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """
    heading_block = HeadingBlock()
    highlight_block = HighlightsBlock()
    paragraph_block = RichTextBlock(
        icon="fa-paragraph",
        template="blocks/paragraph_block.html"
    )
    image_block = ImageBlock()
    block_quote = BlockQuote()
    embed_block = EmbedBlock(
        help_text='Insert an embed URL like a video from Youtube.',
        icon="fa-s15",
        template="blocks/embed_block.html")
    two_column_block = MultiColumnBlock(max_num=2, min_num=2)


class ReferenceBlock(StructBlock):
    """
    Custom Struckblock that allows user to created list of link urls.
    Useful when creating lists for Refences or Attributions.
    """

    reference = URLBlock()
    document = DocumentChooserBlock()

    class Meta:
        icon = 'page'
        verbose_name = 'Reference or Attibution'
        verbose_name_plural = 'References or Attributions'
