from django import template
from django.utils import timezone

from juntagrico_godparent.config import GodparentConfig

register = template.Library()


@register.simple_tag
def jgo_config(prop):
    if hasattr(GodparentConfig, prop):
        return getattr(GodparentConfig, prop)()


@register.filter
def can_be_godparent(user):
    limit = GodparentConfig.godparent_membership_duration_limit()
    return limit is None or user.date_joined < timezone.now() - limit


@register.filter
def can_be_godchild(user):
    limit = GodparentConfig.godparent_membership_duration_limit()
    return limit is None or user.date_joined >= timezone.now() - limit
