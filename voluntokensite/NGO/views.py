# users/views.py
from django.urls import reverse_lazy
from django.views import generic
from BUSINESS.models import business, total_support_stub, EXCHANGE_USD_TOKEN
from users.models import CustomUser, total_hours_stub
from .models import event, event_registration_stub, event_hours_spent_stub
from .forms import eventCreationForm, eventChangeForm

from django.views import View
from django.shortcuts import render, redirect

from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse


#VIEW STATS
#----------------------------------------------------------------------------------------------------------------------------------------------------
class View_Stats(View):
	template_name = 'ngo_stats.html'

	def get(self, request, *args, **kwargs):
		if(request.user.user_type != 'NG'):
			return HttpResponseNotFound('<h1>Page not found</h1>')

		ngo_instance = request.user.parent_ngo

		#Table of NGOs Supported: ngos_supported
		event_set    = event.objects.filter(parent_ngo=ngo_instance)
		events_hosted = []

		for event_instance in event_set:
			event_info = {}

			event_info['name']    = event_instance.name
			event_info['id']      = event_instance.id
			event_info['is_active'] = event_instance.is_active
			event_info['hours']   = event_instance.volunteer_hour
			registered_users_set  = event_registration_stub.objects.filter(parent_event=event_instance)
			event_info['number_registered'] = registered_users_set.count()
			participant_users_set = event_hours_spent_stub.objects.filter(parent_event=event_instance)
			event_info['number_participants'] = participant_users_set.count()

			events_hosted.append(event_info)



		#Table of Supporting Businesses
		total_support_stub_set  = total_support_stub.objects.filter(parent_ngo=ngo_instance)
		business_support = []

		for stub in total_support_stub_set:
			business_info = {}
			business_info['name']      = stub.parent_business.name
			business_info['hours']     = stub.total_hours
			business_info['donations'] = stub.total_donation_tokens*EXCHANGE_USD_TOKEN
			business_info['discounts'] = stub.total_discount_tokens
			business_info['website']   = stub.parent_business.website

			business_support.append(business_info)


		#Table of Volunteers
		total_hours_stub_set    = total_hours_stub.objects.filter(parent_ngo=ngo_instance)
		volunteer_support = []

		for stub in total_hours_stub_set:
			volunteer_info = {}
			volunteer_info['name']  = stub.parent_volunteer.first_name + " " + stub.parent_volunteer.last_name
			volunteer_info['email'] = stub.parent_volunteer.email
			volunteer_info['hours'] = stub.total_hours
			volunteer_info['donations'] = stub.total_donation_tokens*EXCHANGE_USD_TOKEN

			volunteer_support.append(volunteer_info)

		#Totals
		total = {}
		total['hours']      = ngo_instance.volunteer_hour
		total['volunteers'] = total_hours_stub_set.count()
		total['donations']  = ngo_instance.total_donation_tokens*EXCHANGE_USD_TOKEN


		return render(request, self.template_name, {'title':"NGO Stats", "events_hosted": events_hosted, "business_support": business_support, "volunteer_support":volunteer_support, "total": total})


#----------------------------------------------------------------------------------------------------------------------------------------------------

#COUPONS
#----------------------------------------------------------------------------------------------------------------------------------------------------
#delete event
def delete_event(request,event_id =None, end_route='see_events'):
	try:
		event_obj = event.objects.get(id=event_id)
	except event.DoesNotExist:
		return HttpResponseNotFound('<h1>Event Does Not Exist</h1>')
	
	if (event_obj.parent_ngo != request.user.parent_ngo):
			return HttpResponse('<h1> Access Denied </h1>', status=403)
	
	event_obj.delete()
	return HttpResponseRedirect(reverse(end_route))

def deactivate_event(request,event_id =None, end_route='see_events'):
	try:
		event_obj = event.objects.get(id=event_id)
	except event.DoesNotExist:
		return HttpResponseNotFound('<h1>Event Does Not Exist</h1>')
	
	if (event_obj.parent_ngo != request.user.parent_ngo):
			return HttpResponse('<h1> Access Denied </h1>', status=403)
	
	event_obj.is_active = False
	event_obj.save()
	return HttpResponseRedirect(reverse(end_route))

def activate_event(request,event_id =None, end_route='see_events'):
	try:
		event_obj = event.objects.get(id=event_id)
	except event.DoesNotExist:
		return HttpResponseNotFound('<h1>Event Does Not Exist</h1>')
	
	if (event_obj.parent_ngo != request.user.parent_ngo):
			return HttpResponse('<h1> Access Denied </h1>', status=403)

	event_obj.is_active = True
	event_obj.save()
	return HttpResponseRedirect(reverse(end_route))


#display events
class Show_Events(View):
	template_name = 'event_view.html'
	
	def get(self, request, *args, **kwargs):
		if(request.user.user_type != 'NG'):
			return HttpResponseNotFound('<h1>Page not found</h1>')
		user_ngo = request.user.parent_ngo		
		event_list = event.objects.filter(parent_ngo=user_ngo)
		return render(request, self.template_name, {'title':"Events","events":event_list})
			


class Create_Event(View):
	form_class = eventCreationForm
	success_url = 'see_events'
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
		if(request.user.user_type != 'NG'):
			return HttpResponseNotFound('<h1>Page not found</h1>')
		user_ngo_id = request.user.parent_ngo
		form = self.form_class(request.POST, parent_ngo_name=user_ngo_id)
		if form.is_valid():
			form.save()
			# <process form cleaned data>
			return redirect(self.success_url)

		return render(request, self.template_name, {'form': form, 'title':"Event Creation",'submit_text':"create"})
#----------------------------------------------------------------------------------------------------------------------------------------------------

class Change_Event(View):
	form_class = eventChangeForm
	success_url = 'see_events'
	template_name = 'form.html'
	
	def get(self, request, *args, **kwargs):
		if(request.user.user_type != 'NG'):
			return HttpResponseNotFound('<h1>Page not found</h1>')
		try:
			event_obj = event.objects.get(id=self.kwargs['event_id'])
		except event.DoesNotExist:
			return HttpResponseNotFound('<h1>Event Does Not Exist</h1>')

		if (event_obj.parent_ngo != request.user.parent_ngo):
			return HttpResponse('<h1> Access Denied </h1>', status=403)

		form = self.form_class(instance=event_obj)	
		return render(request, self.template_name, {'form': form, 'title':"Event Modification",'submit_text':"save"})

	def post(self, request, *args, **kwargs):
		try:
			event_obj = event.objects.get(id=self.kwargs['event_id'])
		except event.DoesNotExist:
			return HttpResponseNotFound('<h1>Event Does Not Exist</h1>')

		if (event_obj.parent_ngo != request.user.parent_ngo):
			return HttpResponse('<h1> Access Denied </h1>', status=403)

		form = self.form_class(request.POST, instance=event_obj)			
		if form.is_valid():
			form.save()
			return redirect(self.success_url)

		return render(request, self.template_name, {'form': form})


