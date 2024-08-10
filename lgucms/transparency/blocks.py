from tabnanny import verbose
from wagtail.embeds.blocks import EmbedBlock
from wagtail.blocks import (
    CharBlock, ChoiceBlock, RichTextBlock, StreamBlock, StructBlock, ListBlock
)

from lgucms.base.blocks import (
    PageBlock,
    ImageBlock,
    HeadingBlock,
    HighlightBlock,

)

class PageListBlock(PageBlock):
    page_title = CharBlock(max_length=255, blank=True, required=True)

    class Meta:
        icon = 'page'
        # template = 'blocks/feature_block.html' 

class DocumentListBlock(StructBlock):
    """
    Custom Structblock that allows user to created highlights or summaries for the page.
    """
    section_title = CharBlock(max_length=255, blank=True, required=True)

    items = ListBlock(child_block=
        PageListBlock(), blank=True, required=True)
    
    class Meta:
        icon = "list"
        verbose_name = "Document List"
        verbose_name_plural = "Documents List"
        template = "block/highlight.html"


# StreamBlocks
class BaseStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """
    heading_block = HeadingBlock()
    highlight_block = HighlightBlock()
    paragraph_block = RichTextBlock(
        icon="fa-paragraph",
        template="blocks/paragraph_block.html"
    )
    image_block = ImageBlock()
    document_list = DocumentListBlock()
