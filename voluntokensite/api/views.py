#from django.shortcuts import render
#
## Create your views here.
#from rest_framework import generics
#
#from users.models import CustomUser 
#from . import serializers
#
#class UserListView(generics.ListCreateAPIView):
#	queryset = models.CustomUser.objects.all()
#	serializer_class = serializers.UserSerializer
	
# backend/api/views.py

from users.models import CustomUser
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from api.serializers import CreateUserSerializer


class CreateUserAPIView(CreateAPIView):
	serializer_class = CreateUserSerializer
	permission_classes = [AllowAny]

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		# We create a token than will be used for future auth
		token = Token.objects.create(user=serializer.instance)
		token_data = {"token": token.key}
		return Response(
			{**serializer.data, **token_data},
			status=status.HTTP_201_CREATED,
			headers=headers
		)


class LogoutUserAPIView(APIView):
	queryset = CustomUser.objects.all()

	def get(self, request, format=None):
		# simply delete the token to force a login
		request.user.auth_token.delete()
		return Response(status=status.HTTP_200_OK)