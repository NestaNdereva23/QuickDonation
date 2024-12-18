from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('donation/', views.donation_page, name='donation'),
]