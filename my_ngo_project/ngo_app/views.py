from django.shortcuts import render, redirect
from .models import Slider, AboutUs, SchemeData, Donor, Donation
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse
from allauth.account.views import SignupView, LoginView, LogoutView, PasswordResetView
from allauth.account.forms import SignupForm, LoginForm
from allauth.account.views import EmailVerificationSentView
from django.contrib.auth.decorators import login_required
from .forms import DonationForm
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.models import User


import logging

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

def blog(request):
    return render(request, 'blog/blog.html')

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['scope'] = ['profile', 'email']
        context['auth_params'] = {'access_type': 'online'}
        return context

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
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            try:
                # Create donor
                donor = Donor.objects.create(
                    surname=form.cleaned_data['surname'],
                    first_name=form.cleaned_data['first_name'],
                    middle_name=form.cleaned_data['middle_name'],
                    pan_no=form.cleaned_data['pan_no'],
                    email=form.cleaned_data['email'],
                    mobile=form.cleaned_data['mobile'],
                    dofficial=form.cleaned_data['dofficial'],
                    address=form.cleaned_data['address'],
                    city=form.cleaned_data['city'],
                    country=form.cleaned_data['country'],
                    state=form.cleaned_data['state'],
                    pincode=form.cleaned_data['pincode'],
                )

                # Create donation
                donation = Donation.objects.create(
                    donor=donor,
                    amount=form.cleaned_data['amount'],
                    purpose=form.cleaned_data['purpose'],
                    is_zakat=request.POST.get('is_zakat') == 'Yes',
                    notes=form.cleaned_data['notes'],
                )

                # Create Razorpay Order
                razorpay_order = razorpay_client.order.create(dict(
                    amount=int(donation.amount * 100),
                    currency='INR',
                    payment_capture='0'
                ))

                # Update donation with Razorpay order_id
                donation.razorpay_order_id = razorpay_order['id']
                donation.save()

                context = {
                    'form': form,
                    'razorpay_order_id': razorpay_order['id'],
                    'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
                    'razorpay_amount': int(donation.amount * 100),
                    'currency': 'INR',
                    'callback_url': 'http://' + request.get_host() + '/razorpay-callback/'
                }
                return render(request, 'donate.html', context)
            except Exception as e:
                print(f"Error processing donation: {str(e)}")
                messages.error(request, 'An error occurred while processing your donation. Please try again.')
        else:
            print(form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = DonationForm()
    
    context = {
        'form': form,
        'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
    }
    return render(request, 'donate.html', context)



def donation_success(request):
    return render(request, 'donation_success.html')

def donation_failure(request):
    return render(request, 'donation_failure.html')

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

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from allauth.account.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

@method_decorator(csrf_protect, name='dispatch')
class CustomPasswordResetView(PasswordResetView):
    def get_users(self, email):
        """Return the users with the given email address."""
        User = get_user_model()
        return User.objects.filter(email__iexact=email, is_active=True)

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        users = self.get_users(email)
        
        if not users.exists():
            return JsonResponse({
                'status': 'error',
                'message': "Email doesn't exist.",
            })

        # Send the password reset email
        form.save(request=self.request)

        return JsonResponse({
            'status': 'success',
            'message': "Password reset e-mail has been sent successfully.",
        })

    def form_invalid(self, form):
        errors = form.errors.as_text()
        return JsonResponse({
            'status': 'error',
            'message': errors,
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.request.GET.get('email', '')  # Get email from query params
        return context

class CustomConfirmEmailView(EmailVerificationSentView):
    template_name = 'account/verification_sent.html'

from django.http import JsonResponse
from .models import Donor
from django.db.models import Q

def donor_data_api(request):
    identifier = request.GET.get('identifier')
    donor = Donor.objects.filter(Q(email=identifier) | Q(mobile=identifier)).first()
    
    if donor:
        return JsonResponse({
            'success': True,
            'donor': {
                'surname': donor.surname,
                'firstName': donor.first_name,
                'middleName': donor.middle_name,
                'panNo': donor.pan_no if request.user.is_authenticated else None,
                'email': donor.email,
                'mobile': donor.mobile,
                'dofficial': donor.dofficial,
                'address': donor.address,
                'city': donor.city,
                'country': donor.country,
                'state': donor.state,
                'pincode': donor.pincode
            },
            'isAuthenticated': request.user.is_authenticated
        })
    else:
        return JsonResponse({'success': False})

def donate_view(request):
    return render(request, 'donate.html')

@login_required
def user_donations(request):
    donations = Donation.objects.filter(donor__user=request.user).order_by('-created_at')
    return render(request, 'user_donations.html', {'donations': donations})
