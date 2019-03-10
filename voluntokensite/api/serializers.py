#!/usr/bin/python

from users.models import CustomUser
from rest_framework import serializers


class CreateUserSerializer(serializers.ModelSerializer):
	username = serializers.CharField()
	password = serializers.CharField(write_only=True,
									style={'input_type': 'password'})

	class Meta:
		model = CustomUser
#		fields = ('email', 'username')
		fields = ('email', 'username', 'password')
		write_only_fields = ('password')

	def create(self, validated_data):
		user = super(CreateUserSerializer, self).create(validated_data)
		user.set_password(validated_data['password'])
		user.save()
		return user
