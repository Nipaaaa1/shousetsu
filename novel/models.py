from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from wagtail.fields import RichTextField


class ArcIndexPage(Page):
    description = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("description")]
    subpage_types = ["ArcDetailPage"]

    def get_context(self, request):
        context = super().get_context(request)
        arcs = ArcDetailPage.objects.live().order_by("-first_published_at")  # pyright: ignore

        context["arcs"] = arcs
        return context


class ArcDetailPage(Page):
    description = RichTextField(blank=True)
    thumbnail = models.ForeignKey(
        "wagtailimages.image",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("thumbnail"),
        FieldPanel("description"),
    ]
    parent_page_types = ["ArcIndexPage"]
    subpage_types = ["ChapterPage"]

    def get_context(self, request):
        context = super().get_context(request)
        chapters = ChapterPage.objects.live().order_by("-first_published_at")  # pyright: ignore

        context["chapters"] = chapters
        return context


class ChapterPage(Page):
    content = RichTextField()
    thumbnail = models.ForeignKey(
        "wagtailimages.image",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    postscript = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("thumbnail"),
        FieldPanel("content"),
        FieldPanel("postscript"),
    ]
    parent_page_types = ["ArcDetailPage"]
