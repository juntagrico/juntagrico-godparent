from django.urls import reverse

from juntagrico_godparent.models import Godchild
from test import JuntagricoTestCase


class MatcherViewTests(JuntagricoTestCase):

    def setUp(self):
        super().setUp()
        self.set_up_godchild_and_parent()

    def testMatch(self):
        self.assertGet(reverse('jgo:manage-match'))
        self.assertGet(reverse('jgo:manage-match'), member=self.member2, code=302)
        self.assertPost(reverse('jgo:manage-match'), data={'match-1-1': "on"})
        self.godchild.refresh_from_db()
        self.assertEqual(self.godchild.godparent, self.member.godparent)
        self.assertGet(reverse('jgo:manage-matched'))
        self.assertGet(reverse('jgo:manage-matched-removed'))
        self.assertGet(reverse('jgo:manage-matched'), member=self.member2, code=302)
        # test views of godchild and godparent
        self.assertGet(reverse('jgo:godchild'), member=self.member2)
        self.assertGet(reverse('jgo:godparent'))
        # test unmatch
        self.assertGet(reverse('jgo:manage-unmatch', args=[self.godchild.id]), code=302)
        self.godchild.refresh_from_db()
        self.assertIsNone(self.godchild.godparent)

    def testUnmatchable(self):
        self.assertGet(reverse('jgo:manage-unmatchable'))
        self.assertGet(reverse('jgo:manage-unmatchable'), member=self.member2, code=302)
        self.assertPost(reverse('jgo:manage-unmatchable'), data={'godparent': self.godparent.id,
                                                                 'godchild': self.godchild2.id})
        self.godchild2.refresh_from_db()
        self.assertEqual(self.godchild2.godparent, self.member.godparent)
        self.assertGet(reverse('jgo:manage-matched'))
        self.assertGet(reverse('jgo:manage-matched'), member=self.member2, code=302)
        # test views of godchild and godparent
        self.assertGet(reverse('jgo:godchild'), member=self.member3)
        self.assertGet(reverse('jgo:godparent'))
        # test unmatch
        self.assertGet(reverse('jgo:manage-unmatch', args=[self.godchild2.id]), code=302)
        self.godchild2.refresh_from_db()
        self.assertIsNone(self.godchild2.godparent)

    def testCompleted(self):
        self.godchild.godparent = self.godparent
        self.godchild.progress = Godchild.DONE
        self.godchild.save()
        self.assertGet(reverse('jgo:manage-completed'))
