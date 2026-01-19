from django import template

from juntagrico_godparent.models import week_slots_choices
from juntagrico_godparent.util import utils

register = template.Library()


@register.simple_tag
def member_depot(member):
    return utils.member_depot(member)


@register.simple_tag
def member_subscription(member):
    return member.subscription_future or member.subscription_current


@register.inclusion_tag('jgo/snippets/slot_grid.html')
def slot_grid(slots, matching_slots):
    return {
        'slots': slots,
        'matching_slots': matching_slots,
        'choices': [
            (weekday[:2], option[0])
            for weekday, options in week_slots_choices()
            for option in options
        ]
    }
