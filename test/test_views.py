from django.urls import reverse
from test import JuntagricoTestCase


class ViewTests(JuntagricoTestCase):

    def testHome(self):
        self.assertGet(reverse('jgo:home'))
        self.assertGet(reverse('jgo:home'), member=self.member2)
        self.assertGet(reverse('jgo:home'), member=self.member5)  # test member without subscription

    def testGodparent(self):
        self.assertGet(reverse('jgo:godparent'))
        self.assertGet(reverse('jgo:godparent'), member=self.member5)  # test member without subscription
        self.assertPost(reverse('jgo:godparent'),
                        data={'max_godchildren': 1, 'languages': ["de"], 'slots': ["1am"], 'children': "on",
                              'areas': [1], 'phone': "012345678", 'accept_terms': "on"},
                        code=302)
        self.member.refresh_from_db()
        self.assertEqual(self.member.godparent.languages[0], "de")
        self.assertGet(reverse('jgo:home'))
        self.assertGet(reverse('jgo:increment-max-godchildren'), code=302)
        self.member.refresh_from_db()
        self.assertEqual(self.member.godparent.max_godchildren, 2)
        self.assertGet(reverse('jgo:leave'), code=302)
        self.member.refresh_from_db()
        self.assertFalse(hasattr(self.member, 'godparent'))

    def testGodchild(self):
        self.assertGet(reverse('jgo:godchild'))
        self.assertGet(reverse('jgo:godchild'), member=self.member5)  # test member without subscription
        self.assertPost(reverse('jgo:godchild'),
                        data={'languages': "de", 'slots': "1am", 'children': "on", 'talents': "", 'areas': "1",
                              'comments': "", 'phone': "012345678", 'accept_terms': "on", 'submit': "Anmelden"},
                        code=302)
        self.member.refresh_from_db()
        self.assertEqual(self.member.godchild.languages[0], "de")
        self.assertGet(reverse('jgo:home'))
        self.assertGet(reverse('jgo:leave'), code=302)
        self.member.refresh_from_db()
        self.assertFalse(hasattr(self.member, 'godchild'))
