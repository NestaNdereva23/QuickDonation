from django import forms
from .models import Donation, Organizations

class DonationForm(forms.ModelForm):
    phone_number = forms.CharField(
        label='Phone Number',
        help_text='Enter your Mpesa-registered phone number'
    )
    amount = forms.DecimalField(label='Donation Amount', min_value=1)
    organization = forms.ModelChoiceField(
        queryset=Organizations.objects.all(),
        label="Select Organization",
        empty_label="Choose an organization",
        help_text="Select the organization you want to donate to",
    )

    class Meta:
        model = Donation
        fields = ['phone_number', 'amount', 'organization']
