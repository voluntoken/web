# users/views.py
from django.urls import reverse_lazy
from django.views import generic
from .models import CustomUser
from .forms import CustomUserCreationForm_Volunteer, CustomUserCreationForm_NGO, CustomUserCreationForm_Business

#Additional Email Confirmation Stuff
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

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