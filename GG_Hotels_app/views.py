from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Room, Service, Booking, Booking_Service
from django.contrib.auth.models import User
from .forms import UserSignInForm, CustomUserSignUpForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate, logout
# Create your views here.




def homepage(request):
    hotels = User.objects.filter(is_staff=True)
    return render(request, 'homepage.html', {'hotels': hotels})


def user_sign_up(request):
    error_message = ''
    if request.method == 'POST':
        form = CustomUserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('homepage'))
        else:
            error_message = 'Invalid sign-up - try again'
    
    form = CustomUserSignUpForm()
    return render(request, 'users/user_sign_up.html', {
        'form': form, 
        'error_message': error_message
    })


def user_sign_in(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            auth_user = authenticate(request, username=user.username, password=password)
            if auth_user:
                login(request, auth_user)
                return redirect(reverse('homepage'))
            else:
                error = 'Invalid email or password.'
                form = UserSignInForm()
                return render(request, 'users/user_sign_in.html', {'form': form, 'error': error})
        except User.DoesNotExist:
            error = 'Email does not exist.'
            form = UserSignInForm()
            return render(request, 'users/user_sign_in.html', {'form': form, 'error': error})
    else:
        form = UserSignInForm()
        return render(request, 'users/user_sign_in.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect(reverse('homepage'))


def hotel_sign_up(request):
    
    return render(request, 'hotels/hotel_sign_up.html')


def hotel_sign_in(request):
    
    return render(request, 'hotels/hotel_sign_in.html')


def hotels_list(request):
    hotels = User.objects.filter(is_staff=True)
    return render(request, 'gg_pages/hotels_list.html', {'hotels': hotels})


def rooms_list(request):
    rooms = Room.objects.all()
    return render(request, 'gg_pages/rooms_list.html', {'rooms': rooms})


def hotel_rooms_list(request, hotel_id):
    hotel = User.objects.get(id=hotel_id)
    rooms = Room.objects.filter(hotel_id=hotel_id)
    return render(request, 'gg_pages/hotel_rooms_list.html', {'rooms': rooms, 'hotel': hotel})
