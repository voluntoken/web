# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
import os

# Image Stuff
def get_image_path(instance, filename):
	return os.path.join('photos', str(instance.id), filename)


#CustomUser Class - Volunteer, NGO, Business Users
#----------------------------------------------------------------------------------------------------------------------------------------------------
class CustomUser(AbstractUser):
    #Personal INFO
    #picture    = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    first_name = models.CharField(max_length = 40)
    last_name  = models.CharField(max_length = 40)
    user_type  = models.CharField(max_length=2)
    is_public  = models.BooleanField(default = True)
    is_active  = models.BooleanField(default = True)
    
    #Volunteer Specific
    volunteer_token       = models.FloatField(null=True)
    volunteer_role        = models.CharField(max_length=2, null=True, default='VO')
    volunteer_hour        = models.FloatField(null=True)

    #Parent References
    parent_business = models.ForeignKey('BUSINESS.business', on_delete=models.CASCADE, null=True)
    parent_ngo      = models.ForeignKey('NGO.org', on_delete=models.CASCADE, null=True)
     
    def __str__(self):
        return self.email
#----------------------------------------------------------------------------------------------------------------------------------------------------