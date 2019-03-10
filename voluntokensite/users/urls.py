# users/urls.py
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('signup_volunteer/', views.SignUp_Volunteer.as_view(), name='signup_volunteer'),
    path('signup_ngo/', views.SignUp_NGO.as_view(), name='signup_ngo'),
    path('signup_business/', views.SignUp_Business.as_view(), name='signup_business'),
      	
    #EMAIL CONFIRMATION
   	#path('signup/', views.signuprequest, name='signuprequest'),
    #url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #    views.activate, name='activate'),

]