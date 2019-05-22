# users/views.py
from django.urls import reverse_lazy
from django.views import generic
from .models import coupon, total_support_stub, EXCHANGE_TOKEN_HOUR, user_support_stub, transaction_stub, EXCHANGE_USD_TOKEN
from .forms import couponDiscountCreationForm, couponDiscountChangeForm, couponDonationCreationForm, couponDonationChangeForm

from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404, HttpResponseNotFound
from django.urls import reverse
import numpy as np



#VIEW STATS
#----------------------------------------------------------------------------------------------------------------------------------------------------
class View_Stats(View):
	template_name = 'business_stats.html'

	def get(self, request, *args, **kwargs):
		if(request.user.user_type != 'BU'):
			return HttpResponseNotFound('<h1>Page not found</h1>')

		business_instance = request.user.parent_business

		#Table of NGOs Supported: ngos_supported
		total_support_stub_set = total_support_stub.objects.filter(parent_business=business_instance)
		ngos_supported = []#array of dicts - ngo_support_info

		for total_support_stub_instance in total_support_stub_set:
			ngo_support_info = {}
			ngo_instance = total_support_stub_instance.parent_ngo
			ngo_support_info['name']                = ngo_instance.name
			ngo_support_info['website']             = ngo_instance.website
			ngo_support_info['hours']               = total_support_stub_instance.total_hours
			ngo_support_info['donations']           = total_support_stub_instance.total_donation_tokens*1.0/(EXCHANGE_TOKEN_HOUR)
			ngo_support_info['discounts']           = total_support_stub_instance.total_discount_tokens
			ngo_support_info['number_customers']    = (user_support_stub.objects.filter(parent_business=business_instance, parent_ngo=ngo_instance)).count()
			ngo_support_info['number_transactions'] = total_support_stub_instance.total_transactions
			ngo_support_info['total_profit']        = total_support_stub_instance.total_profit

			ngos_supported.append(ngo_support_info)

		#Table of Donation Coupon STATS	
		donation_coupons = []
		donation_coupon_set = coupon.objects.filter(parent_business=business_instance, is_donation=True)

		for coupon_instance in donation_coupon_set:
			coupon_info = {}
			coupon_info['name']      = coupon_instance.name
			coupon_info['id']        = coupon_instance.id
			coupon_info['is_active'] = coupon_instance.is_active
			#all the transactions using this coupon that are donations, a bit of a redundant filter
			transaction_set                 = transaction_stub.objects.filter(parent_business=business_instance, coupon_used=coupon_instance, is_donation=True)
			customer_ids                    = np.unique(np.array([x.parent_volunteer.id for x in transaction_set]))
			num_customer_ids                = len(customer_ids)

			number_of_transactions          = transaction_set.count()
			coupon_info['donations']        = coupon_instance.donation_val*number_of_transactions
			coupon_info['hours']            = coupon_instance.token_cost*1.0/(EXCHANGE_TOKEN_HOUR)*number_of_transactions
			coupon_info['times_used']       = number_of_transactions
			coupon_info['number_customers'] = num_customer_ids
			if(num_customer_ids == 0):
				coupon_info['customer_average_use'] = 0
			else:
				coupon_info['customer_average_use'] = number_of_transactions/num_customer_ids
			coupon_info['total_profit']             = coupon_instance.item_cost*number_of_transactions

			donation_coupons.append(coupon_info)


		#Table of Discount Coupon STATS
		discount_coupons = []
		discount_coupon_set = coupon.objects.filter(parent_business=business_instance, is_donation=False)

		for coupon_instance in discount_coupon_set:
			coupon_info = {}
			coupon_info['name']      = coupon_instance.name
			coupon_info['id']        = coupon_instance.id
			coupon_info['is_active'] = coupon_instance.is_active
			
			#all the transactions using this coupon that are donations, a bit of a redundant filter
			transaction_set                 = transaction_stub.objects.filter(parent_business=business_instance, coupon_used=coupon_instance, is_donation=False)
			customer_ids                    = np.unique(np.array([x.parent_volunteer.id for x in transaction_set]))
			num_customer_ids                = len(customer_ids)

			number_of_transactions          = transaction_set.count()
			coupon_info['discounts']        = coupon_instance.token_cost*number_of_transactions
			coupon_info['hours']            = coupon_instance.token_cost*1.0/(EXCHANGE_TOKEN_HOUR)*number_of_transactions
			coupon_info['times_used']       = number_of_transactions
			coupon_info['number_customers'] = num_customer_ids
			if(num_customer_ids == 0):
				coupon_info['customer_average_use'] = 0
			else:
				coupon_info['customer_average_use'] = number_of_transactions/num_customer_ids
			coupon_info['total_profit']             = coupon_instance.item_cost*number_of_transactions

			discount_coupons.append(coupon_info)

		#Table Total Stats
		total = {}
		total['hours']  = business_instance.total_hours
		transaction_set  = transaction_stub.objects.filter(parent_business=business_instance)
		num_customer_ids = len(np.unique(np.array([x.parent_volunteer.id for x in transaction_set])))
		num_coupon_ids   = len(transaction_set)
		total['number_customers'] = num_customer_ids
		total['total_profit']     = business_instance.total_profit
		total['transactions']     = num_coupon_ids
		total['donations']        = business_instance.donation_tokens*EXCHANGE_USD_TOKEN
		total['discounts']        = business_instance.discount_tokens

		return render(request, self.template_name, {'title':"Business Stats", "ngos_supported": ngos_supported, "donation_coupons":donation_coupons, "discount_coupons":discount_coupons, "total":total})




