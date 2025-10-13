from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Room, Service, Booking, Booking_Service
from django.contrib.auth.models import User
from .forms import UserSignUpForm, UserSignInForm

# Create your views here.


def homepage(request):
    
    return render(request, 'homepage.html')


def user_sign_up(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(reverse('homepage'))
        else:
            return render(request, 'users/user_sign_up.html', {'form': form})
    elif request.method == 'GET':
        form = UserSignUpForm()
        return render(request, 'users/user_sign_up.html', {'form': form})


def user_sign_in(request):
    if request.method == 'POST':
        form = UserSignInForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                user = User.objects.get(email=email)
                if user.password == password:
                    return redirect(reverse('homepage'))
                else:
                    form.add_error('email', 'Invalid email or password.')
            except User.DoesNotExist:
                form.add_error('email', 'Email does not exist.')
        return render(request, 'users/user_sign_in.html', {'form': form})
    else:
        form = UserSignInForm()
        return render(request, 'users/user_sign_in.html', {'form': form})


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

