from django import forms
from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

from django import forms
from .models import Donor, Donation

class DonationForm(forms.Form):
    surname = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    middle_name = forms.CharField(max_length=100, required=False)
    pan_no = forms.CharField(max_length=10)
    email = forms.EmailField()
    mobile = forms.CharField(max_length=15)
    dofficial = forms.CharField(max_length=100, required=False)
    address = forms.CharField(widget=forms.Textarea)
    city = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    pincode = forms.CharField(max_length=10)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    purpose = forms.CharField(max_length=200)
    is_zakat = forms.BooleanField(required=False)
    notes = forms.CharField(widget=forms.Textarea, required=False)