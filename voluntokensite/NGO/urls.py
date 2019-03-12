# BUSINESS/urls.py
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
	path('create_event/', views.Create_Event.as_view(), name='create_event'),
	path('see_events/', views.Show_Events.as_view(), name='see_events'),
	path('edit_event/<event_id>', views.Change_Event.as_view(), name='edit_event'),
	path('delete_edit/<event_id>', views.delete_event, name='delete_event'),

]