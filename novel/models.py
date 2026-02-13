import math

from django.db import models
from django.utils.html import strip_tags
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from wagtail.fields import RichTextField


class ArcIndexPage(Page):
    max_count = 1
    description = RichTextField(blank=True)
    readers_note = models.TextField(
        default="Arc disarankan dibaca secara berurutan untuk mendapatkan pengalaman cerita yang utuh. Beberapa detail kecil di awal akan memiliki dampak besar di arc berikutnya."
    )

    content_panels = Page.content_panels + [
        FieldPanel("readers_note"),
        FieldPanel("description"),
    ]
    parent_page_types = ["home.HomePage"]
    subpage_types = ["ArcDetailPage"]

    def get_context(self, request):
        context = super().get_context(request)
        arcs = ArcDetailPage.objects.live().order_by("-first_published_at")  # pyright: ignore

        context["arcs"] = arcs
        return context

    def save(self, *args, **kwargs):
        self.slug = "arcs"
        super().save(*args, **kwargs)


class ArcStatusChoices(models.TextChoices):
    ONGOING = "ongoing", "Ongoing"
    COMPLETED = "completed", "Completed"


class ArcDetailPage(Page):
    arc_number = models.PositiveIntegerField(editable=False, blank=True)
    status = models.CharField(
        max_length=20,
        choices=ArcStatusChoices.choices,
        default=ArcStatusChoices.ONGOING,
    )
    description = RichTextField(blank=True)
    thumbnail = models.ForeignKey(
        "wagtailimages.image",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("status"),
        FieldPanel("thumbnail"),
        FieldPanel("description"),
    ]
    parent_page_types = ["ArcIndexPage"]
    subpage_types = ["ChapterPage"]

    def get_context(self, request):
        context = super().get_context(request)
        chapters = self.get_children().live().order_by("-first_published_at")  # pyright: ignore

        first_chapter = chapters.last()

        context["chapters"] = chapters
        context["first_chapter"] = first_chapter
        return context

    def save(self, *args, **kwargs):
        if not self.arc_number:
            siblings = ArcDetailPage.objects.child_of(self.get_parent()).exclude(  # pyright: ignore
                pk=self.pk
            )
            max_number = (
                siblings.aggregate(models.Max("arc_number"))["arc_number__max"] or 0
            )

            self.arc_number = max_number + 1

        super().save(*args, **kwargs)


class ChapterPage(Page):
    chapter_number = models.PositiveIntegerField(editable=False, blank=True)
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

    @property
    def reading_time(self):
        text = strip_tags(self.content)
        words = text.split()
        return max(1, math.ceil(len(words) / 200))

    @property
    def prev_chapter(self):
        return self.get_prev_sibling() if self.get_prev_sibling() else None

    @property
    def next_chapter(self):
        return self.get_next_sibling() if self.get_next_sibling() else None

    def save(self, *args, **kwargs):
        if not self.chapter_number:
            siblings = ChapterPage.objects.child_of(self.get_parent()).exclude(  # pyright: ignore
                pk=self.pk
            )
            max_number = (
                siblings.aggregate(models.Max("chapter_number"))["chapter_number__max"]
                or 0
            )

            self.chapter_number = max_number + 1

        super().save(*args, **kwargs)
