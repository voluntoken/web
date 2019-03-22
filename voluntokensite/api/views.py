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
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from NGO.permissions import IsParentVolunteerOrReadOnly

from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from api import serializers

from datetime import datetime, timedelta


from django.http import Http404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from NGO.models   import event, org, event_registration_stub, checks_stub, event_hours_spent_stub
from BUSINESS.models import business, coupon, transaction_stub, total_support_stub
from users.models import CustomUser, total_hours_stub
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView


#time stuff
import pytz
utc=pytz.utc

#exchange rate
EXCHANGE_TOKEN_HOUR = 1.0 #units = token/hour

#USER VIEWS
#----------------------------------------------------------------------------------------------------------------------------------------------------
class CreateUserAPIView(generics.CreateAPIView):
	serializer_class = serializers.CreateUserSerializer
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

class ChangeUserAPIView(generics.RetrieveUpdateAPIView):
	serializer_class = serializers.ChangeUserSerializer
	def get_object(self):
		user_id     = self.request.user.id
		try:
			return CustomUser.objects.get(id=user_id, is_active=True)
		except CustomUser.DoesNotExist:
			raise Http404

class ChangePasswordAPIView(APIView):
	"""
    An endpoint for changing password.
    """
	def get_object(self, queryset=None):
		return self.request.user

	def put(self, request, *args, **kwargs):
		self.object = self.get_object()
		serializer = serializers.ChangePasswordSerializer(data=request.data)

		if serializer.is_valid():
			# Check old password
			old_password = serializer.data.get("old_password")
			if not self.object.check_password(old_password):
				return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
			# set_password also hashes the password that the user will get
			self.object.set_password(serializer.data.get("new_password"))
			self.object.save()
			return Response(status=status.HTTP_204_NO_CONTENT)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutUserAPIView(APIView):
	queryset = CustomUser.objects.all()

	def get(self, request, format=None):
		# simply delete the token to force a login
		request.user.auth_token.delete()
		return Response(status=status.HTTP_200_OK)

class get_user(generics.RetrieveAPIView):
	serializer_class = serializers.UserVolunteerSerializer
	def get_object(self):
		try:
			return CustomUser.objects.get(id=self.request.user.id)
		except:
			raise Http404
#----------------------------------------------------------------------------------------------------------------------------------------------------

#Home Page API Routes
#----------------------------------------------------------------------------------------------------------------------------------------------------



class make_checkin(APIView):
	def post(self, request):
		event_id        = request.data['event_id']
		pin_try         = int(request.data['pin_try'])

		#CHECK event exists and is active
		try:
			event_instance = event.objects.get(id=event_id, is_active=True)
		except:
			return Response(data ={'error_message':'event not found', 'success':False})


		#CHECK correct pin
		correct_pin      = event_instance.pin_checkin
		if (correct_pin != pin_try):
			return Response(data ={'error_message':'incorrect pin', 'success':False})

		time_now         = datetime.utcnow()
		time_now         = time_now.replace(tzinfo=utc)
		tolerance        = 60.0*60.0 #in seconds
		event_start_time = event_instance.start_time.replace(tzinfo=utc)
		event_end_time   = event_instance.end_time.replace(tzinfo=utc) 

		print(str(event_instance.start_time))
		#TIME ERROR CHECKS
		if ((event_start_time - time_now).total_seconds() >= tolerance):
			return Response(data = {'error_message':'event has not started', 'success':False})
		elif ((time_now  - event_end_time).total_seconds() >= tolerance):
			return Response(data = {'error_message':'event has ended', 'success':False})

		#ALREADY CHECKED IN ERROR
		try:
			last_stub   = checks_stub.objects.filter(parent_event=event_instance, parent_volunteer=self.request.user).last()
			if(last_stub.is_check_in == True):
				return Response(data = {'error_message':'you are already checked in!', 'success':False})
		except:
			pass
		#CREATE CHECKS_STUB FOR CHECKIN
		stub = checks_stub.objects.create(is_check_in=True, parent_event=event_instance, parent_volunteer=self.request.user, time= time_now)
		stub.save()
		return Response(data ={'error_message':'none', 'success':True})

