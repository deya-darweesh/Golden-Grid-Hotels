from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Room, Service, Booking, Booking_Service
from django.contrib.auth.models import User
from .forms import UserSignInForm, CustomUserSignUpForm, CustomHotelSignUpForm, HotelSignInForm, RoomForm, ServiceForm, BookingForm, UserProfileForm, BookingEditForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime




def homepage(request):
    hotels = User.objects.filter(is_staff=True)
    featured_rooms = Room.objects.all()[:6]
    return render(request, 'homepage.html', {'hotels': hotels, 'featured_rooms': featured_rooms})


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


@login_required
def create_booking(request, room_id):
    if request.user.is_staff:
        messages.error(request, "Hotels cannot make bookings. Please use a customer account.")
        return redirect('homepage')
    
    room = get_object_or_404(Room, id=room_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST, room=room)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer_id = request.user
            booking.room_id = room
            
            check_in = form.cleaned_data['check_in_date']
            check_out = form.cleaned_data['check_out_date']
            nights = (check_out - check_in).days
            
            total_price = room.price_per_night * nights
            
            services = form.cleaned_data['services']
            for service in services:
                total_price += service.price
            
            booking.total_price = total_price
            booking.save()
            
            for service in services:
                Booking_Service.objects.create(
                    booking=booking,
                    service=service,
                    quantity=1
                )
            
            messages.success(request, f"Booking confirmed! Total price: ${total_price}")
            return redirect('homepage')
    else:
        form = BookingForm(room=room)
    
    services = Service.objects.filter(available=True)
    context = {
        'form': form,
        'room': room,
        'services': services,
    }
    
    return render(request, 'booking/booking_form.html', context)


@login_required
def user_profile(request):
    if request.user.is_staff:
        messages.error(request, "Hotels should use the admin panel instead.")
        return redirect('hotel_admin_panel')
    
    if request.method == 'POST':
        if 'delete_account' in request.POST:
            user = request.user
            logout(request)
            user.delete()
            messages.success(request, "Your account has been deleted successfully.")
            return redirect('homepage')
        else:
            form = UserProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, "Your profile has been updated successfully.")
                return redirect('user_profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    bookings = Booking.objects.filter(customer_id=request.user).order_by('-check_in_date')
    
    return render(request, 'users/user-panel.html', {
        'form': form,
        'bookings': bookings
    })


@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer_id=request.user)
    
    if request.method == 'POST':
        form = BookingEditForm(request.POST, instance=booking)
        if form.is_valid():
            updated_booking = form.save(commit=False)
            
            check_in = form.cleaned_data['check_in_date']
            check_out = form.cleaned_data['check_out_date']
            nights = (check_out - check_in).days
            
            total_price = booking.room_id.price_per_night * nights
            
            services = form.cleaned_data['services']
            for service in services:
                total_price += service.price
            
            updated_booking.total_price = total_price
            updated_booking.save()
            
            booking.booking_services.all().delete()
            
            for service in services:
                Booking_Service.objects.create(
                    booking=updated_booking,
                    service=service,
                    quantity=1
                )
            
            messages.success(request, "Booking updated successfully.")
            return redirect('user_profile')
    else:
        form = BookingEditForm(instance=booking)
    
    return render(request, 'users/edit-booking.html', {'form': form, 'booking': booking})


@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer_id=request.user)
    
    if request.method == 'POST':
        booking.delete()
        messages.success(request, "Booking deleted successfully.")
        return redirect('user_profile')
    
    return render(request, 'users/delete-booking.html', {'booking': booking})
