# users/views.py
from django.urls import reverse_lazy
from django.views import generic
from .models import coupon, total_support_stub, EXCHANGE_TOKEN_HOUR, user_support_stub
from .forms import couponDiscountCreationForm, couponDiscountChangeForm, couponDonationCreationForm, couponDonationChangeForm

from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404, HttpResponseNotFound
from django.urls import reverse


#VIEW STATS
#----------------------------------------------------------------------------------------------------------------------------------------------------
class View_Stats(View):
	template_name = 'business_stats.html'

	def get(self, request, *args, **kwargs):
		if(request.user.user_type != 'BU'):
			return HttpResponseNotFound('<h1>Page not found</h1>')

		#Table of NGOs Supported: ngos_supported
		business_instance = request.user.parent_business
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

			ngos_supported.append(ngo_support_info)

		return render(request, self.template_name, {'title':"Business Stats", "ngos_supported": ngos_supported})




#----------------------------------------------------------------------------------------------------------------------------------------------------


#SHOW Coupon
#----------------------------------------------------------------------------------------------------------------------------------------------------
class Show_Coupon(View):
	template_name = 'coupon_view.html'
	
	def get(self, request, *args, **kwargs):
		if(request.user.user_type != 'BU'):
			return HttpResponseNotFound('<h1>Page not found</h1>')
		user_business_id = request.user.parent_business		
		coupon_list = coupon.objects.filter(parent_business=user_business_id)
		return render(request, self.template_name, {'title':"Coupons","coupons":coupon_list})		
#----------------------------------------------------------------------------------------------------------------------------------------------------

#CREATE Coupon
#----------------------------------------------------------------------------------------------------------------------------------------------------
class Create_Coupon_Discount(View):
	form_class = couponDiscountCreationForm
	success_url = reverse_lazy('')
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
			return render(request, 'business_home.html', {})

		return render(request, self.template_name, {'form': form})

class Create_Coupon_Donation(View):
	form_class = couponDonationCreationForm
	success_url = reverse_lazy('')
	template_name = 'form.html'
	
	def get(self, request, *args, **kwargs):
		if(request.user.user_type != 'BU'):
			return HttpResponseNotFound('<h1>Page not found</h1>')
		# print(request.user.username)
		# print(request.user.parent_business)
		user_business_id = request.user.parent_business
		form = self.form_class(parent_business_name=user_business_id)
		return render(request, self.template_name, {'form': form, 'title':"Donation Creation",'submit_text':"create"})
		
	def post(self, request, *args, **kwargs):
		user_business_id = request.user.parent_business
		form = self.form_class(request.POST, parent_business_name=user_business_id)
		if form.is_valid():
			form.save()
			# <process form cleaned data>
			return render(request, 'business_home.html', {})

		return render(request, self.template_name, {'form': form})
#----------------------------------------------------------------------------------------------------------------------------------------------------

#EDIT Coupon
#----------------------------------------------------------------------------------------------------------------------------------------------------
def delete_coupon(request,coupon_id =None, end_route='see_coupons'):
	coupon_obj = coupon.objects.get(id=coupon_id)
	coupon_obj.delete()
	return HttpResponseRedirect(reverse(end_route))

class Coupon_Discount_Edit(View):
	form_class = couponDiscountChangeForm
	success_url = reverse_lazy('')
	template_name = 'form.html'
	
	def get(self, request, *args, **kwargs):
		if(request.user.user_type != 'BU'):
			return HttpResponseNotFound('<h1>Page not found</h1>')
		coupon_obj = coupon.objects.get(id=self.kwargs['coupon_id'])
		form = self.form_class(instance=coupon_obj)
		return render(request, self.template_name, {'form': form, 'title':"Coupon Modification",'submit_text':"save"})
		
	def post(self, request, *args, **kwargs):
		coupon_obj = coupon.objects.get(id=self.kwargs['coupon_id'])
		form = self.form_class(request.POST,instance=coupon_obj)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('see_coupons'))
		return render(request, self.template_name, {'form': form})

class Coupon_Donation_Edit(View):
	form_class = couponDonationChangeForm
	success_url = reverse_lazy('')
	template_name = 'form.html'
	
	def get(self, request, *args, **kwargs):
		if(request.user.user_type != 'BU'):
			return HttpResponseNotFound('<h1>Page not found</h1>')
		coupon_obj = coupon.objects.get(id=self.kwargs['coupon_id'])
		form = self.form_class(instance=coupon_obj)
		return render(request, self.template_name, {'form': form, 'title':"Coupon Modification",'submit_text':"save"})
		
	def post(self, request, *args, **kwargs):
		coupon_obj = coupon.objects.get(id=self.kwargs['coupon_id'])
		form = self.form_class(request.POST,instance=coupon_obj)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('see_coupons'))
		return render(request, self.template_name, {'form': form})
#----------------------------------------------------------------------------------------------------------------------------------------------------