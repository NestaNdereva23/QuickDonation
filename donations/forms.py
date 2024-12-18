from django import forms
from . models import Donation

class DonationForm(forms.ModelForm):
    phone_number = forms.CharField(
        label='Phone Number', 
        help_text='Enter your Mpesa-registered phone number'
    )
    amount = forms.DecimalField(label='Donation Amount', min_value=1)

    class Meta:
        model = Donation
        fields = ['phone_number', 'amount']