from django.contrib.auth.models import Permission
from django.test import TestCase, override_settings
from django.utils import timezone
from django.core import mail

from juntagrico.entity.depot import Depot
from juntagrico.entity.jobs import ActivityArea
from juntagrico.entity.location import Location
from juntagrico.entity.member import Member
from juntagrico.entity.subs import Subscription, SubscriptionPart
from juntagrico.entity.subtypes import SubscriptionProduct, SubscriptionSize, SubscriptionType

from juntagrico_godparent.models import Godparent, Godchild


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class JuntagricoTestCase(TestCase):

    def setUp(self):
        self.set_up_member()
        self.set_up_admin()
        self.set_up_area()
        self.set_up_location()
        self.set_up_depots()
        self.set_up_sub_types()
        self.set_up_sub()
        mail.outbox.clear()

    @staticmethod
    def create_member(email):
        member_data = {'first_name': 'first_name',
                       'last_name': 'last_name',
                       'email': email,
                       'addr_street': 'addr_street',
                       'addr_zipcode': 'addr_zipcode',
                       'addr_location': 'addr_location',
                       'phone': 'phone',
                       'mobile_phone': 'phone',
                       'confirmed': True,
                       }
        member = Member.objects.create(**member_data)
        member.user.set_password('12345')
        member.user.save()
        return member

    def set_up_member(self):
        """
            member
        """
        self.member = self.create_member('email1@email.org')
        self.member2 = self.create_member('email2@email.org')
        self.member3 = self.create_member('email3@email.org')
        self.member4 = self.create_member('email4@email.org')
        self.member5 = self.create_member('email5@email.org')
        self.member.user.user_permissions.add(
            Permission.objects.get(codename='is_depot_admin'))
        self.member.user.user_permissions.add(
            Permission.objects.get(codename='is_area_admin'))
        self.member.user.user_permissions.add(
            Permission.objects.get(codename='can_filter_members'))
        self.member.user.user_permissions.add(
            Permission.objects.get(codename='can_filter_subscriptions'))
        self.member.user.user_permissions.add(
            Permission.objects.get(codename='change_subscription'))
        self.member.user.user_permissions.add(
            Permission.objects.get(codename='change_member'))
        self.member.user.user_permissions.add(
            Permission.objects.get(codename='change_share'))
        self.member.user.user_permissions.add(
            Permission.objects.get(codename='change_assignment'))
        self.member.user.user_permissions.add(
            Permission.objects.get(codename='change_subscriptionpart'))
        self.member.user.user_permissions.add(
            Permission.objects.get(codename='can_view_lists'))
        self.member.user.user_permissions.add(
            Permission.objects.get(codename='can_view_exports'))
        self.member.user.user_permissions.add(
            Permission.objects.get(codename='is_operations_group'))
        self.member.user.user_permissions.add(
            Permission.objects.get(codename='can_send_mails'))
        self.member.user.user_permissions.add(
            Permission.objects.get(codename='can_load_templates'))
        self.member.user.user_permissions.add(
            Permission.objects.get(codename='change_subscriptionpart'))
        self.member.user.user_permissions.add(
            Permission.objects.get(codename='notified_on_subscription_creation'))
        self.member.user.user_permissions.add(
            Permission.objects.get(codename='notified_on_member_creation'))
        self.member.user.user_permissions.add(
            Permission.objects.get(codename='notified_on_share_creation'))
        self.member.user.save()

    def set_up_admin(self):
        """
        admin members
        """
        self.admin = self.create_member('admin@email.org')
        self.admin.user.set_password("123456")
        self.admin.user.is_staff = True
        self.admin.user.is_superuser = True
        self.admin.user.save()
        self.area_admin = self.create_member('areaadmin@email.org')
        self.area_admin.user.set_password("123456")
        self.area_admin.user.is_staff = True
        self.area_admin.user.user_permissions.add(
            Permission.objects.get(codename='is_area_admin'))
        self.area_admin.user.user_permissions.add(
            Permission.objects.get(codename='change_activityarea'))
        self.area_admin.user.user_permissions.add(
            Permission.objects.get(codename='change_assignment'))
        self.area_admin.user.user_permissions.add(
            Permission.objects.get(codename='change_jobtype'))
        self.area_admin.user.user_permissions.add(
            Permission.objects.get(codename='change_recuringjob'))
        self.area_admin.user.user_permissions.add(
            Permission.objects.get(codename='change_onetimejob'))
        self.area_admin.user.save()

    def set_up_area(self):
        """
        area
        """
        area_data = {'name': 'name',
                     'coordinator': self.area_admin,
                     'auto_add_new_members': True}
        area_data2 = {'name': 'name2',
                      'coordinator': self.area_admin,
                      'hidden': True}
        self.area = ActivityArea.objects.create(**area_data)
        self.area2 = ActivityArea.objects.create(**area_data2)
        self.member.areas.add(self.area)
        self.member.save()

    def set_up_location(self):
        """
        location
        """
        location_data_depot = {'name': 'Depot location',
                               'latitude': '12.513',
                               'longitude': '1.314',
                               'addr_street': 'Fakestreet 123',
                               'addr_zipcode': '1000',
                               'addr_location': 'Faketown',
                               'description': 'Place to be'}
        self.location_depot = Location.objects.create(**location_data_depot)

    def set_up_depots(self):
        """
        depots
        """
        depot_data = {
            'name': 'depot',
            'contact': self.member,
            'weekday': 1,
            'location': self.location_depot}
        self.depot = Depot.objects.create(**depot_data)
        depot_data = {
            'name': 'depot2',
            'contact': self.member,
            'weekday': 1,
            'location': self.location_depot}
        self.depot2 = Depot.objects.create(**depot_data)

    def set_up_sub_types(self):
        """
        subscription product, size and types
        """
        sub_product_data = {
            'name': 'product'
        }
        self.sub_product = SubscriptionProduct.objects.create(**sub_product_data)
        sub_size_data = {
            'name': 'sub_name',
            'long_name': 'sub_long_name',
            'units': 1,
            'visible': True,
            'depot_list': True,
            'product': self.sub_product,
            'description': 'sub_desc'
        }
        self.sub_size = SubscriptionSize.objects.create(**sub_size_data)
        sub_type_data = {
            'name': 'sub_type_name',
            'long_name': 'sub_type_long_name',
            'size': self.sub_size,
            'shares': 1,
            'visible': True,
            'required_assignments': 10,
            'price': 1000,
            'description': 'sub_type_desc'}
        self.sub_type = SubscriptionType.objects.create(**sub_type_data)
        sub_type_data = {
            'name': 'sub_type_name2',
            'long_name': 'sub_type_long_name',
            'size': self.sub_size,
            'shares': 2,
            'visible': True,
            'required_assignments': 10,
            'price': 1000,
            'description': 'sub_type_desc'}
        self.sub_type2 = SubscriptionType.objects.create(**sub_type_data)

    def set_up_sub(self):
        """
        subscription
        """
        sub_data = {'depot': self.depot,
                    'future_depot': None,
                    'activation_date': timezone.now().date(),
                    'deactivation_date': None,
                    'creation_date': '2017-03-27',
                    'start_date': '2018-01-01',
                    }
        sub_data2 = {'depot': self.depot,
                     'future_depot': None,
                     'activation_date': None,
                     'deactivation_date': None,
                     'creation_date': '2017-03-27',
                     'start_date': '2018-01-01'
                     }
        self.sub = Subscription.objects.create(**sub_data)
        self.sub2 = Subscription.objects.create(**sub_data2)
        self.member.join_subscription(self.sub)
        self.sub.primary_member = self.member
        self.sub.save()
        self.member3.join_subscription(self.sub)
        self.member2.join_subscription(self.sub2)
        self.sub2.primary_member = self.member2
        self.sub2.save()
        SubscriptionPart.objects.create(subscription=self.sub, type=self.sub_type)

    def set_up_godchild_and_parent(self):
        self.godparent = Godparent.objects.create(
            member=self.member,
            max_godchildren=1,
            languages=["de"],
            slots=["1am"],
            children=True
        )
        self.godchild = Godchild.objects.create(
            member=self.member2,
            languages=["de"],
            slots=["1am"],
            children=True
        )
        self.godchild2 = Godchild.objects.create(
            member=self.member3,
            languages=["en"],
            slots=["1am"],
            children=False
        )
        self.member.user.user_permissions.add(
            Permission.objects.get(codename='can_make_matches'))

    def assertGet(self, url, code=200, member=None):
        login_member = member or self.member
        self.client.force_login(login_member.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, code)
        return response

    def assertPost(self, url, data=None, code=200, member=None):
        login_member = member or self.member
        self.client.force_login(login_member.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, code)
        return response
