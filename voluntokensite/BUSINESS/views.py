# users/views.py
from django.urls import reverse_lazy
from django.views import generic
from .models import coupon
from .forms import couponDiscountCreationForm, couponDiscountChangeForm, couponDonationCreationForm, couponDonationChangeForm

from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

#COUPONS
#----------------------------------------------------------------------------------------------------------------------------------------------------


def delete_coupon(request,coupon_id =None, end_route='see_coupons_dis'):
	coupon_obj = coupon.objects.get(id=coupon_id)
	coupon_obj.delete()
	return HttpResponseRedirect(reverse(end_route))

class Coupon_Discount_Edit(View):
	form_class = couponDiscountChangeForm
	success_url = reverse_lazy('')
	template_name = 'form.html'
	
	def get(self, request, *args, **kwargs):
		
		coupon_obj = coupon.objects.get(id=self.kwargs['coupon_id'])
		form = self.form_class(instance=coupon_obj)
		return render(request, self.template_name, {'form': form, 'title':"Coupon Modification",'submit_text':"save"})
		
	def post(self, request, *args, **kwargs):
		coupon_obj = coupon.objects.get(id=self.kwargs['coupon_id'])
		form = self.form_class(request.POST,instance=coupon_obj)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('see_coupons_dis'))
		return render(request, self.template_name, {'form': form})

class Coupon_Donation_Edit(View):
	form_class = couponDonationChangeForm
	success_url = reverse_lazy('')
	template_name = 'form.html'
	
	def get(self, request, *args, **kwargs):
		
		coupon_obj = coupon.objects.get(id=self.kwargs['coupon_id'])
		form = self.form_class(instance=coupon_obj)
		return render(request, self.template_name, {'form': form, 'title':"Coupon Modification",'submit_text':"save"})
		
	def post(self, request, *args, **kwargs):
		coupon_obj = coupon.objects.get(id=self.kwargs['coupon_id'])
		form = self.form_class(request.POST,instance=coupon_obj)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('see_coupons_don'))
		return render(request, self.template_name, {'form': form})


class Show_Coupon_Discount(View):
	template_name = 'coupon_view.html'
	
	def get(self, request, *args, **kwargs):
			user_business_id = request.user.parent_business		
			
			coupon_list = coupon.objects.filter(parent_business=user_business_id,is_donation=False)
			print(coupon_list)
			return render(request, self.template_name, {'title':"Discount Coupons","coupons":coupon_list})		
	
class Show_Coupon_Donation(View):
	template_name = 'coupon_view.html'
	
	def get(self, request, *args, **kwargs):
			user_business_id = request.user.parent_business
			
			coupon_list = coupon.objects.filter(parent_business=user_business_id,is_donation=True)
			print(coupon_list)
			return render(request, self.template_name, {'title':"Donation Coupons","coupons":coupon_list})

	
	


class Create_Coupon_Discount(View):
	form_class = couponDiscountCreationForm
	success_url = reverse_lazy('')
	template_name = 'form.html'
	
	def get(self, request, *args, **kwargs):
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