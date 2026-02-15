from django.db import models
from wagtail import blocks
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.fields import StreamField


class SocialBlock(blocks.StructBlock):
    provider = blocks.ChoiceBlock(
        choices=[
            ("facebook", "Facebook"),
            ("x", "X"),
            ("instagram", "Instagram"),
            ("threads", "Threads"),
        ]
    )
    url = blocks.URLBlock()


@register_setting
class FooterSettings(BaseGenericSetting):
    description = models.TextField(default="Novel App Shousetsu")
    social_media = StreamField(
        [("social", SocialBlock())], blank=True, use_json_field=True
    )
