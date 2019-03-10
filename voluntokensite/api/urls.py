# api/urls.py
#from django.urls import include, path
#
#urlpatterns = [
#	path('users/', include('users.urls')),
#	path('rest-auth/', include('rest_auth.urls')),
#]
from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from .views import CreateUserAPIView, LogoutUserAPIView

urlpatterns = [
	url(r'^auth/login/$',
		obtain_auth_token,
		name='auth_user_login'),
	url(r'^auth/register/$',
		CreateUserAPIView.as_view(),
		name='auth_user_create'),
	url(r'^auth/logout/$',
		LogoutUserAPIView.as_view(),
		name='auth_user_logout')
]