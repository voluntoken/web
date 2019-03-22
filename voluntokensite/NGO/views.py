# users/views.py
from django.urls import reverse_lazy
from django.views import generic
from .models import event
from .forms import eventCreationForm, eventChangeForm

from django.views import View
from django.shortcuts import render, redirect

from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse

#COUPONS
#----------------------------------------------------------------------------------------------------------------------------------------------------

#delete event
def delete_event(request,event_id =None):
	event_obj = event.objects.get(id=event_id)
	event_obj.delete()
	return HttpResponseRedirect(reverse('see_events'))
	
#display events
class Show_Events(View):
	template_name = 'event_view.html'
	
	def get(self, request, *args, **kwargs):
		if(request.user.user_type != 'NG'):
			return HttpResponseNotFound('<h1>Page not found</h1>')
		user_ngo_id = request.user.parent_ngo		
		event_list = event.objects.filter(parent_ngo=user_ngo_id)
		print(event_list)
		return render(request, self.template_name, {'title':"Events","events":event_list})
			


class Create_Event(View):
	form_class = eventCreationForm
	success_url = reverse_lazy('')
	template_name = 'form.html'
	
	def get(self, request, *args, **kwargs):
		if(request.user.user_type != 'NG'):
			return HttpResponseNotFound('<h1>Page not found</h1>')
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

class Change_Event(View):
	form_class = eventChangeForm
	success_url = reverse_lazy('')
	template_name = 'form.html'
	
	def get(self, request, *args, **kwargs):
		if(request.user.user_type != 'NG'):
			return HttpResponseNotFound('<h1>Page not found</h1>')
		event_obj = event.objects.get(id=self.kwargs['event_id'])
		form = self.form_class(instance=event_obj)	
		return render(request, self.template_name, {'form': form, 'title':"Event Modification",'submit_text':"save"})

	def post(self, request, *args, **kwargs):
		
		event_obj = event.objects.get(id=self.kwargs['event_id'])
		form = self.form_class(request.POST, instance=event_obj)			
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('see_events'))

		return render(request, self.template_name, {'form': form})


