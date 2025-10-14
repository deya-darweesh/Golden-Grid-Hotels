from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Room, Service, Booking, Booking_Service
from django.contrib.auth.models import User
from .forms import UserSignInForm, CustomUserSignUpForm, CustomHotelSignUpForm, HotelSignInForm, RoomForm, ServiceForm
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
    error_message = ''
    if request.method == 'POST':
        form = CustomHotelSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('hotel_admin_panel')
        else:
            error_message = 'Invalid sign-up - try again'
    
    form = CustomHotelSignUpForm()
    return render(request, 'hotels/hotel_sign_up.html', {
        'form': form, 
        'error_message': error_message
    })


def hotel_sign_in(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email, is_staff=True)
            auth_user = authenticate(request, username=user.username, password=password)
            if auth_user:
                login(request, auth_user)
                return redirect('hotel_admin_panel')
            else:
                error = 'Invalid email or password.'
                form = HotelSignInForm()
                return render(request, 'hotels/hotel_sign_in.html', {'form': form, 'error': error})
        except User.DoesNotExist:
            error = 'Hotel email does not exist.'
            form = HotelSignInForm()
            return render(request, 'hotels/hotel_sign_in.html', {'form': form, 'error': error})
    else:
        form = HotelSignInForm()
        return render(request, 'hotels/hotel_sign_in.html', {'form': form})


def hotel_admin_panel(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('hotel_sign_in')
    
    hotel_rooms = Room.objects.filter(hotel_id=request.user)
    services = Service.objects.all()
    return render(request, 'hotels/full_hotel_panel.html', {'hotel_rooms': hotel_rooms, 'services': services})


def add_room(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('hotel_sign_in')
    
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.hotel_id = request.user
            room.save()
            return redirect('hotel_admin_panel')
    else:
        form = RoomForm()
    
    return render(request, 'hotels/add_room.html', {'form': form})


def edit_room(request, room_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('hotel_sign_in')
    
    room = Room.objects.get(id=room_id, hotel_id=request.user)
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('hotel_admin_panel')
    else:
        form = RoomForm(instance=room)
    
    return render(request, 'hotels/edit_room.html', {'form': form, 'room': room})


def delete_room(request, room_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('hotel_sign_in')
    
    room = Room.objects.get(id=room_id, hotel_id=request.user)
    room.delete()
    return redirect('hotel_admin_panel')


def add_service(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('hotel_sign_in')
    
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hotel_admin_panel')
    else:
        form = ServiceForm()
    
    return render(request, 'hotels/add_service.html', {'form': form})


def edit_service(request, service_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('hotel_sign_in')
    
    service = Service.objects.get(id=service_id)
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('hotel_admin_panel')
    else:
        form = ServiceForm(instance=service)
    
    return render(request, 'hotels/edit_service.html', {'form': form, 'service': service})


def delete_service(request, service_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('hotel_sign_in')
    
    service = Service.objects.get(id=service_id)
    service.delete()
    return redirect('hotel_admin_panel')


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
