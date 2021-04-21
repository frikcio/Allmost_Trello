from django.contrib.auth.forms import UserCreationForm

from desk.models import TrelloUser


class RegisterForm(UserCreationForm):
    class Meta:
        model = TrelloUser
        fields = ["username"]
