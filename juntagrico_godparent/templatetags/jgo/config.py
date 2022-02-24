from django import template

from juntagrico_godparent.config import GodparentConfig

register = template.Library()


@register.simple_tag
def jgo_config(prop):
    if hasattr(GodparentConfig, prop):
        return getattr(GodparentConfig, prop)()
