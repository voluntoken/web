# users/views.py
from django.urls import reverse_lazy
from django.views import generic
from .models import coupon
from .forms import couponDiscountCreationForm, couponDiscountChangeForm, couponDonationCreationForm, couponDonationChangeForm

from django.views import View
from django.shortcuts import render, redirect


class Create_Coupon_Discount(View):
	form_class = couponDiscountCreationForm
	success_url = reverse_lazy('')
	template_name = 'form.html'
	
	def get(self, request, *args, **kwargs):
		print(request.user.username)
		print(request.user.parent_business)
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

	
#class Create_Coupon_Donation(generic.CreateView):