class make_checkout(APIView):
	def post(self, request):
		event_id        = request.data['event_id']
		pin_try         = int(request.data['pin_try'])

		#CHECK event exists and is active
		try:
			event_instance = event.objects.get(id=event_id, is_active=True)
		except:
			return Response(data ={'error_message':'event not found', 'success':False})


		#CHECK correct pin
		correct_pin      = event_instance.pin_checkout
		if (correct_pin != pin_try):
			return Response(data ={'error_message':'incorrect pin', 'success':False})

		time_now         = datetime.utcnow()
		time_now         = time_now.replace(tzinfo=utc)
		tolerance        = 60.0*60.0 #in seconds
		event_start_time = event_instance.start_time.replace(tzinfo=utc)
		event_end_time   = event_instance.end_time.replace(tzinfo=utc) 

		print(str(event_instance.start_time))
		#TIME ERROR CHECKS
		if ((event_start_time - time_now).total_seconds() >= tolerance):
			return Response(data = {'error_message':'Event has not started!', 'success':False})
		elif ((time_now  - event_end_time).total_seconds() >= tolerance):
			return Response(data = {'error_message':'Event has ended!', 'success':False})

		
		try:
			last_stub   = checks_stub.objects.filter(parent_event=event_instance, parent_volunteer=self.request.user).last()
			#ALREADY CHECKED OUT ERROR
			if(last_stub.is_check_in == False):
				return Response(data = {'error_message':'You are already checked out!', 'success':False})
		except:
			#NOT CHECKED OUT ERROR
			return Response(data = {'error_message':'You have not checked in!', 'success':False})


		#CREATE CHECKS_STUB FOR CHECKOUT
		new_checks_stub = checks_stub.objects.create(is_check_in=False, parent_event=event_instance, parent_volunteer=self.request.user, time= time_now)

		#CREATE event_hours_spent_stub for good bookkeeping
		check_in_time  = last_stub.time.replace(tzinfo=utc)
		check_out_time = time_now

		hours_spent    = ((check_out_time - check_in_time).total_seconds())/(60.0*60.0)
		new_hours_stub = event_hours_spent_stub.objects.create(parent_event=event_instance, parent_volunteer=self.request.user, hours=hours_spent)		
		

		#Update NGO Volunteer Hours
		ngo_parent                 = event_instance.parent_ngo
		ngo_parent.volunteer_hour += hours_spent 
		

		#Update Event Volunteer Hours
		event_instance.volunteer_hour += hours_spent
		

		#UPDATE CustomUser 
		tokens_earned  = hours_spent*EXCHANGE_TOKEN_HOUR
		user_instance  = self.request.user
		user_instance.volunteer_token += tokens_earned
		user_instance.volunteer_hour  += hours_spent
		

		#Update total_hours_stub for CustomUser
		try:
			total_hours_stub_instance  = total_hours_stub.objects.get(parent_ngo=ngo_parent, parent_volunteer=user_instance)
		except total_hours_stub.DoesNotExist:
			total_hours_stub_instance  = total_hours_stub.objects.create(parent_ngo=ngo_parent, parent_volunteer=user_instance)

		total_hours_stub_instance.total_hours += hours_spent


		new_checks_stub.save()
		new_hours_stub.save()
		ngo_parent.save()
		event_instance.save()
		user_instance.save()
		total_hours_stub_instance.save()

		return Response(data ={'error_message':'none', 'success':True})

#----------------------------------------------------------------------------------------------------------------------------------------------------

#NGO API Routes
#----------------------------------------------------------------------------------------------------------------------------------------------------
class get_all_event(generics.ListAPIView):
	#setting authentication, permission to empty!
	authentication_classes = []
	permission_classes = []
	queryset = event.objects.filter(is_active=True)
	serializer_class = serializers.EventSerializer

class get_all_ngo(generics.ListAPIView):
	#setting authentication, permission to empty!
	authentication_classes = []
	permission_classes = []
	queryset = org.objects.filter(is_active=True)
	serializer_class = serializers.NGOSerializer

class get_all_ngo_event(generics.ListAPIView):
	#setting authentication, permission to empty!
	authentication_classes = []
	permission_classes = []
	
	def get_queryset(self):
		parent_ngo_id = self.kwargs['parent_ngo_id']
		return event.objects.filter(parent_ngo=parent_ngo_id, is_active=True)
	serializer_class = serializers.EventSerializer

class get_ngo(generics.RetrieveAPIView):
	#setting authentication, permission to empty!
	authentication_classes = []
	permission_classes = []
	def get_object(self):
		ngo_id = self.kwargs['ngo_id']
		try:
			return org.objects.get(id=ngo_id, is_active=True)
		except org.DoesNotExist:
			raise Http404
	serializer_class = serializers.NGOSerializer

class get_event(generics.RetrieveAPIView):
	#setting authentication, permission to empty!
	authentication_classes = []
	permission_classes = []
	def get_object(self):
		event_id = self.kwargs['event_id']
		try:
			return event.objects.get(id=event_id, is_active=True)
		except event.DoesNotExist:
			raise Http404

	serializer_class = serializers.EventSerializer



