# djauth/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic.base import TemplateView

from django.conf import settings
from django.views.static import serve

from users.views import home_page

urlpatterns = [
#    path('', TemplateView.as_view(template_name='home.html'), name='home'),
	path('', home_page, name='home'),
    path('admin/', admin.site.urls),
    url(r'api/', include('api.urls')),
#    path('api/v1/', include('api.urls')),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
	path('BUSINESS/', include('BUSINESS.urls')),



]

if settings.DEBUG:
	urlpatterns += [
		url(r'^media/(?P<path>.*)$', serve, {
			'document_root': settings.MEDIA_ROOT,
		}),
	]