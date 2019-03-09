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

    #USERTYPES
    volunteer_user_abreviation = 'VO'
    ngo_user_abreviation       = 'NG'
    business_user_abreviation  = 'BU'

    user_type_choices  = {
    			(volunteer_user_abreviation, 'Volunteer User'),
    			(ngo_user_abreviation, 'NGO User'),
    			(business_user_abreviation, 'Business User')
    }
    user_type  = models.CharField(max_length=2, choices=user_type_choices, default=volunteer_user_abreviation)
    

    #refence to NGO, Business, Volunteer 
    #reference_id = 
    def __str__(self):
        return self.email