class get_event_registered_users(generics.ListAPIView):
	serializer_class = serializers.UserVolunteerSerializer
	def get_queryset(self):
		event_id    = self.kwargs['event_id']
		registration_stubs  = event_registration_stub.objects.filter(parent_event=event_id)
		user_ids            = [x.parent_volunteer.id for x in registration_stubs]
		return CustomUser.objects.filter(id__in=user_ids, is_public = True, is_active=True)

class get_all_my_event(generics.ListAPIView):
	serializer_class = serializers.EventSerializer
	def get_queryset(self):
		registration_stubs  = event_registration_stub.objects.filter(parent_volunteer=self.request.user)
		event_ids           = [x.parent_event.id for x in registration_stubs]
		return event.objects.filter(id__in=event_ids, is_active=True)
		

class is_user_registered_for_event(APIView):
	def get(self, request, **kwargs):
		event_id = kwargs['event_id']
		#if no registration stubs corresponding to parent_event and user, then return false, otherwise true
		if not event_registration_stub.objects.filter(parent_volunteer = request.user, parent_event=event_id):
			return Response(data={'is_user_registered_for_event':False})
		else:
			return Response(data={'is_user_registered_for_event':True})




class unregister_user_for_event(generics.DestroyAPIView):
	serializer_class = serializers.EventRegistrationStubSerializer
	def get_object(self):
		try:
			parent_event_data  = self.request.data['parent_event']
			return event_registration_stub.objects.filter(parent_volunteer=self.request.user, parent_event=parent_event_data).first()
		except:
			raise Http404
class register_user_for_event(generics.CreateAPIView):
	queryset         = event_registration_stub.objects.all()
	serializer_class = serializers.EventRegistrationStubSerializer
	def perform_create(self, serializer):
		parent_event_data     = self.request.data['parent_event']
		if not event_registration_stub.objects.filter(parent_volunteer = self.request.user, parent_event=parent_event_data):
			serializer.save(parent_volunteer=self.request.user)
		else:
			raise Http404#not sure if http404 error is appropriate
#----------------------------------------------------------------------------------------------------------------------------------------------------

#NGO API Routes
#----------------------------------------------------------------------------------------------------------------------------------------------------
class get_all_coupon(generics.ListAPIView):
	#setting authentication, permission to empty!
	authentication_classes = []
	permission_classes = []
	queryset = coupon.objects.filter(is_active=True)
	serializer_class = serializers.CouponSerializer

class get_all_business(generics.ListAPIView):
	#setting authentication, permission to empty!
	authentication_classes = []
	permission_classes = []
	queryset = business.objects.filter(is_active=True)
	serializer_class = serializers.BusinessSerializer


class get_all_business_discount_coupon(generics.ListAPIView):
	#setting authentication, permission to empty!
	authentication_classes = []
	permission_classes = []
	
	def get_queryset(self):
		parent_business_id = self.kwargs['parent_business_id']
		return coupon.objects.filter(parent_business=parent_business_id, is_active=True, is_donation=False)
	serializer_class = serializers.CouponSerializer

class get_all_business_donation_coupon(generics.ListAPIView):
	#setting authentication, permission to empty!
	authentication_classes = []
	permission_classes = []
	
	def get_queryset(self):
		parent_business_id = self.kwargs['parent_business_id']
		return coupon.objects.filter(parent_business=parent_business_id, is_active=True, is_donation=True)
	serializer_class = serializers.CouponSerializer



class get_business(generics.RetrieveAPIView):
	#setting authentication, permission to empty!
	authentication_classes = []
	permission_classes = []
	def get_object(self):
		business_id = self.kwargs['business_id']
		try:
			return business.objects.get(id=business_id, is_active=True)
		except business.DoesNotExist:
			raise Http404
	serializer_class = serializers.BusinessSerializer



class get_coupon(generics.RetrieveAPIView):
	#setting authentication, permission to empty!
	authentication_classes = []
	permission_classes = []
	def get_object(self):
		coupon_id     = self.kwargs['coupon_id']  
		try:
			return coupon.objects.get(id=coupon_id, is_active=True)
		except coupon.DoesNotExist:
			raise Http404
	serializer_class = serializers.CouponSerializer