#----------------------------------------------------------------------------------------------------------------------------------------------------


#SHOW Coupon
#----------------------------------------------------------------------------------------------------------------------------------------------------
class Show_Coupon(View):
	template_name = 'coupon_view.html'
	
	def get(self, request, *args, **kwargs):
		if(request.user.user_type != 'BU'):
			return HttpResponseNotFound('<h1>Page not found</h1>')
		user_business    = request.user.parent_business		
		business_pin     = request.user.parent_business.pin
		coupon_list = coupon.objects.filter(parent_business=user_business)
		return render(request, self.template_name, {'title':"Coupons","coupons":coupon_list, "business_pin":business_pin})		
#----------------------------------------------------------------------------------------------------------------------------------------------------

#CREATE Coupon
#----------------------------------------------------------------------------------------------------------------------------------------------------
class Create_Coupon_Discount(View):
	form_class = couponDiscountCreationForm
	success_url = 'see_coupons'
	template_name = 'form.html'
	
	def get(self, request, *args, **kwargs):
		if(request.user.user_type != 'BU'):
			return HttpResponseNotFound('<h1>Page not found</h1>')
		# print(request.user.username)
		# print(request.user.parent_business)
		user_business_id = request.user.parent_business
		form = self.form_class(parent_business_name=user_business_id)
		return render(request, self.template_name, {'form': form, 'title':"Discount Creation",'submit_text':"create"})
		
	def post(self, request, *args, **kwargs):
		user_business_id = request.user.parent_business
		form = self.form_class(request.POST, parent_business_name=user_business_id)
		if form.is_valid():
			form.save()
			# <process form cleaned data>
			return redirect(self.success_url)

		return render(request, self.template_name, {'form': form, 'title':"Discount Creation",'submit_text':"create"})

class Create_Coupon_Donation(View):
	form_class = couponDonationCreationForm
	success_url = 'see_coupons'
	template_name = 'form.html'
	
	def get(self, request, *args, **kwargs):
		if(request.user.user_type != 'BU'):
			return HttpResponseNotFound('<h1>Page not found</h1>')

		user_business_id = request.user.parent_business
		form = self.form_class(parent_business_name=user_business_id)
		return render(request, self.template_name, {'form': form, 'title':"Donation Creation",'submit_text':"create"})
		
	def post(self, request, *args, **kwargs):
		user_business_id = request.user.parent_business
		form = self.form_class(request.POST, parent_business_name=user_business_id)
		if form.is_valid():
			form.save()
			# <process form cleaned data>
			return redirect(self.success_url)

		return render(request, self.template_name, {'form': form, 'title':"Donation Creation",'submit_text':"create"})
#----------------------------------------------------------------------------------------------------------------------------------------------------

#EDIT Coupon
#----------------------------------------------------------------------------------------------------------------------------------------------------
def delete_coupon(request,coupon_id =None, end_route='see_coupons'):
	try:
		coupon_obj = coupon.objects.get(id=coupon_id)
	except coupon.DoesNotExist:
		return HttpResponseNotFound('<h1>Coupon Does Not Exist</h1>')

	if (coupon_obj.parent_business != request.user.parent_business):
			return HttpResponse('<h1> Access Denied </h1>', status=403)

	coupon_obj.delete()

	return HttpResponseRedirect(reverse(end_route))

