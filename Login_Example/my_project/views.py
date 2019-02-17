from django.shortcuts import render
from django.http import HttpResponse
import requests


def home_page(request):
	context = {}
	print("Redirecting to right page!")
	
	if request.user.is_authenticated:
		if request.user.is_superuser:
			print("super_user")
			return render(request, 'home_admin.html', context)
		else :
			print("regular_user")
			return render(request, 'home_user.html', context)
			
	print("error")
	return render(request, 'home_user.html', context)
	
	