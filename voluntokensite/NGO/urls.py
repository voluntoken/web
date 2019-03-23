# BUSINESS/urls.py
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
	path('ngo_stats/', views.View_Stats.as_view(), name='ngo_stats'),
	path('create_event/', views.Create_Event.as_view(), name='create_event'),
	path('see_events/', views.Show_Events.as_view(), name='see_events'),
	path('edit_event/<event_id>', views.Change_Event.as_view(), name='edit_event'),
	path('delete_edit/<event_id>/<end_route>', views.delete_event, name='delete_event'),
	path('deactivate_event/<event_id>/<end_route>', views.deactivate_event, name='deactivate_event'),
	path('activate_event/<event_id>/<end_route>', views.activate_event, name='activate_event'),
]