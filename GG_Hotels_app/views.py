from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Room, Service, Booking, Booking_Service
from django.contrib.auth.models import User
# later forms will imported


# Create your views here.


def homepage(request):
    
    return render(request, 'homepage.html')


def user_sign_up(request):
    
    return render(request, 'users/user_sign_up.html')


def user_sign_in(request):
    
    return render(request, 'users/user_sign_in.html')


def hotel_sign_up(request):
    
    return render(request, 'hotels/hotel_sign_up.html')


def hotel_sign_in(request):
    
    return render(request, 'hotels/hotel_sign_in.html')


def hotels_list(request):
    
    return render(request, 'gg_pages/hotels_list.html')


# def rooms_list(request):
#     pass
#     return render(request, 'homepage.html')


# def hotel_rooms_list(request):
#     pass
#     return render(request, 'gg_pages/hotel_rooms_list.html')

