# users/views.py
from django.urls import reverse_lazy
from django.views import generic
from .models import CustomUser
from .forms import CustomUserCreationForm_Volunteer, CustomUserCreationForm_NGO, CustomUserCreationForm_Business
from .forms import CustomUserChangeForm_Volunteer, CustomUserChangeForm_NGO, CustomUserChangeForm_Business

#Additional Email Confirmation Stuff
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from django.views import View


#HOME PAGE
#----------------------------------------------------------------------------------------------------------------------------------------------------
class View_Stats(View):
    template_name = 'User_stats.html'
    

#----------------------------------------------------------------------------------------------------------------------------------------------------

#HOME PAGE
#----------------------------------------------------------------------------------------------------------------------------------------------------
def home_page(request):
    context = {}
    # print("Redirecting to right page!")

    if request.user.is_authenticated:
        if request.user.user_type == "VO":
            #volunteer 
            #load events 
            print("Volunteer")
            return render(request, 'volunteer_home.html', context)
        elif request.user.user_type == "NG":
            #NGO
            #load NGO events
            print("NGO")
            return render(request, 'NGO_home.html', context)
        elif request.user.user_type == "BU":
            #Business
            #load Business coupons 
            print("Business")
            return render(request, 'business_home.html', context)
        else :
            #should not happen unless admin made user
            print("SuperUser")
            return render(request, 'home.html', context)
    
    print("Not logged in")        
    return render(request, 'home.html', context)
#----------------------------------------------------------------------------------------------------------------------------------------------------

#SETTINGS
#----------------------------------------------------------------------------------------------------------------------------------------------------
class Modify_Volunteer(View):
    form_class = CustomUserChangeForm_Volunteer
    success_url = reverse_lazy('home')
    template_name = 'settings.html'
    
    def get(self, request, *args, **kwargs):
        if(request.user.user_type != 'VO'):
            return HttpResponseNotFound('<h1>Page not found</h1>')
        print(request.user.username)
        user = request.user
        form = self.form_class(instance=user)
        return render(request, self.template_name, {'form': form})
        
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # <process form cleaned data>
            return render(request, 'volunteer_home.html', {})

        return render(request, self.template_name, {'form': form})
        
class Modify_NGO(View):
    form_class = CustomUserChangeForm_NGO
    success_url = reverse_lazy('home')
    template_name = 'settings.html'
    
    def get(self, request, *args, **kwargs):
        if(request.user.user_type != 'NG'):
            return HttpResponseNotFound('<h1>Page not found</h1>')
        print(request.user.username)
        user = request.user
        form = self.form_class(instance=user)
        return render(request, self.template_name, {'form': form})
        
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # <process form cleaned data>
            return render(request, 'NGO_home.html', {})

        return render(request, self.template_name, {'form': form})
        
        
class Modify_Business(View):
    form_class = CustomUserChangeForm_Business
    success_url = reverse_lazy('home')
    template_name = 'settings.html'
    
    def get(self, request, *args, **kwargs):
        if(request.user.user_type != 'BU'):
            return HttpResponseNotFound('<h1>Page not found</h1>')
        print(request.user.username)
        user = request.user
        form = self.form_class(instance=user)
        return render(request, self.template_name, {'form': form})
        
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # <process form cleaned data>
            return render(request, 'business_home.html', {})

        return render(request, self.template_name, {'form': form})
#----------------------------------------------------------------------------------------------------------------------------------------------------        
        


#SIGN UP
#----------------------------------------------------------------------------------------------------------------------------------------------------
class SignUp_Volunteer(generic.CreateView):
    form_class = CustomUserCreationForm_Volunteer
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    
class SignUp_NGO(generic.CreateView):
    form_class = CustomUserCreationForm_NGO
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    
class SignUp_Business(generic.CreateView):
    form_class = CustomUserCreationForm_Business
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
#----------------------------------------------------------------------------------------------------------------------------------------------------

# def signuprequest(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False #only make this true after confirmation
#             user.save()
#             current_site = get_current_site(request)
#             mail_subject = 'Activate your blog account.'
#             message = render_to_string('acc_active_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
#                 'token':account_activation_token.make_token(user),
#             })
#             to_email = form.cleaned_data.get('email')
#             email = EmailMessage(
#                         mail_subject, message, to=[to_email]
#             )
#             email.send()
#             return HttpResponse('Please confirm your email address to complete the registration')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'signup.html', {'form': form})

# def activate(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = CustomUser.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         # return redirect('home')
#         return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
#     else:
#         return HttpResponse('Activation link is invalid!')