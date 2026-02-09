from django.db import models
from wagtail import blocks
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from novel.models import ArcDetailPage


class HomePage(Page):
    genres = StreamField(
        [
            ("genre", blocks.CharBlock(label="Genre"))
        ],
        use_json_field=True,
        blank=True
    )
    description = RichTextField(blank=True)
    quote_text = models.TextField(blank=True)
    quote_author = models.CharField(blank=True, max_length=255)
 
    content_panels = Page.content_panels + [
        FieldPanel("genres"),
        FieldPanel("description"),
        FieldPanel("quote_text"),
        FieldPanel("quote_author"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        latest_arc = ArcDetailPage.objects.live().order_by("-arc_number").first()  # pyright: ignore

        context["latest_arc"] = latest_arc

        return context
