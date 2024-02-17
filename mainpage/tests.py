from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Reservation, Pitch, Item, BoughtItem
from django.urls import reverse
from django.utils import timezone
from users.models import Profile
from .additional_functions import generate_random_code
from urllib.parse import urlencode

# Create your tests here.
class TestReservePitch(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.pitch = Pitch.objects.create(
            name = 'testpitch',
            address = 'testaddress',
            phone_number = '12345678',
        )

    def test_reserve_pitch_valid(self):
        current_date = timezone.now().date()
        valid_datetime = timezone.datetime.combine(current_date, timezone.datetime.strptime('16:00', '%H:%M').time())
        valid_datetime = valid_datetime + timezone.timedelta(days=2)

        valid_datetime_str = valid_datetime.strftime('%Y-%m-%dT%H:%M')

        response = self.client.post(reverse('RFP:detail', args=[self.pitch.id]), {'datetime': valid_datetime_str})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Reservation.objects.count(), 1)


    def test_reserve_pitch_datetime_before_current(self):
        current_date = timezone.now().date()
        invalid_datetime = timezone.datetime.combine(current_date, timezone.datetime.strptime('16:00', '%H:%M').time())
        invalid_datetime = invalid_datetime - timezone.timedelta(days=2)

        invalid_datetime_str = invalid_datetime.strftime('%Y-%m-%dT%H:%M')

        response = self.client.post(reverse('RFP:detail', args=[self.pitch.id]), {'datetime': invalid_datetime_str})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Reservation.objects.count(), 0)

    def test_reserve_pitch_hours_invalid(self):
        current_date = timezone.now().date()
        invalid_datetime = timezone.datetime.combine(current_date, timezone.datetime.strptime('07:00', '%H:%M').time())
        invalid_datetime = invalid_datetime + timezone.timedelta(days=1)

        invalid_datetime_str = invalid_datetime.strftime('%Y-%m-%dT%H:%M')

        response = self.client.post(reverse('RFP:detail', args=[self.pitch.id]), {'datetime': invalid_datetime_str})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Reservation.objects.count(), 0)


class TestItems(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.profile = self.user.profile
        self.profile.tokens = 20
        self.profile.save()
        self.client.login(username='testuser', password='testpassword')

    def test_buy_item_valid(self):
        item_to_purchase = Item.objects.create(name='Item to Purchase', price=5)

        response = self.client.post(reverse('RFP:buy_item', args=[item_to_purchase.id]))

        updated_tokens = Profile.objects.get(user=self.user).tokens

        self.assertEqual(updated_tokens, 15)
        self.assertEqual(BoughtItem.objects.count(), 1)
        self.assertRedirects(response, reverse('RFP:bought_items'))

    def test_buy_item_not_enough_money(self):
        item_to_purchase = Item.objects.create(name='Item to Purchase', price=30)

        response = self.client.post(reverse('RFP:buy_item', args=[item_to_purchase.id]))

        updated_tokens = Profile.objects.get(user=self.user).tokens

        self.assertEqual(updated_tokens, 20)
        self.assertEqual(BoughtItem.objects.count(), 0)
        self.assertRedirects(response, reverse('RFP:shop'))

class TestJoinGame(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.profile = Profile.objects.get(user = self.user)
        self.client.login(username='testuser', password='testpassword')
        self.creator = User.objects.create_user(username='thecreator', email='creator@example.com', password='creatorishere')
        
        self.reservation = Reservation.objects.create(
            made_by = self.creator,
            reservation_code = generate_random_code()
        )

    def test_join_game_valid(self):
        self.creator_profile = Profile.objects.get(user = self.creator)
        self.creator_profile.friends.add(self.profile)
        self.creator_profile.save()
        reservation_code_to_join = self.reservation.reservation_code
        url = reverse('RFP:join_game') + '?' + urlencode({'input_code': reservation_code_to_join})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

        updated_reservation = Reservation.objects.get(reservation_code=reservation_code_to_join)
        self.assertTrue(self.user in updated_reservation.participants.all())
