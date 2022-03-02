from django.conf import settings
from juntagrico.config import Config


class GodparentConfig:
    @staticmethod
    def contact():
        if hasattr(settings, 'GODPARENT_CONTACT'):
            return settings.GODPARENT_CONTACT
        return Config.info_email()

    @staticmethod
    def show_menu():
        if hasattr(settings, 'GODPARENT_SHOW_MENU'):
            return settings.GODPARENT_SHOW_MENU
        return True

    @staticmethod
    def godparent_membership_duration_limit():
        if hasattr(settings, 'GODPARENT_MEMBERSHIP_DURATION_LIMIT'):
            return settings.GODPARENT_MEMBERSHIP_DURATION_LIMIT
        return None
