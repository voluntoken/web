# BUSINESS/urls.py
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
	path('business_stats/', views.View_Stats.as_view(), name='business_stats'),
	path('create_coupons_dis/', views.Create_Coupon_Discount.as_view(), name='create_coupons_dis'),
	path('create_coupons_don/', views.Create_Coupon_Donation.as_view(), name='create_coupons_don'),
	path('see_coupons/', views.Show_Coupon.as_view(), name='see_coupons'),
	path('edit_coupons_dis/<coupon_id>', views.Coupon_Discount_Edit.as_view(), name='coupon_dis_edit'),
	path('edit_coupons_don/<coupon_id>', views.Coupon_Donation_Edit.as_view(), name='coupon_don_edit'),
	path('delete_coupon/<coupon_id>/<end_route>', views.delete_coupon, name='delete_coupon'),
	path('deactivate_coupon/<coupon_id>/<end_route>', views.deactivate_coupon, name='deactivate_coupon'),
	path('activate_coupon/<coupon_id>/<end_route>', views.activate_coupon, name='activate_coupon'),
]