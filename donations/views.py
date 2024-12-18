from django.shortcuts import render, redirect
from .models import Organizations
from .forms import DonationForm
from django.contrib import messages
from mpesa_integration.mpesa_client import MpesaClient
import json
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)
# Create your views here.
def home(request):
    return render(request, 'donations/index.html')

def donation_page(request):

    #get all organizations
    orgs = Organizations.objects.all()

    #handle the donation form
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            #Normalize phone number
            phone_number = form.cleaned_data['phone_number']
            if phone_number.startswith('0'):
                phone_number = '254' + phone_number[1:]
            elif not phone_number.startswith('254'):
                messages.error(request, 'Invalid phone no format')
                return redirect('donation')

            amount = form.cleaned_data['amount']

            #create donation record
            donation = form.save(commit=False)
            donation.save()

            #initiate mpesa STK push
            mpesa_client = MpesaClient()
            try:
                mpesa_response = mpesa_client.initiate_stk_push(phone_number, int(amount))
                logger.info(f"Mpesa Response: {mpesa_response}")

                if mpesa_response and mpesa_response.get('ResponseCode') == '0':
                    donation.status = 'Processing'
                    messages.success(request, 'Donation request sent! Check your phone.')
                else:
                    donation.status = 'Failed'
                    messages.error(request, 'Failed to process donation. Please try again.')
            except Exception as e:
                logger.error(f"Error initiating Mpesa STK Push: {str(e)}")
                donation.status = 'Failed'
                messages.error(request, 'An error occurred. Please try again.')

            donation.save()
            return redirect('donation')
    else:
        form = DonationForm()

    return render(request, 'donations/donation.html', {"orgs":orgs, "form":form})

"""
    handle the callback url
"""
def mpesa_callback(request):
    if request.method =='POST':
        callback_data = json.loads(request.body)

        #process the callback data
        print("Callback Data:", callback_data)

        #Return a success response to Saf
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
    return JsonResponse({"ResultCode": 1, "ResultDesc": "Invalid Request"}, status=400)