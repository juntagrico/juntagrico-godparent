"""
Member notification emails
"""
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from juntagrico.mailer import EmailSender, base_dict
from juntagrico.util.organisation_name import enriched_organisation

from juntagrico_godparent.config import GodparentConfig
from juntagrico_godparent.signals import matched


@receiver(matched, dispatch_uid='notify_matched_members')
def notify_matched_members(godchild, matcher, **kwargs):
    godparent = godchild.godparent
    # inform godchild
    EmailSender.get_sender(
        _('Dein*e Gotte/Götti bei {0}').format(enriched_organisation('D')),
        render_to_string('jgo/mails/member/found_godparent.txt', base_dict(locals())),
        from_email=GodparentConfig.contact()
    ).send_to(godchild.member.email)
    # inform godparent
    EmailSender.get_sender(
        _('Deine Patenschaft bei {0}').format(enriched_organisation('D')),
        render_to_string('jgo/mails/member/found_godchild.txt', base_dict(locals())),
        from_email=GodparentConfig.contact()
    ).send_to(godparent.member.email)
