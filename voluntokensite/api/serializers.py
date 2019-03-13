#!/usr/bin/python

from users.models import CustomUser
from rest_framework import serializers
from NGO.models import event, org
from BUSINESS.models import coupon, business

#User AuthSerializer
#----------------------------------------------------------------------------------------------------------------------------------------------------
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

class ChangeUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomUser

class UserVolunteerSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomUser
		fields = ('first_name', 'last_name', 'user_type', 'is_public', 'volunteer_role')
#----------------------------------------------------------------------------------------------------------------------------------------------------


#NGO Serializers
#----------------------------------------------------------------------------------------------------------------------------------------------------
class EventSerializer(serializers.ModelSerializer):
	class Meta:
		model = event
		fields = ('id', 'qr_code', 'parent_ngo', 'name', 'description', 'is_active', 'start_time', 'end_time')

class NGOSerializer(serializers.ModelSerializer):
	class Meta:
		model = org
		fields = ('name', 'description', 'email', 'address')

#----------------------------------------------------------------------------------------------------------------------------------------------------


#BUSINESS Serializers
#----------------------------------------------------------------------------------------------------------------------------------------------------
class CouponSerializer(serializers.ModelSerializer):
	class Meta:
		model = coupon
		fields = ('name', 'description', 'is_donation', 'token_cost', 'parent_business', 'donation_val')

class BusinessSerializer(serializers.ModelSerializer):
	class Meta:
		model = business
		fields = ('name', 'description', 'email', 'address')
	

#----------------------------------------------------------------------------------------------------------------------------------------------------