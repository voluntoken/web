#!/usr/bin/python

from users.models import CustomUser
from rest_framework import serializers
from NGO.models import event, org, event_registration_stub, checks_stub
from BUSINESS.models import coupon, business, transaction_stub
from django.contrib.auth.password_validation import validate_password
#User AuthSerializer
#----------------------------------------------------------------------------------------------------------------------------------------------------
class CreateUserSerializer(serializers.ModelSerializer):
	username = serializers.CharField()
	password = serializers.CharField(write_only=True,
									style={'input_type': 'password'})
	
	class Meta:
		model = CustomUser
		fields = ('email', 'username', 'password', 'first_name', 'last_name', 'is_public', 'volunteer_role')
		write_only_fields = ('password')

	def create(self, validated_data):
		user = super(CreateUserSerializer, self).create(validated_data)
		user.set_password(validated_data['password'])
		user.save()
		return user

class ChangeUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomUser
		fields = ('id', 'email', 'username', 'first_name', 'last_name', 'user_type', 'is_public', 'volunteer_role', 'volunteer_token', 'volunteer_hour')
		read_only_fields = ('id', 'username', 'user_type', 'volunteer_hour', 'volunteer_token')


class ChangePasswordSerializer(serializers.Serializer):
	"""
	Serializer for password change endpoint.
	"""
	old_password = serializers.CharField(required=True)
	new_password = serializers.CharField(required=True)

	def validate_new_password(self, value):
		validate_password(value)
		return value

class UserVolunteerSerializer(serializers.ModelSerializer):

	class Meta:
		model = CustomUser
		fields = ('id', 'email', 'username', 'first_name', 'last_name', 'user_type', 'is_public', 'volunteer_role', 'volunteer_token', 'volunteer_hour')
		#read_only_fields = ('id', 'username', 'user_type', 'volunteer_hour', 'volunteer_token')


#----------------------------------------------------------------------------------------------------------------------------------------------------


#NGO Serializers
#----------------------------------------------------------------------------------------------------------------------------------------------------
class EventSerializer(serializers.ModelSerializer):
	class Meta:
		model = event
		fields = ('id', 'qr_code', 'parent_ngo', 'name', 'description', 'is_active', 'start_time', 'end_time', 'volunteer_hour')
		#read_only_fields = ('id', 'qr_code', 'parent_ngo', 'name', 'description', 'is_active', 'start_time', 'end_time')

class NGOSerializer(serializers.ModelSerializer):
	class Meta:
		model = org
		fields = ('id', 'name', 'description', 'email', 'address')
		#read_only_fields = ('id', 'name', 'description', 'email', 'address')
		
class EventRegistrationStubSerializer(serializers.ModelSerializer):
	parent_volunteer = serializers.ReadOnlyField(source='parent_volunteer.id')
	class Meta:
		model = event_registration_stub
		fields = ('id', 'parent_event', 'parent_volunteer')

#----------------------------------------------------------------------------------------------------------------------------------------------------


#BUSINESS Serializers
#----------------------------------------------------------------------------------------------------------------------------------------------------
class CouponSerializer(serializers.ModelSerializer):
	class Meta:
		model = coupon
		fields = ('id', 'name', 'description', 'is_donation', 'token_cost', 'parent_business', 'donation_val')

class BusinessSerializer(serializers.ModelSerializer):
	class Meta:
		model = business
		fields = ('id', 'name', 'description', 'email', 'address')


class TransactionStubSerializer(serializers.ModelSerializer):
	parent_volunteer = serializers.ReadOnlyField(source='parent_volunteer.id')
	class Meta:
		model = transaction_stub
		fields = ('id', 'parent_business', 'parent_volunteer', 'tokens_transferred', 'is_donation')	

#----------------------------------------------------------------------------------------------------------------------------------------------------