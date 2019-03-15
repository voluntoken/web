#!/usr/bin/python

from users.models import CustomUser
from rest_framework import serializers
from NGO.models import event, org, event_registration_stub, checks_stub
from BUSINESS.models import coupon, business, transaction_stub

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

class UserVolunteerSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomUser
		fields = ('id', 'email', 'username', 'first_name', 'last_name', 'user_type', 'is_public', 'volunteer_role', 'volunteer_token', 'volunteer_hour')
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
		fields = ('id', 'name', 'description', 'email', 'address')


# class EventRegistrationStubSerializer(serializers.Serializer):
# 	parent_volunteer = serializers.ReadOnlyField(source='parent_volunteer.username')
# 	parent_event     = serializers.IntegerField()

# 	def create(self, validated_data):
# 		return event_registration_stub.objects.create(**validated_data)

# 	def update(self, instance, validated_data):
# 		instance.parent_volunteer = validated_data.get('parent_volunteer', instance.parent_volunteer)
# 		instance.parent_event     = validated_data.get('parent_event', instance.parent_event)
# 		isntance.save()
# 		return instance


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