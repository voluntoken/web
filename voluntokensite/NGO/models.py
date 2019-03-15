from django.db import models
from users.models import CustomUser
from datetime import datetime
from random import randint
from django import forms
import os


def get_image_path(instance, filename):
	return os.path.join('photos', str(instance.id), filename)

#org class - 
#----------------------------------------------------------------------------------------------------------------------------------------------------
class org(models.Model):
	#Profile Info
	name        = models.CharField(max_length = 50)
	description = models.CharField(max_length = 2500)
	email       = models.EmailField(max_length = 200)
	address     = models.CharField(max_length = 500)
	is_active   = models.BooleanField(default=True)
	volunteer_hour = models.FloatField(default=0.0)
	#picture     = models.ImageField(upload_to=get_image_path, blank=True, null=True)

	def __str__(self):
		return self.name
#----------------------------------------------------------------------------------------------------------------------------------------------------

#event class
#----------------------------------------------------------------------------------------------------------------------------------------------------
class event(models.Model):
	#Profile Info
	name         = models.CharField(max_length = 200)
	description  = models.CharField(max_length = 2500)
	#picture     = models.ImageField(upload_to=get_image_path, blank=True, null=True)
	parent_ngo   = models.ForeignKey(org, on_delete=models.CASCADE)
	qr_code      = models.ImageField(upload_to=get_image_path, blank=True, null=True)
	pin_checkin  = models.IntegerField(default=randint(1000,9999))
	pin_checkout = models.IntegerField(default=randint(1000,9999))
	is_active    = models.BooleanField(default=True)

	#Timing
	start_time   = models.DateTimeField(default=datetime.utcnow)
	end_time     = models.DateTimeField(default=datetime.utcnow)


	#NEEDS TESTING -------------------------------------------------
	#Check ifstop_time - start_time is positive
	if  start_time >= end_time:
		raise forms.ValidationError("The end time of your event must be after the start time!")

	#---------------------------------------------------------------

	def __str__(self):
		return self.name
#----------------------------------------------------------------------------------------------------------------------------------------------------

#checks_stub class - check in, check out stub
#----------------------------------------------------------------------------------------------------------------------------------------------------
class checks_stub(models.Model):
	is_check_in      = models.BooleanField(default = True) #True: Check IN, False: Check OUT
	time             = models.DateTimeField(default=datetime.utcnow)
	parent_event     = models.ForeignKey(event, on_delete=models.CASCADE)
	parent_volunteer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	
	# def __str__(self):
	# 	return __str__(self.time)
#----------------------------------------------------------------------------------------------------------------------------------------------------

#event registrsation is different from checking in or out
#----------------------------------------------------------------------------------------------------------------------------------------------------
class event_registration_stub(models.Model):
	parent_event     = models.ForeignKey(event, on_delete=models.CASCADE)
	parent_volunteer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#----------------------------------------------------------------------------------------------------------------------------------------------------
	# def __str__(self):
	# 	return __str__(self.parent_event)


#event_hours_spent_stub stores hours user volunteered at event
#----------------------------------------------------------------------------------------------------------------------------------------------------
class event_hours_spent_stub(models.Model):
	parent_event     = models.ForeignKey(event, on_delete=models.CASCADE)
	parent_volunteer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	hours            = models.FloatField(default=0.0)
#----------------------------------------------------------------------------------------------------------------------------------------------------