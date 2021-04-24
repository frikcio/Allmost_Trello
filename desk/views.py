from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import *

from desk.models import TrelloUser, BoardModel, TaskModel
from desk.my_mixins import AdminRequiredMixin
from desk.project_forms import *


class Register(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = '/login/'


class Login(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return f'/profile/{self.request.user.id}/'


class Logout(LoginRequiredMixin, LogoutView):
    login_url = '/login/'
    next_page = '/login/'


class ProfileView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = TrelloUser
    template_name = 'profile.html'


class AddNewProjectView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    form_class = NewProjectForm
    http_method_names = ['post']

    def form_valid(self, form):
        project = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return "/"


class ProjectsListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    paginate_by = 10
    template_name = 'projects.html'
    queryset = BoardModel.objects.all()
    extra_context = {"form": NewProjectForm}


class CreateCardView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    template_name = 'create_card.html'
    form_class = NewCardForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['owner'] = self.request.user
        return kwargs

    def form_valid(self, form):
        card = form.save(commit=False)
        card.owner = self.request.user
        card.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return "/"


class HomeView(LoginRequiredMixin, ListView):
    queryset = TaskModel.objects.all()
    login_url = '/login/'
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data()
        form = ChangePerfomerForm(self.request.user)
        kwargs['perfomer_form'] = form
        return kwargs


class RiseStatusView(LoginRequiredMixin, UpdateView):
    http_method_names = ['post']
    login_url = "/login/"
    form_class = ChangeStatusForm

    def get_object(self, queryset=None):
        return TaskModel.objects.get(pk=self.kwargs['pk'])

    def form_valid(self, form):
        card = form.save(commit=False)
        if not self.request.user.is_superuser and self.request.user == card.perfomer:
            if card.status < 4:
                card.status += 1
        else:
            if card.status < 5:
                card.status += 1
        card.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return "/"


class OmitStatusView(LoginRequiredMixin, UpdateView):
    http_method_names = ['post']
    login_url = "/login/"
    form_class = ChangeStatusForm

    def get_object(self, queryset=None):
        return TaskModel.objects.get(pk=self.kwargs['pk'])

    def form_valid(self, form):
        card = form.save(commit=False)
        if not self.request.user.is_superuser and self.request.user == card.perfomer:
            if 4 >= card.status > 2:
                card.status -= 1
        else:
            if card.status > 3:
                card.status -= 1
        card.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return "/"


class DeleteCardView(LoginRequiredMixin, DeleteView):
    model = TaskModel
    success_url = "/"


class ChangePerfomerView(LoginRequiredMixin, UpdateView):
    http_method_names = ['post']
    login_url = '/login/'
    form_class = ChangePerfomerForm

    def get_object(self, queryset=None):
        return TaskModel.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        return "/"
