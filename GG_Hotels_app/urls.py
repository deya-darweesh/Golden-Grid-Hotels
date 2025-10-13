from django.urls import path
from . import views
urlpatterns = [

    path('', views.homepage),
    path('homepage/', views.homepage, name='homepage'),    
    path('sign_up/', views.user_sign_up, name='sign_up'),
    path('sign_in/', views.user_sign_in, name='sign_in'),
    path('hotel_sign_up/', views.hotel_sign_up, name='hotel_sign_up'),
    path('hotel_sign_in/', views.hotel_sign_in, name='hotel_sign_in'),
    path('hotels_list/', views.hotels_list, name='hotels_list'),
    # path('hotel_rooms_list/', views.hotel_rooms_list, name='hotel_rooms_list'),




   
]
