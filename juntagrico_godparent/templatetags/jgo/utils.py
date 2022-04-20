from django import template
from juntagrico.util.temporal import weekdays

register = template.Library()


@register.simple_tag
def member_subscription(member):
    return member.subscription_future or member.subscription_current


@register.simple_tag
def weekday_from_option(option, length=None):
    weekday = weekdays[int(option[0])]
    if length:
        return weekday[:length]
    return weekday
