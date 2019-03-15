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


from django.http import Http404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from NGO.models   import event, org, event_registration_stub
from BUSINESS.models import business, coupon, transaction_stub
from users.models import CustomUser
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

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
		return event.objects.filter(id__in=event_ids)
		

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


class is_verified_donation(APIView):
	def get(self, request, **kwargs):
		coupon_id       = kwargs['coupon_id']
		pin_try         = kwargs['pin_try']
		try:
			coupon_instance = coupon.objects.get(id=coupon_id, is_donation = True, is_active=True)
		except:
			return Response(data ={'error_message':'not donation', 'success':False})
		business_agent  = coupon_instance.parent_business
		correct_pin     = business_agent.pin
		if (correct_pin == pin_try):
			return Response(data ={'error_message':'none', 'success':True})
		else:
			return Response(data ={'error_message':'wrong pin', 'success':False})


class make_transcation_donation(APIView):
	def post(self, request):
		coupon_id       = request.data['coupon_id']
		try:
			coupon_instance = coupon.objects.get(id=coupon_id, is_donation = True, is_active=True)
		except:
			return Response(data ={'error_message':'not donation', 'success':False})

		business_agent  = coupon_instance.parent_business
		coupon_cost     = coupon_instance.token_cost
		volunteer       = request.user
		volunteer_funds = volunteer.volunteer_token

		if (volunteer_funds >= coupon_cost):
			volunteer_funds                = volunteer_funds - coupon_cost
			volunteer.volunteer_token      = volunteer_funds
			business_agent.donation_tokens += coupon_cost
			stub = transaction_stub.objects.create(is_donation=True,tokens_transferred = coupon_cost, parent_business =business_agent, parent_volunteer=volunteer)
			stub.save()
			business_agent.save()
			volunteer.save()
			return Response(data ={'error_message':'none', 'success':True})
		else:
			return Response(data = {'error message':'insufficient funds', 'success':False})

class make_transcation_discount(APIView):
	def post(self, request):
		coupon_id       = request.data['coupon_id']
		try:
			coupon_instance = coupon.objects.get(id=coupon_id, is_donation = False, is_active=True)
		except:
			return Response(data ={'error_message':'not donation', 'success':False})

		business_agent  = coupon_instance.parent_business
		coupon_cost     = coupon_instance.token_cost
		volunteer       = request.user
		volunteer_funds = volunteer.volunteer_token

		if (volunteer_funds >= coupon_cost):
			volunteer_funds                = volunteer_funds - coupon_cost
			volunteer.volunteer_token      = volunteer_funds
			business_agent.discount_tokens += coupon_cost
			stub = transaction_stub.objects.create(is_donation=False,tokens_transferred = coupon_cost, parent_business =business_agent, parent_volunteer=volunteer)
			stub.save()
			business_agent.save()
			volunteer.save()
			return Response(data ={'error_message':'none', 'success':True})
		else:
			return Response(data = {'error message':'insufficient funds', 'success':False})

#----------------------------------------------------------------------------------------------------------------------------------------------------
