from django import forms
from django.shortcuts import render, redirect
from .models import Slider, AboutUs, SchemeData
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from allauth.account.utils import send_email_confirmation
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from allauth.account.views import SignupView
from allauth.account.forms import SignupForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model
import random
import logging

User = get_user_model()

logger = logging.getLogger(__name__)

def home(request):
    sliders = Slider.objects.all()
    about_us = AboutUs.objects.first()
    scheme_data = SchemeData.objects.first()
    return render(request, 'home.html', {
        'sliders': sliders,
        'about_us': about_us,
        'scheme_data': scheme_data,
    })

# About Pages
def about(request):
    return render(request, 'about/about.html')

def about_glance(request):
    return render(request, 'about/mesco_at_glance.html')

def managing_committee(request):
    return render(request, 'about/managing_committee.html')

def good_governance(request):
    return render(request, 'about/good_governance.html')

# Add similar views for the rest of the about, our work, and media pages
def mesco_education_society(request):
    return render(request, 'about/mesco_education_society.html')

def angels_paradise_nursery(request):
    return render(request, 'about/angels_paradise_nursery.html')

def vocational_training(request):
    return render(request, 'about/vocational_training.html')

def ecce(request):
    return render(request, 'about/ecce.html')

# Our Work Pages
def our_work(request):
    context = {
        'current_page': 'Our Work',
        'page_title': 'Our Projects',
    }
    return render(request, 'our_work.html', context)

def educational_support(request):
    return render(request, 'our_work/educational_support.html')

def medical_aid(request):
    return render(request, 'our_work/medical_aid.html')

def clinics_dispensaries(request):
    return render(request, 'our_work/clinics_dispensaries.html')

def school_adoption(request):
    return render(request, 'our_work/school_adoption.html')

def newspaper_units(request):
    return render(request, 'our_work/newspaper_units.html')

# Media Pages
def media(request):
    return render(request, 'media/media.html')

def in_media(request):
    return render(request, 'media/in_media.html')

def image_gallery(request):
    return render(request, 'media/image_gallery.html')

def video_gallery(request):
    return render(request, 'media/video_gallery.html')

def newsletters(request):
    return render(request, 'newsletters.html')

def annual_reports(request):
    return render(request, 'annual_reports.html')

def success_stories(request):
    return render(request, 'success_stories.html')

def donor_testimonials(request):
    return render(request, 'donor_testimonials.html')

# Contact, Login, Register, FAQ, Terms, etc.
def contact(request):
    return render(request, 'contact.html')

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')  # Replace 'home' with your home page URL name
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    context = {
        'form': form,
        'current_page': 'Login',
        'page_title': 'Login here',
    }
    return render(request, 'login.html', context)

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

class CustomSignupView(SignupView):
    form_class = CustomSignupForm
    template_name = 'account/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registration successful. Please check your email for verification.')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return response

def email_verification(request):
    if request.method == 'POST':
        entered_code = request.POST.get('verification_code')
        stored_code = request.session.get('verification_code')
        user_email = request.session.get('user_email')

        if entered_code == stored_code:
            user = User.objects.get(email=user_email)
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, 'Your account has been successfully verified. You are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid verification code. Please try again.')

    return render(request, 'account/email_verification.html')

@login_required
def profile(request):
    return render(request, 'profile.html')

def faq(request):
    return render(request, 'faq.html')

def terms_conditions(request):
    return render(request, 'terms_conditions.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def volunteer(request):
    return render(request, 'volunteer.html')

def donate(request):
    context = {
        'current_page': 'Donation',
        'page_title': 'Donate Now',
    }
    return render(request, 'donate.html', context)

def blog(request):
    return render(request, 'blog.html')

def custom_signup_view(request):
    # Your signup logic here
    # ...
    # Override the email sending function
    send_email_confirmation = lambda request, user, signup=False: None
    # ...

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')  # or any other URL you prefer

from django.shortcuts import render, redirect
from django.urls import reverse
from google_auth_oauthlib.flow import Flow
from django.conf import settings
from django.contrib import messages

# ... other imports and views ...

def oauth2callback(request):
    flow = Flow.from_client_secrets_file(
        settings.GMAIL_CREDENTIALS_FILE, settings.GMAIL_SCOPES)
    flow.redirect_uri = request.build_absolute_uri(reverse('oauth2callback'))

    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    with open(settings.GMAIL_TOKEN_FILE, 'wb') as token:
        pickle.dump(flow.credentials, token)

    return redirect('home')  # or wherever you want to redirect after authentication

def send_email_view(request):
    if request.method == 'POST':
        to = request.POST.get('to')
        subject = request.POST.get('subject')
        body = request.POST.get('body')

        service = get_gmail_service(request)
        if isinstance(service, redirect):
            return service  # This is a redirect to the OAuth flow

        if send_email(service, to, subject, body):
            messages.success(request, 'Email sent successfully!')
        else:
            messages.error(request, 'Failed to send email.')

    return render(request, 'send_email.html')

def register(request):
    if request.method == 'POST':
        # Your existing registration logic here
        # ...

        # Remove email verification code
        user = User.objects.create_user(username, email, password)
        user.save()

        return redirect('login')

    return render(request, 'account/register.html')