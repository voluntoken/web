from django.contrib.auth.models import AbstractUser
from django.db import models

class VolunteerUser(AbstractUser):
    # add additional fields in here

    def __str__(self):
        return self.email