"""
Admin notification emails
"""
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from juntagrico.mailer import EmailSender, base_dict, organisation_subject

from juntagrico_godparent.config import GodparentConfig
from juntagrico_godparent.models import Godchild, Godparent
from juntagrico_godparent.signals import created, changed, reactivated


@receiver(created, sender=Godchild, dispatch_uid='notify_on_godchild')
def notify_on_godchild(instance, existed=False, **kwargs):
    """
    notify admin when new godchild registers or changes profile
    """
    godchild = instance
    if contact := GodparentConfig.contact():
        EmailSender.get_sender(
            organisation_subject(_('Neumitglied geändert') if existed else _('Neues Neumitglied')),
            render_to_string('jgo/mails/admin/new_godchild.txt', base_dict(locals())),
        ).send_to(contact)


@receiver(changed, sender=Godchild, dispatch_uid='notify_on_changed_godchild')
def notify_on_changed_godchild(instance, **kwargs):
    notify_on_godchild(instance, True, **kwargs)


@receiver(created, sender=Godparent, dispatch_uid='notify_on_godparent')
def notify_on_godparent(instance, existed=False, **kwargs):
    """
    notify admin when new godparent registers or changes profile
    """
    godparent = instance
    if contact := GodparentConfig.contact():
        EmailSender.get_sender(
            organisation_subject(_('Pat*in geändert') if existed else _('Neue*r Pat*in')),
            render_to_string('jgo/mails/admin/new_godparent.txt', base_dict(locals())),
        ).send_to(contact)


@receiver(changed, sender=Godparent, dispatch_uid='notify_on_changed_godparent')
def notify_on_changed_godparent(instance, **kwargs):
    notify_on_godchild(instance, True, **kwargs)


@receiver(reactivated, sender=Godparent, dispatch_uid='notify_on_godparent_increment')
def notify_on_godparent_increment(instance, **kwargs):
    """
    notify admin when new godparent increments their max godchild count
    """
    godparent = instance
    if contact := GodparentConfig.contact():
        EmailSender.get_sender(
            organisation_subject(_('Pat*in wieder aktiv')),
            render_to_string('jgo/mails/admin/godparent_increment.txt', base_dict(locals())),
        ).send_to(contact)
