from django.contrib.auth.models import Permission

from juntagrico.tests import JuntagricoTestCase

from juntagrico_godparent.models import Godparent, Godchild


class JuntagricoGodparentTestCase(JuntagricoTestCase):

    @classmethod
    def setUpTestData(cls):
        # load from fixtures
        cls.load_members()
        cls.load_areas()
        # setup other objects
        cls.set_up_depots()
        cls.set_up_sub_types()
        cls.set_up_sub()

    @classmethod
    def set_up_godchild_and_parent(cls):
        cls.godparent = Godparent.objects.create(
            member=cls.member,
            max_godchildren=1,
            languages=["de"],
            slots=["1am"],
            children=True
        )
        cls.godchild = Godchild.objects.create(
            member=cls.member2,
            languages=["de"],
            slots=["1am"],
            children=True
        )
        cls.godchild2 = Godchild.objects.create(
            member=cls.member3,
            languages=["en"],
            slots=["1am"],
            children=False
        )
        cls.member.user.user_permissions.add(
            Permission.objects.get(codename='can_make_matches'))
