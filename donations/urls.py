from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('donation/', views.donation_page, name='donation'),
    path('mpesa/callback/', views.mpesa_callback, name='mpesa_callback'),
]