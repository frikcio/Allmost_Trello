from django.test import TestCase, RequestFactory

from desk.views import *


class TestCreateCard(TestCase):
    def setUp(self):
        self.user1 = TrelloUser.objects.create_user(username="frikcio", password="0000")
        self.user2 = TrelloUser.objects.create_user(username="foxana", password="0000")
        self.data = {'title': 'test_card', 'text': 'some-text', 'performer': f"{self.user1.pk}"}
        self.request = RequestFactory().post('/card/create/', data=self.data)
        self.request.user = self.user1
        self.view = CreateCardView()

    def test_success_url(self):
        self.client.force_login(self.user1)
        response = self.client.post('/card/create/', data=self.data)
        self.assertRedirects(response=response, expected_url='/', status_code=302)

    def test_owner_in_form_kwargs(self):
        self.view.setup(self.request)
        kwargs = self.view.get_form_kwargs()
        self.assertIn('owner', kwargs)

    def test_owner_is_user_(self):
        self.view.setup(self.request)
        self.view.form_valid(self.view.get_form())
        card = TaskModel.objects.get(title=self.data['title'])
        self.assertEquals(card.owner, self.request.user)

    def test_performer_is_owner(self):
        self.view.setup(self.request)
        self.view.form_valid(self.view.get_form())
        card = TaskModel.objects.get(title=self.data['title'])
        self.assertEquals(card.performer, self.request.user)


class TestChangeStatus(TestCase):
    def setUp(self):
        self.user1 = TrelloUser.objects.create_user(username="foxana", password="0000")
        self.user2 = TrelloUser.objects.create_user(username="frikcio", password="0000")
        self.admin = TrelloUser.objects.create_superuser(username='admin', password='admin')
        self.card = TaskModel.objects.create(title="test", text="bla pla", performer=self.user2, owner=self.user1,
                                             status=3)
        self.request1 = RequestFactory().post(f"/card/status/raise/{self.card.pk}/")
        self.request1.user = self.user2
        self.request2 = RequestFactory().post(f"/card/status/omit/{self.card.pk}/")
        self.view = RaiseStatusView()

    def test_success_url(self):     # Test if all are good, all are work)
        self.client.force_login(self.user2)
        response = self.client.post(f"/card/status/raise/{self.card.pk}/")
        self.assertRedirects(response=response, expected_url='/', status_code=302)
        response = self.client.post(f"/card/status/omit/{self.card.pk}/")
        self.assertRedirects(response=response, expected_url='/', status_code=302)

    def test_user_is_performer(self):   # Test if request.user is performer or admin, status will changed
        self.client.force_login(self.user2)
        begin_status = TaskModel.objects.get(pk=self.card.pk).status
        self.client.post(f"/card/status/raise/{self.card.pk}/")     # status increase by 1
        finish_status = TaskModel.objects.get(pk=self.card.pk).status
        self.assertNotEquals(begin_status, finish_status)
        self.client.post(f"/card/status/omit/{self.card.pk}/")      # status decrease by 1
        another_finish_status = TaskModel.objects.get(pk=self.card.pk).status
        self.assertEquals(begin_status, another_finish_status)

    def test_user_is_not_performer(self):   # Test if request.user is not performer or admin, status will not changed
        self.client.force_login(self.user1)
        begin_status = self.card.status
        self.client.post(f"/card/status/raise/{self.card.pk}/")
        finish_status = self.card.status
        self.assertEqual(begin_status, finish_status)
        self.client.post(f"/card/status/omit/{self.card.pk}/")
        finish_status = self.card.status
        self.assertEqual(begin_status, finish_status)

