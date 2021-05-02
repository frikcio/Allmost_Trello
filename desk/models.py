from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework.authtoken.models import Token

STATUS_CHOICES = (
    (1, _("New")),
    (2, _("In progress")),
    (3, _("In QA")),
    (4, _("Ready")),
    (5, _("Done")),
)


class TrelloUser(AbstractUser):
    avatar = models.ImageField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.username

    @property
    def age(self):
        return (timezone.now() - self.birth_date).year

    @property
    def total(self):
        return (timezone.now() - self.date_joined).days


class TaskModel(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    screenshot = models.ImageField(blank=True, null=True)
    owner = models.ForeignKey(TrelloUser, on_delete=models.DO_NOTHING, related_name='created')
    performer = models.ForeignKey(TrelloUser, on_delete=models.DO_NOTHING, related_name='development', default=None,
                                  null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class BoardModel(models.Model):
    project_name = models.CharField(max_length=100, unique=True)
    tasks = models.ManyToManyField(TaskModel, related_name="project_name")
    users_access_list = models.ManyToManyField(TrelloUser, related_name='projects_access')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class TemporaryTokenModel(Token):
    last_action = models.DateTimeField(null=True)
