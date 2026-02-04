from django.db import models
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Orderable, Page, ParentalKey
from wagtail.fields import RichTextField


class ArcIndexPage(Page):
    description = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("description")]


class ArcDetailPage(Page):
    description = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        InlinePanel("arc_thumbnail", label="Arc Thumbnail"),
        FieldPanel("description"),
    ]


class ChapterPage(Page):
    content = RichTextField()
    postscript = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        InlinePanel("chapter_thumbnail", label="Chapter Thumbnail"),
        FieldPanel("content"),
        FieldPanel("postscript"),
    ]


class ArcThumbnail(Orderable):
    page = ParentalKey(
        ArcDetailPage, related_name="arc_thumbnail", on_delete=models.CASCADE
    )

    image = models.ForeignKey(
        "wagtailimages.image", related_name="+", on_delete=models.CASCADE
    )

    panels = [FieldPanel("image")]


class ChapterThumbnail(Orderable):
    page = ParentalKey(
        ChapterPage, related_name="chapter_thumbnail", on_delete=models.CASCADE
    )

    image = models.ForeignKey(
        "wagtailimages.image", related_name="+", on_delete=models.CASCADE
    )

    panels = [FieldPanel("image")]
