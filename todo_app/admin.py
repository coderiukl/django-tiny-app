from django.contrib import admin
from .models import Task
from .forms import TaskForm

# Register your models here.
admin.site.register(Task)