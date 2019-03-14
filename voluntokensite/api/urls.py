# api/urls.py
#from django.urls import include, path
#
#urlpatterns = [
#	path('users/', include('users.urls')),
#	path('rest-auth/', include('rest_auth.urls')),
#]
from django.conf.urls import url
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from api import views

urlpatterns = [
	#USER AUTH API ROUTES
	#----------------------------------------------------------------------------------------------------------------------------------------------------
	url(r'^auth/login/$',
		obtain_auth_token,
		name='auth_user_login'),
	url(r'^auth/register/$',
		views.CreateUserAPIView.as_view(),
		name='auth_user_create'),
	url(r'^auth/logout/$',
		views.LogoutUserAPIView.as_view(),
		name='auth_user_logout'),
	#----------------------------------------------------------------------------------------------------------------------------------------------------

	#NGO API ROUTES
	#----------------------------------------------------------------------------------------------------------------------------------------------------
	#GET Requests
	path('get_all_event/', views.get_all_event.as_view(), name='get_all_event'),
	path('get_all_ngo/', views.get_all_ngo.as_view(), name='get_all_ngo'),

	path('get_all_ngo_event/<int:parent_ngo_id>', views.get_all_ngo_event.as_view(), name='get_all_ngo_event'),
	path('get_ngo/<int:ngo_id>', views.get_ngo.as_view(), name='get_ngo'),
	path('get_event/<int:event_id>', views.get_event.as_view(), name='get_event'),
	path('get_event_registered_users/<int:event_id>', views.get_event_registered_users.as_view(), name='get_event_registered_users'),
	
	#self.request.user
	path('get_all_my_event/', views.get_all_my_event.as_view(), name='get_all_my_event'),
	path('is_user_registered_for_event/', views.is_user_registered_for_event.as_view(), name='is_user_registered_for_event'),
	
	#DELETE Request
	path('signoff_user_for_event/', views.unregister_user_for_event.as_view(), name='unregister_user_for_event'),

	#POST Request
	path('signup_user_for_event/', views.register_user_for_event.as_view(), name='register_user_for_event'),
	
	#----------------------------------------------------------------------------------------------------------------------------------------------------

	#BUSINESS API ROUTES
	#----------------------------------------------------------------------------------------------------------------------------------------------------
	path('get_coupon/<int:coupon_id>', views.get_coupon.as_view(), name='get_coupon'),
	path('get_all_business_discount_coupon/<int:parent_business_id>', views.get_all_business_discount_coupon.as_view(), name='get_all_business_discount_coupon'),
	path('get_all_business_donation_coupon/<int:parent_business_id>', views.get_all_business_donation_coupon.as_view(), name='get_all_business_donation_coupon'),
	path('get_all_coupon', views.get_all_coupon.as_view(), name='get_all_coupon'),

	path('get_business/<int:business_id>', views.get_business.as_view(), name='get_business'),
	path('get_all_business', views.get_all_business.as_view(), name='get_all_business'),

	#----------------------------------------------------------------------------------------------------------------------------------------------------



]