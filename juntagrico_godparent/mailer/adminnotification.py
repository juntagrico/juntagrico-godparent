"""
Admin notification emails
"""

from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from juntagrico.mailer import EmailSender, base_dict, organisation_subject

from juntagrico_godparent.config import GodparentConfig


def notify_on_godchild(godchild, existed):
    """
    notify admin when new godchild registers or changes profile
    """
    if contact := GodparentConfig.contact():
        EmailSender.get_sender(
            organisation_subject(_('Neumitglied geändert') if existed else _('Neues Neumitglied')),
            render_to_string('jgo/mails/admin/new_godchild.txt', base_dict(locals())),
        ).send_to(contact)


def notify_on_godparent(godparent, existed):
    """
    notify admin when new godparent registers or changes profile
    """
    if contact := GodparentConfig.contact():
        EmailSender.get_sender(
            organisation_subject(_('Pat*in geändert') if existed else _('Neue*r Pat*in')),
            render_to_string('jgo/mails/admin/new_godparent.txt', base_dict(locals())),
        ).send_to(contact)


def notify_on_godparent_increment(godparent):
    """
    notify admin when new godparent increments their max godchild count
    """
    if contact := GodparentConfig.contact():
        EmailSender.get_sender(
            organisation_subject(_('Pat*in wieder aktiv')),
            render_to_string('jgo/mails/admin/godparent_increment.txt', base_dict(locals())),
        ).send_to(contact)
