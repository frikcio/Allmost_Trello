from django.test import TestCase

from desk.models import TrelloUser
from desk.views import Login


class TestLogin(TestCase):
    def setUp(self):
        self.user = TrelloUser.objects.create_user(username="foxana", password="52654936abcdA")

    def test_success_url(self):
        request = self.client.post('/login/', data={'username': 'foxana',
                                                     'password': '52654936abcdA'})
        request.user = self.user
        view = Login()
        view.setup(request)
        self.assertEqual(f'/profile/{request.user.id}/', view.get_success_url())

    def test_fail_success_url(self):
        request = self.client.post('/login/', data={'username': 'foxana',
                                                    'password': '52654936abcdA'})
        request.user = self.user
        view = Login()
        view.setup(request)
        self.assertNotEqual(f'/login/', view.get_success_url())
