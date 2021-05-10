from django.test import TestCase, RequestFactory

from desk.views import *


class TestCreateCard(TestCase):
    def setUp(self):
        self.view = CreateCardView()
        self.request = RequestFactory().post('/card/create/', data={'title': 'test_card',
                                                                    'text': 'some-text',
                                                                    'performer': ''})
        self.request.user = TrelloUser.objects.create_user(username="foxana", password="52654936abcdA")

    def test_success_url(self):
        self.view.setup(self.request)
        self.assertEqual('/', self.view.get_success_url())

    def test_owner_in_form_kwargs(self):
        self.view.setup(self.request)
        kwargs = self.view.get_form_kwargs()
        self.assertIn('owner', kwargs)

    def test_form_valid(self):
        self.view.setup(self.request)
        form = self.view.get_form()
        self.assertEquals(form.owner, self.request.user)


class TestRaiseStatus(TestCase):
    def setUp(self):
        self.user1 = TrelloUser.objects.create_user(username="foxana", password="0000")
        self.user2 = TrelloUser.objects.create_user(username="frikcio", password="0000")
        self.admin = TrelloUser.objects.create_superuser(username='admin', password='admin')
        self.card = TaskModel.objects.create(title="test", text="bla pla", performer=self.user2, owner=self.user1)
        self.request = RequestFactory().post(f"/card/status/raise/{self.card.pk}/")
        self.view = RaiseStatusView()

    def test_success_url(self):
        self.view.setup(self.request)
        self.assertEqual('/', self.view.get_success_url())

    def test_form_valid(self):
        self.view.setup(self.request, pk=self.card.pk)
        starting_status = self.view.get_object().status
        self.view.post(self.request)
        finish_status = self.view.get_object().status
        self.assertNotEquals(starting_status, finish_status)
