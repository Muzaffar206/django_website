from django.shortcuts import render, redirect
from .models import Slider, AboutUs, SchemeData
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse
from allauth.account.views import SignupView, LoginView, LogoutView
from allauth.account.forms import SignupForm, LoginForm

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

class CustomLoginView(LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'You have successfully logged in.')
        return response

login = CustomLoginView.as_view()

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

class CustomSignupView(SignupView):
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.user.is_authenticated:
            messages.success(self.request, 'Your account has been created. Please check your email to verify your account.')
        return response

custom_signup_view = CustomSignupView.as_view()

class CustomLogoutView(LogoutView):
    def post(self, *args, **kwargs):
        response = super().post(*args, **kwargs)
        messages.success(self.request, 'You have been successfully logged out.')
        return response

custom_logout = CustomLogoutView.as_view()

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

