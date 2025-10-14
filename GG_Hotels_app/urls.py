from django.urls import path
from . import views
urlpatterns = [

    path('', views.homepage, name='homepage'),
    path('homepage/', views.homepage, name='homepage'),    
    path('sign_up/', views.user_sign_up, name='sign_up'),
    path('sign_in/', views.user_sign_in, name='sign_in'),
    path('logout/', views.user_logout, name='logout'),
    path('hotel_sign_up/', views.hotel_sign_up, name='hotel_sign_up'),
    path('hotel_sign_in/', views.hotel_sign_in, name='hotel_sign_in'),
    path('hotel_admin_panel/', views.hotel_admin_panel, name='hotel_admin_panel'),
    path('hotels_list/', views.hotels_list, name='hotels_list'),
    path('rooms_list/', views.rooms_list, name='rooms_list'),
    path('hotel/<int:hotel_id>/rooms/', views.hotel_rooms_list, name='hotel_rooms_list'),
    # path('sign_up/', views.UserSignUpView.as_view(), name='sign_up'),
    # path('sign_in/', views.UserSignInView.as_view(), name='sign_in'),


   
]
