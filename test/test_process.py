from django.urls import reverse

from juntagrico_godparent.models import Godchild
from test import JuntagricoTestCase


class ProcessTests(JuntagricoTestCase):

    def setUp(self):
        super().setUp()
        self.set_up_godchild_and_parent()
        # match
        self.godchild.godparent = self.godparent
        self.godchild.save()

    def run_process(self, member):
        # arranged
        response = self.assertGet(reverse('jgo:arranged', args=[self.godchild.id]), 302, member=member)
        self.assertRedirects(response, reverse('jgo:home'))
        self.godchild.refresh_from_db()
        self.assertEqual(self.godchild.progress, Godchild.ARRANGED)
        self.assertGet(reverse('jgo:home'), member=member)
        # done
        response = self.assertGet(reverse('jgo:done', args=[self.godchild.id]), 302, member=member)
        self.assertRedirects(response, reverse('jgo:home'))
        self.godchild.refresh_from_db()
        self.assertEqual(self.godchild.progress, Godchild.DONE)
        self.assertGet(reverse('jgo:home'), member=member)

    def testGodchild(self):
        self.run_process(self.godchild.member)

    def testGodparent(self):
        self.run_process(self.godparent.member)
