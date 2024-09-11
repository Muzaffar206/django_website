from django.shortcuts import render
from .models import Slider, AboutUs, SchemeData

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
        # ... other context data ...
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
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

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