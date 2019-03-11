# users/views.py
from django.urls import reverse_lazy
from django.views import generic
from .models import event
from .forms import eventCreationForm, eventChangeForm

from django.views import View
from django.shortcuts import render, redirect

#COUPONS
#----------------------------------------------------------------------------------------------------------------------------------------------------
class Create_Event(View):
	form_class = eventCreationForm
	success_url = reverse_lazy('')
	template_name = 'form.html'
	
	def get(self, request, *args, **kwargs):
		# print(request.user.username)
		# print(request.user.parent_ngo)
		user_ngo_id = request.user.parent_ngo
		form = self.form_class(parent_ngo_name=user_ngo_id)
		return render(request, self.template_name, {'form': form, 'title':"Event Creation",'submit_text':"create"})
		
	def post(self, request, *args, **kwargs):
		user_ngo_id = request.user.parent_ngo
		form = self.form_class(request.POST, parent_ngo_name=user_ngo_id)
		if form.is_valid():
			form.save()
			# <process form cleaned data>
			return render(request, 'NGO_home.html', {})

		return render(request, self.template_name, {'form': form})
#----------------------------------------------------------------------------------------------------------------------------------------------------