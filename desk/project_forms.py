from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext as _

from desk.models import TrelloUser, BoardModel, TaskModel


class RegisterForm(UserCreationForm):
    class Meta:
        model = TrelloUser
        fields = ["username"]


class NewProjectForm(ModelForm):
    class Meta:
        model = BoardModel
        fields = ['project_name', 'users_access_list']


class NewCardForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('owner')
        super(NewCardForm, self).__init__(*args, **kwargs)
        self.fields['perfomer'].queryset = TrelloUser.objects.filter(username=self.owner.username)

    class Meta:
        model = TaskModel
        fields = ['title', 'text', 'perfomer']


class ChangeStatusForm(ModelForm):
    class Meta:
        model = TaskModel
        fields = []


class ChangePerfomerForm(ModelForm):
    def __init__(self, owner=None, *args, **kwargs):
        super(ChangePerfomerForm, self).__init__(*args, **kwargs)
        if owner:
            if not owner.is_superuser:
                self.fields['perfomer'].queryset = TrelloUser.objects.filter(username=owner)
            else:
                self.fields['perfomer'].queryset = TrelloUser.objects.exclude(username=owner)

    class Meta:
        model = TaskModel
        fields = ['perfomer']
