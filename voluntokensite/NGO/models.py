from django.db import models
from users.models import CustomUser
import os


def get_image_path(instance, filename):
	return os.path.join('photos', str(instance.id), filename)

class orgs(models.Model):
	name        = models.CharField(max_length = 50)
	description = models.CharField(max_length = 2500)
	email       = models.EmailField(max_length = 200)
	address     = models.CharField(max_length = 500)
	#picture     = models.ImageField(upload_to=get_image_path, blank=True, null=True)

	def __str__(self):
		return self.name

class events(models.Model):
	parent_orgs = models.ForeignKey(orgs, on_delete=models.CASCADE)
	
	name        = models.CharField(max_length = 200)
	description = models.CharField(max_length = 2500)
	#picture     = models.ImageField(upload_to=get_image_path, blank=True, null=True)
	start_time  = models.DateTimeField()
	end_time    = models.DateTimeField()
	

	# #NEEDS TESTING -------------------------------------------------
	# #Check ifstop_time - start_time is positive
	# if (end_time - start_time).hours <= 0:
	# 	raise forms.ValidationError("The end time of your event must be after the start time!")

	# #---------------------------------------------------------------

	QR_code     = models.ImageField(upload_to=get_image_path, blank=True, null=True)
	active      = models.BooleanField(default=True)

	def __str__(self):
		return self.name

class checks_stub(models.Model):
	check_in_or_out  = models.BooleanField(default = True) #True: Check IN, False: Check OUT
	time             = models.DateTimeField()
	parent_event     = models.ForeignKey(events, on_delete=models.CASCADE)
	parent_volunteer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

	# def __str__(self):
	# 	return __str__(self.time)

class event_registration_stub(models.Model):
	active           = models.BooleanField(default=True)
	parent_event     = models.ForeignKey(events, on_delete=models.CASCADE)
	parent_volunteer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

	# def __str__(self):
	# 	return __str__(self.parent_event)