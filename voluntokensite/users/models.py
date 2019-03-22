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
    profile_pic   = models.ImageField(upload_to=get_image_path, blank=True, null=True)
 
    first_name = models.CharField(max_length = 40)
    last_name  = models.CharField(max_length = 40)
    user_type  = models.CharField(max_length=2, default='VO')
    is_public  = models.BooleanField(default = True)
    is_active  = models.BooleanField(default = True)
    
    #Volunteer Specific
    volunteer_token       = models.FloatField(default=0.0)
    volunteer_role        = models.CharField(max_length=2, null=True, default='DI')
    volunteer_hour        = models.FloatField(default=0.0)

    #Parent References
    parent_business = models.ForeignKey('BUSINESS.business', on_delete=models.CASCADE, null=True, blank=True)
    parent_ngo      = models.ForeignKey('NGO.org', on_delete=models.CASCADE, null=True, blank=True)
     


    #Keeping 
    def __str__(self):
        return self.username
#----------------------------------------------------------------------------------------------------------------------------------------------------

#Keeps track of how many hours a user has volunteered at an NGO
#----------------------------------------------------------------------------------------------------------------------------------------------------
class total_hours_stub(models.Model):
    parent_volunteer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    parent_ngo       = models.ForeignKey('NGO.org', on_delete=models.CASCADE)
    total_hours      = models.FloatField(default=0.0)
#----------------------------------------------------------------------------------------------------------------------------------------------------