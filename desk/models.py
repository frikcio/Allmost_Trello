from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

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
    perfomer = models.ForeignKey(TrelloUser, on_delete=models.DO_NOTHING, related_name='development')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class BoardModel(models.Model):
    project = models.TextField(max_length=100)
    tasks = models.ManyToManyField(TaskModel, related_name="project_name")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
