from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date

class Room(models.Model):
    id = models.AutoField(primary_key=True)
    hotel_id = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='hotel_rooms', null=True)
    room_type = models.CharField(max_length=20, null=False)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    capacity = models.IntegerField(null=False)
    description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(null=False, default=1)

    def __str__(self):
        return f"Room: {self.room_type} - Hotel: {self.hotel_id}"


class Service(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=False, default=0)
    description = models.TextField(blank=True, null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id =models.ForeignKey(User, on_delete=models.SET_NULL, related_name='customer_bookings', null=True)
    room_id = models.ForeignKey(Room, on_delete=models.SET_NULL, related_name='room_bookings', null=True)
    check_in_date = models.DateField(null=False)
    check_out_date = models.DateField(null=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f"Booking: {self.id} - Customer: {self.customer_id}"


class Booking_Service(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, related_name='booking_services', null=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, related_name='service_requests', null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"Service: {self.service.name} x{self.quantity} for: (Booking {self.booking.id})"