def deactivate_coupon(request,coupon_id =None, end_route='see_coupons'):
	try:
		coupon_obj = coupon.objects.get(id=coupon_id)
	except coupon.DoesNotExist:
		return HttpResponseNotFound('<h1>Coupon Does Not Exist</h1>')

	if (coupon_obj.parent_business != request.user.parent_business):
			return HttpResponse('<h1> Access Denied </h1>', status=403)

	coupon_obj.is_active = False
	coupon_obj.save()
	return HttpResponseRedirect(reverse(end_route))

def activate_coupon(request,coupon_id =None, end_route='see_coupons'):
	try:
		coupon_obj = coupon.objects.get(id=coupon_id)
	except coupon.DoesNotExist:
		return HttpResponseNotFound('<h1>Coupon Does Not Exist</h1>')

	if (coupon_obj.parent_business != request.user.parent_business):
			return HttpResponse('<h1> Access Denied </h1>', status=403)
		
	coupon_obj.is_active = True
	coupon_obj.save()
	return HttpResponseRedirect(reverse(end_route))

class Coupon_Discount_Edit(View):
	form_class = couponDiscountChangeForm
	success_url = 'see_coupons'
	template_name = 'form.html'
	
	def get(self, request, *args, **kwargs):
		if(request.user.user_type != 'BU'):
			return HttpResponseNotFound('<h1>Page not found</h1>')
		try:
			coupon_obj = coupon.objects.get(id=self.kwargs['coupon_id'], is_donation=False)
		except coupon.DoesNotExist:
			return HttpResponseNotFound('<h1>Coupon Does Not Exist</h1>')
		if (coupon_obj.parent_business != request.user.parent_business):
			return HttpResponse('<h1> Access Denied </h1>', status=403)
		form = self.form_class(instance=coupon_obj)
		return render(request, self.template_name, {'form': form, 'title':"Discount Coupon Modification",'submit_text':"save"})
		
	def post(self, request, *args, **kwargs):
		try:
			coupon_obj = coupon.objects.get(id=self.kwargs['coupon_id'], is_donation=False)
		except coupon.DoesNotExist:
			return HttpResponseNotFound('<h1>Coupon Does Not Exist</h1>')
		
		if (coupon_obj.parent_business != request.user.parent_business):
			return HttpResponse('<h1> Access Denied </h1>', status=403)

		form = self.form_class(request.POST,instance=coupon_obj)
		if form.is_valid():
			form.save()
			return redirect(self.success_url)
		return render(request, self.template_name, {'form': form, 'title':"Discount Coupon Modification",'submit_text':"save"})

class Coupon_Donation_Edit(View):
	form_class = couponDonationChangeForm
	success_url = 'see_coupons'
	template_name = 'form.html'
	
	def get(self, request, *args, **kwargs):
		if(request.user.user_type != 'BU'):
			return HttpResponseNotFound('<h1>Page not found</h1>')
		try:
			coupon_obj = coupon.objects.get(id=self.kwargs['coupon_id'], is_donation=True)
		except coupon.DoesNotExist:
			return HttpResponseNotFound('<h1>Coupon Does Not Exist</h1>')
		if (coupon_obj.parent_business != request.user.parent_business):
			return HttpResponse('<h1> Access Denied </h1>', status=403)
		
		form = self.form_class(instance=coupon_obj)
		return render(request, self.template_name, {'form': form, 'title':"Donation Coupon Modification",'submit_text':"save"})
		
	def post(self, request, *args, **kwargs):
		try:
			coupon_obj = coupon.objects.get(id=self.kwargs['coupon_id'], is_donation=True)
		except coupon.DoesNotExist:
			return HttpResponseNotFound('<h1>Coupon Does Not Exist</h1>')
		if (coupon_obj.parent_business != request.user.parent_business):
			return HttpResponse('<h1> Access Denied </h1>', status=403)
		
		form = self.form_class(request.POST,instance=coupon_obj)
		if form.is_valid():
			form.save()
			return redirect(self.success_url)
		return render(request, self.template_name, {'form': form, 'title':"Donation Coupon Modification",'submit_text':"save"})
#----------------------------------------------------------------------------------------------------------------------------------------------------