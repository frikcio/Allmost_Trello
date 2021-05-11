from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.views.generic import *

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
    form_class = CreateCardForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['owner'] = self.request.user
        return kwargs

    def form_valid(self, form):
        card = form.save(commit=False)
        if not card.performer or card.performer == self.request.user or self.request.user.is_superuser:
            card.owner = self.request.user
            card.save()
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return "/"


class HomeView(LoginRequiredMixin, ListView):
    queryset = TaskModel.objects.all()
    login_url = '/login/'
    template_name = 'index.html'


class RaiseStatusView(LoginRequiredMixin, UpdateView):
    http_method_names = ['post']
    login_url = "/login/"
    form_class = ChangeStatusForm
    queryset = TaskModel.objects.all()

    def form_valid(self, form):
        card = form.save(commit=False)
        if self.request.user == card.performer:
            if card.status < 4:
                card.status += 1
        elif self.request.user.is_superuser:
            if 3 < card.status < 5:
                card.status += 1
        card.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return "/"


class OmitStatusView(LoginRequiredMixin, UpdateView):
    http_method_names = ['post']
    login_url = "/login/"
    form_class = ChangeStatusForm
    queryset = TaskModel.objects.all()

    def form_valid(self, form):
        card = form.save(commit=False)
        if self.request.user == card.performer:
            if 4 >= card.status > 2:
                card.status -= 1
        elif self.request.user.is_superuser:
            if card.status > 4:
                card.status -= 1
        card.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return "/"


class DeleteCardView(LoginRequiredMixin, DeleteView):
    model = TaskModel
    success_url = "/"


class ChangeTextView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    form_class = ChangeTextForm
    template_name = 'change_text.html'
    success_url = '/'
    queryset = TaskModel.objects.all()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['owner'] = self.request.user
        return kwargs

    def form_valid(self, form):
        card = self.get_object()
        if self.request.user != card.owner or not self.request.user.is_superuser:
            HttpResponseRedirect('/')
        else:
            if (not self.object.performer and card.performer != card.owner) and not self.request.user.is_superuser:
                card = form.save(commit=False)
                card.performer = self.get_object().performer
                card.save()
            return super().form_valid(form=form)