class make_transaction_donation(APIView):
	def post(self, request):
		coupon_id       = request.data['coupon_id']
		pin_try         = int(request.data['pin_try'])


		#Check if Coupon is active, donation, and exists
		try:
			coupon_instance = coupon.objects.get(id=coupon_id, is_donation = True, is_active=True)
		except:
			return Response(data ={'error_message':'not donation', 'success':False})

		business_agent  = coupon_instance.parent_business
		correct_pin     = business_agent.pin

		#Check if PIN IS CORRECT
		if (correct_pin != pin_try):
			return Response(data ={'error_message':'incorrect pin', 'success':False})

		coupon_cost     = coupon_instance.token_cost
		volunteer       = request.user
		volunteer_funds = volunteer.volunteer_token

		#CHECK IF ENOUGH FUNDS
		if (volunteer_funds <= coupon_cost):
			return Response(data = {'error_message':'insufficient funds', 'success':False})

		#Update Volunteer Funds
		volunteer_funds                = volunteer_funds - coupon_cost
		volunteer.volunteer_token      = volunteer_funds
		
		#Update Business Donation Tokens and Hours
		business_agent.donation_tokens += coupon_cost
		business_agent.total_hours     += coupon_cost*1.0/(EXCHANGE_TOKEN_HOUR)

		#Update Transaction Stub Instance
		transaction_stub_instance      = transaction_stub.objects.create(is_donation=True,tokens_transferred = coupon_cost, item_cost = coupon_instance.item_cost,  parent_business =business_agent, parent_volunteer=volunteer)

		#Update relevant total_support_stub's
		total_hours_stub_set     = total_hours_stub.objects.filter(parent_volunteer=volunteer)
		for total_hours_stub_instance in total_hours_stub_set:
			ngo_instance         = total_hours_stub_instance.parent_ngo

			#Update total_support_stub_instance for specific ngo
			try:
				total_support_stub_instance = total_support_stub.objects.get(parent_business=business_agent, parent_ngo=ngo_instance)
			except total_support_stub.DoesNotExist:
				total_support_stub_instance = total_support_stub.objects.create(parent_business=business_agent, parent_ngo=ngo_instance)
			total_support_stub_instance.total_hours           += coupon_cost*1.0/(EXCHANGE_TOKEN_HOUR)
			total_support_stub_instance.total_donation_tokens += coupon_cost

			#Update total_hours_stub_instance for specific ngo and user
			try:
				total_hours_stub_instance   = total_hours_stub.objects.get(parent_ngo=ngo_instance, parent_volunteer=volunteer)
			except total_hours_stub.DoesNotExist:
				total_hours_stub_instance   = total_hours_stub.objects.create(parent_ngo=ngo_instance, parent_volunteer=volunteer)

			total_hours_stub_instance.total_donation_tokens   += coupon_cost			
			
			total_hours_stub_instance.save()
			total_support_stub_instance.save()

		transaction_stub_instance.save()
		business_agent.save()
		volunteer.save()
		return Response(data ={'error_message':'none', 'success':True})
			

class make_transaction_discount(APIView):
	def post(self, request):
		coupon_id       = request.data['coupon_id']
		

		#CHECK if coupon exists
		try:
			coupon_instance = coupon.objects.get(id=coupon_id, is_donation = False, is_active=True)
		except:
			return Response(data ={'error_message':'not discount', 'success':False})

		business_agent  = coupon_instance.parent_business
		coupon_cost     = coupon_instance.token_cost
		volunteer       = request.user
		volunteer_funds = volunteer.volunteer_token

		#CHECK if sufficient funds
		if (volunteer_funds <= coupon_cost):
			return Response(data = {'error_message':'insufficient funds', 'success':False})
		
		#Update Volunteer Funds
		volunteer_funds                = volunteer_funds - coupon_cost
		volunteer.volunteer_token      = volunteer_funds

		#Update Business Donation Tokens and Hours
		business_agent.discount_tokens += coupon_cost
		business_agent.total_hours     += coupon_cost*1.0/(EXCHANGE_TOKEN_HOUR)

		#Update Transaction Stub Instance
		transaction_stub_instance      = transaction_stub.objects.create(is_donation=False,tokens_transferred = coupon_cost, item_cost = coupon_instance.item_cost, parent_business =business_agent, parent_volunteer=volunteer)
		
		#Update relevant total_support_stub's
		total_hours_stub_set     = total_hours_stub.objects.filter(parent_volunteer=volunteer)
		for total_hours_stub_instance in total_hours_stub_set:
			ngo_instance         = total_hours_stub_instance.parent_ngo
			try:
				total_support_stub_instance = total_support_stub.objects.get(parent_business=business_agent, parent_ngo=ngo_instance)
			except total_support_stub.DoesNotExist:
				total_support_stub_instance = total_support_stub.objects.create(parent_business=business_agent, parent_ngo=ngo_instance)
			total_support_stub_instance.total_hours           += coupon_cost*1.0/(EXCHANGE_TOKEN_HOUR)
			total_support_stub_instance.total_discount_tokens += coupon_cost
			total_support_stub_instance.save()
		
		transaction_stub_instance.save()
		business_agent.save()
		volunteer.save()
		return Response(data ={'error_message':'none', 'success':True})
		
			

#----------------------------------------------------------------------------------------------------------------------------------------------------
