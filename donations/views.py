from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'donations/index.html')

def donation_page(request):
    return render(request, 'donations/donation.html')