from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, AbstractUser

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=1000)
    is_completed = models.BooleanField(default=False)
    is_archieved = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Liên kết với tài khoản

    def __str__(self):
        return self.title
    
    def clean(self):
        if self.is_archieved and self.is_deleted:
            raise ValidationError('Only one of the two checkboxes can be checked (is_archieved or is_deleted).')
        return super().clean()



