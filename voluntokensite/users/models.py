# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
import os


def get_image_path(instance, filename):
	return os.path.join('photos', str(instance.id), filename)
class CustomUser(AbstractUser):
    #Personal INFO
    picture    = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    first_name = models.CharField(max_length = 40)
    last_name  = models.CharField(max_length = 40)
    user_type  = models.CharField(max_length=2)
    
    volunteer_token = models.IntegerField(null=True)
    volunteer_role  = models.CharField(max_length=2)

    parent_business = models.ForeignKey('BUSINESS.businesses', on_delete=models.CASCADE, null=True)
    parent_ngo      = models.ForeignKey('NGO.orgs', on_delete=models.CASCADE, null=True)
     
    def __str__(self):
        return self.email


