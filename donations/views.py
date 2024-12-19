from django.shortcuts import render, redirect
from .models import Organizations, Donation
from .forms import DonationForm
from django.contrib import messages
from mpesa_integration.mpesa_client import MpesaClient
import json
from django.http import JsonResponse
import logging
from time import sleep

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

            organization_id = request.POST.get('organization')  # Get selected organization ID

            # Fetch the organization
            try:
                organization = Organizations.objects.get(id=organization_id)
            except Organizations.DoesNotExist:
                messages.error(request, 'Invalid organization selected.')
                return redirect('donation')
            
            #create donation record
            donation = form.save(commit=False)
            donation.phone_number = phone_number
            donation.amount = amount
            donation.organization = organization  # Associate organization
            donation.save()

            #initiate mpesa STK push
            mpesa_client = MpesaClient()
            try:
                mpesa_response = mpesa_client.initiate_stk_push(phone_number, int(amount))
                logger.info(f"Mpesa Response: {mpesa_response}")

                if mpesa_response and mpesa_response.get('ResponseCode') == '0':
                    donation.status = 'Processing'
                    messages.success(request, 'Donation request sent! Check your phone.')
                    return render(request, 'donations/donation.html', {"donation_id": donation.id, "orgs": orgs, "form": form})
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
    if request.method == 'POST':
        callback_data = json.loads(request.body)

        # Update donation record
        result_code = callback_data.get('Body', {}).get('stkCallback', {}).get('ResultCode')
        receipt_number = callback_data.get('Body', {}).get('stkCallback', {}).get('CallbackMetadata', {}).get('Item', [])

        donation_id = ...  # Extract from callback_data or store it during the STK push
        donation = Donation.objects.filter(id=donation_id).first()

        if donation:
            if result_code == 0:
                donation.status = 'Success'
                donation.receipt_number = receipt_number
            else:
                donation.status = 'Failed'
            donation.save()

        return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
    return JsonResponse({"ResultCode": 1, "ResultDesc": "Invalid Request"}, status=400)

def check_status(request, donation_id):
    timeout = 60
    interval = 5

    for _ in range(0, timeout, interval):
        donation = Donation.objects.filter(id=donation_id).first()
        if donation and donation.status in ['Success', 'Failed']:
            return JsonResponse({"status": donation.status})
        
        sleep(interval)

        return JsonResponse({"status": "Timeout"})