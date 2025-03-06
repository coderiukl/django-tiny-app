from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, AbstractUser, Group, Permission

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


class CustomUser(AbstractUser):
    is_blocked = models.BooleanField(default=False)
    
    # Use different related_name for the reverse relationship to avoid conflicts
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Change the related_name
        blank=True,
        help_text="The groups this user belongs to."
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",  # Change the related_name
        blank=True,
        help_text="Specific permissions for this user."
    )

    def __str__(self):
        return self.username



