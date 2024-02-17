from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Reservation, Pitch, Item, BoughtItem
from django.urls import reverse
from django.utils import timezone
from users.models import Profile
from .additional_functions import generate_random_code

# Create your tests here.
class TestReservePitch(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username = 'testuser', email = 'test@example.com', password = 'testpassword')
        self.client.login(username = 'testuser', password = 'testpassword')
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

        response = self.client.post(reverse('RFP:detail', args = [self.pitch.id]), {'datetime': valid_datetime_str})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Reservation.objects.count(), 1)


    def test_reserve_pitch_datetime_before_current(self):
        current_date = timezone.now().date()
        invalid_datetime = timezone.datetime.combine(current_date, timezone.datetime.strptime('16:00', '%H:%M').time())
        invalid_datetime = invalid_datetime - timezone.timedelta(days = 2)

        invalid_datetime_str = invalid_datetime.strftime('%Y-%m-%dT%H:%M')

        response = self.client.post(reverse('RFP:detail', args=[self.pitch.id]), {'datetime': invalid_datetime_str})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Reservation.objects.count(), 0)

    def test_reserve_pitch_hours_invalid(self):
        current_date = timezone.now().date()
        invalid_datetime = timezone.datetime.combine(current_date, timezone.datetime.strptime('07:00', '%H:%M').time())
        invalid_datetime = invalid_datetime + timezone.timedelta(days = 1)

        invalid_datetime_str = invalid_datetime.strftime('%Y-%m-%dT%H:%M')

        response = self.client.post(reverse('RFP:detail', args = [self.pitch.id]), {'datetime': invalid_datetime_str})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Reservation.objects.count(), 0)


class TestItems(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username = 'testuser', email = 'test@example.com', password = 'testpassword')
        self.profile = self.user.profile
        self.profile.tokens = 20
        self.profile.save()
        self.client.login(username ='testuser', password ='testpassword')

    def test_buy_item_valid(self):
        item_to_purchase = Item.objects.create(name = 'Item to Purchase', price = 5)

        response = self.client.post(reverse('RFP:buy_item', args = [item_to_purchase.id]))

        updated_tokens = Profile.objects.get(user = self.user).tokens

        self.assertEqual(updated_tokens, 15)
        self.assertEqual(BoughtItem.objects.count(), 1)
        self.assertRedirects(response, reverse('RFP:bought_items'))

    def test_buy_item_not_enough_money(self):
        item_to_purchase = Item.objects.create(name = 'Item to Purchase', price=30)

        response = self.client.post(reverse('RFP:buy_item', args = [item_to_purchase.id]))

        updated_tokens = Profile.objects.get(user = self.user).tokens

        self.assertEqual(updated_tokens, 20)
        self.assertEqual(BoughtItem.objects.count(), 0)
        self.assertRedirects(response, reverse('RFP:shop'))


class TestJoinGame(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username = 'testuser', email = 'test@example.com', password ='testpassword')
        self.user_profile = Profile.objects.get(user = self.user)
        self.pitch = Pitch.objects.create(name = 'Test Pitch', address ='Test Address', phone_number ='123456789')
        self.reservation = Reservation.objects.create(made_by = self.user, pitch = self.pitch)
        self.client.login(username ='testuser', password = 'testpassword')
        self.friend_user = User.objects.create_user(username = 'frienduser', email ='friend@example.com', password ='friendpassword')
        self.friend_profile = Profile.objects.get(user = self.friend_user)

    def test_join_game_valid(self):
        self.reservation.participants.add(self.user)

        code = self.reservation.reservation_code

        url = reverse('RFP:join_game') + f'?input_code = {code}'
        response = self.client.get(url)

        self.reservation.refresh_from_db()

        self.assertIn(self.user, self.reservation.participants.all())
        self.assertEqual(response.status_code, 302)

    def test_join_game_invalid_game_not_exist(self):
        invalid_code = 'invalidcode'

        url = reverse('RFP:join_game') + f'?input_code = {invalid_code}'
        response = self.client.get(url)

        self.assertNotIn(self.user, self.reservation.participants.all())
        self.assertRedirects(response, reverse('RFP:set_code'))

    def test_join_game_invalid_not_friend(self):
        self.client.login(username ='testuser', password ='testpassword')
        code = self.reservation.reservation_code

        url = reverse('RFP:join_game') + f'?input_code = {code}'
        response = self.client.get(url)

        self.assertNotIn(self.user, self.reservation.participants.all())
        self.assertRedirects(response, reverse('RFP:set_code'))


class TestSearchPitch(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username = 'testuser', email = 'test@example.com', password = 'testpassword')
        self.client.login(username = 'testuser', password = 'testpassword')
        self.pitch1 = Pitch.objects.create(name = 'Pitch 1', address = 'Address 1', phone_number = '123456789')
        self.pitch2 = Pitch.objects.create(name = 'Pitch 2', address = 'Address 2', phone_number = '987654321')

    def test_search_pitch_valid(self):
        url = reverse('RFP:search_pitch') + '?input_pitch=Pitch 1'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Pitch 1')
        self.assertNotContains(response, 'Pitch 2')

    def test_search_pitch_invalid(self):
        url = reverse('RFP:search_pitch') + '?input_pitch = NoExistingPitch'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This pitch does not exist!")

    def test_search_pitch_no_input(self):
        url = reverse('RFP:search_pitch')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Pitch 1')
        self.assertContains(response, 'Pitch 2')


class TestSearchItem(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username = 'testuser', email = 'test@example.com', password = 'testpassword')
        self.client.login(username ='testuser', password = 'testpassword')
        self.item1 = Item.objects.create(name = 'Item 1', price = 10)
        self.item2 = Item.objects.create(name = 'Item 2', price = 20)

    def test_search_item_valid(self):
        url = reverse('RFP:search_items') + '?input_item=Item 1'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Item 1')
        self.assertNotContains(response, 'Item 2')
        self.assertNotContains(response, "This item does not exist!")

    def test_search_item_invalid(self):
        url = reverse('RFP:search_items') + '?input_item = NoExistingItem'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This item does not exist!")

    def test_search_item_no_input(self):
        url = reverse('RFP:search_items')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Item 1')
        self.assertContains(response, 'Item 2')


class TestSearchBoughtItem(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username = 'testuser', email = 'test@example.com', password = 'testpassword')
        self.client.login(username = 'testuser', password = 'testpassword')
        self.item1 = Item.objects.create(name = 'Item 1', price = 10)
        self.item2 = Item.objects.create(name = 'Item 2', price = 20)
        self.bought_item1 = BoughtItem.objects.create(item_name = self.item1, item_code = generate_random_code(),bought_from = self.user)
        self.bought_item2 = BoughtItem.objects.create(item_name = self.item2, item_code = generate_random_code(),bought_from = self.user)

    def test_search_item_valid(self):
        url = reverse('RFP:search_bought_items') + '?input_item=Item 1'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Item 1')
        self.assertNotContains(response, 'Item 2')
        self.assertNotContains(response, "This item does not exist!")

    def test_search_item_invalid(self):
        url = reverse('RFP:search_bought_items') + '?input_item = NoExistingItem'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This item does not exist!")

    def test_search_item_no_input(self):
        url = reverse('RFP:search_bought_items')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Item 1')
        self.assertContains(response, 'Item 2')