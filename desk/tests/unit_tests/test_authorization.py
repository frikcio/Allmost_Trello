from django.test import TestCase

from desk.models import TrelloUser


class TestLogin(TestCase):
    def setUp(self):
        self.user = TrelloUser.objects.create_user(username="frikcio", password="0000")
        self.response = self.client.post('/login/', data={'username': 'frikcio',
                                                          'password': '0000'})

    def test_success_url(self):
        self.assertRedirects(response=self.response, expected_url=f'/profile/{self.user.pk}/')
