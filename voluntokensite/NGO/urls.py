# BUSINESS/urls.py
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
	path('create_event/', views.Create_Event.as_view(), name='create_event'),
]