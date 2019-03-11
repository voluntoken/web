# BUSINESS/urls.py
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
	path('create_coupons_dis/', views.Create_Coupon_Discount.as_view(), name='create_coupons_dis'),
#	path('create_coupons_don/', views.Create_Coupon_Donation.as_view(), name='create_coupons_don'),
]