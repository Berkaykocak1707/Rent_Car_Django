from datetime import date
from django.db import models
from django.utils.text import slugify
import os
import random
from django.core.exceptions import ValidationError

def upload_to(instance, filename):
    ext = os.path.splitext(filename)[1]
    new_filename = f"{instance.slug}_{random.randint(1, 1000000)}{ext}"
    return os.path.join('cars', new_filename)

class City(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(City, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    photo = models.ImageField(upload_to=upload_to)
    doors = models.PositiveIntegerField()
    seats = models.PositiveIntegerField()
    transmission = models.CharField(choices=TRANSMISSION_CHOICES, max_length=10)
    year = models.PositiveIntegerField()
    price_per_day = models.DecimalField(max_digits=7, decimal_places=2)
    is_active = models.BooleanField(default=True)
    available_date = models.DateField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def clean(self):
        # available_date'in bugünden önce olup olmadığını kontrol ediyoruz.
        if self.available_date < date.today():
            raise ValidationError('The date he is available cannot be before today.')

    def save(self, *args, **kwargs):
        self.clean()  # Modeli doğrula
        if not self.slug:
            self.slug = slugify(self.name)
        if self.photo and not hasattr(self.photo, 'url'):
            self.photo.name = upload_to(self, self.photo.name)
        super(Car, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Booking(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    rented_car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="bookings")
    rental_city = models.ForeignKey(City, on_delete=models.SET_NULL, related_name="rental_bookings", null=True)
    dropoff_city = models.ForeignKey(City, on_delete=models.SET_NULL, related_name="dropoff_bookings", null=True)
    rental_start_date = models.DateField()
    rental_end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_approved = models.BooleanField(default=False)

    def clean(self):
        if self.rental_start_date < self.rented_car.available_date:
            raise ValidationError('The rental start date cannot be earlier than the date the car was registered.')

    def save(self, *args, **kwargs):
        self.clean()
        if self.is_approved:
            self.rented_car.city = self.dropoff_city
            self.rented_car.available_date = self.rental_end_date
            self.rented_car.save()
        super(Booking, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.rented_car.name}"
