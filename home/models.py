from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from novel.models import ArcDetailPage


class HomePage(Page):
    description = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("description")]

    def get_context(self, request):
        context = super().get_context(request)
        latest_arc = ArcDetailPage.objects.live().order_by("-arc_number").first()  # pyright: ignore

        context["latest_arc"] = latest_arc

        return context
