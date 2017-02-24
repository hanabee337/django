from django.contrib.auth.models import AbstractUser


# Create your models here.
from django.db import models


class MyUser(AbstractUser):
    img_profile = models.ImageField(upload_to='user')

    def __str__(self):
        return '{} {}'.format(
            self.last_name,
            self.first_name
        )