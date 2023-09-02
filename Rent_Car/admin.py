from django.contrib import admin
from .models import City, Car, Booking

class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

class CarAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'year', 'transmission', 'price_per_day', 'is_active', 'available_date', 'city']
    list_filter = ['transmission', 'year', 'is_active', 'city']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class BookingAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'rented_car', 'rental_city', 'dropoff_city', 'rental_start_date', 'rental_end_date', 'is_approved']
    list_filter = ['is_approved', 'rental_city', 'dropoff_city']
    search_fields = ['first_name', 'last_name', 'email']

admin.site.register(City, CityAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Booking, BookingAdmin)
