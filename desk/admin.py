from django.contrib import admin
from .models import TaskModel, TrelloUser

# Register your models here.

admin.site.register(TaskModel)
admin.site.register(TrelloUser)