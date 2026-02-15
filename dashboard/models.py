from django.db import models
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting


@register_setting
class FooterSettings(BaseGenericSetting):
    description = models.TextField(default="Novel App Shousetsu")
