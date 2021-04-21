from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, TemplateView

from desk.models import TrelloUser, BoardModel
from desk.project_forms import RegisterForm


class HomeView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'index.html'


class Register(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = '/login/'


class Login(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return f'/profile/{self.request.user.id}/'


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/login/'
    login_url = '/login/'


class ProfileView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    pk_url_kwarg = 'pk'
    model = TrelloUser
    template_name = 'profile.html'