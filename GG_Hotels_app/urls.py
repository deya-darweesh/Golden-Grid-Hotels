from django.urls import path
from . import views
urlpatterns = [

    path('', views.homepage, name='homepage'),
    path('homepage/', views.homepage, name='homepage'),
    path('about_us/', views.about_us, name='about_us'),
    path('sign_up/', views.user_sign_up, name='sign_up'),
    path('sign_in/', views.user_sign_in, name='sign_in'),
    path('logout/', views.user_logout, name='logout'),
    path('hotel_sign_up/', views.hotel_sign_up, name='hotel_sign_up'),
    path('hotel_sign_in/', views.hotel_sign_in, name='hotel_sign_in'),
    path('hotel_admin_panel/', views.hotel_admin_panel, name='hotel_admin_panel'),
    path('add_room/', views.add_room, name='add_room'),
    path('edit_room/<int:room_id>/', views.edit_room, name='edit_room'),
    path('delete_room/<int:room_id>/', views.delete_room, name='delete_room'),
    path('add_service/', views.add_service, name='add_service'),
    path('edit_service/<int:service_id>/', views.edit_service, name='edit_service'),
    path('delete_service/<int:service_id>/', views.delete_service, name='delete_service'),
    path('hotels_list/', views.hotels_list, name='hotels_list'),
    path('rooms_list/', views.rooms_list, name='rooms_list'),
    path('hotel/<int:hotel_id>/rooms/', views.hotel_rooms_list, name='hotel_rooms_list'),
    path('book_room/<int:room_id>/', views.create_booking, name='create_booking'),
    path('profile/', views.user_profile, name='user_profile'),
    path('edit_booking/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('delete_booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
]
