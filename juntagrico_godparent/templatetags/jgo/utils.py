from django import template
from juntagrico.util.temporal import weekdays
from juntagrico_godparent.util import utils

register = template.Library()


@register.simple_tag
def member_depot(member):
    return utils.member_depot(member)


@register.simple_tag
def member_subscription(member):
    return member.subscription_future or member.subscription_current


@register.simple_tag
def weekday_from_option(option, length=None):
    weekday = weekdays[int(option[0])]
    if length:
        return weekday[:length]
    return weekday
