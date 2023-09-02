from datetime import date
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Booking, Car, City
from django.core.exceptions import ValidationError
from django.contrib import messages
from datetime import datetime


def index(request):
    if request.method == 'POST':
        selected_city_id = request.POST.get('city')
        journey_date = request.POST.get('journey_date')

        if selected_city_id == "all":
            cars = Car.objects.filter(available_date__lte=journey_date)
        else:
            cars = Car.objects.filter(city__id=selected_city_id, available_date__lte=journey_date) 

        return render(request, 'cars_city_date.html', {'cars': cars})
    else:
        # Veritabanından rastgele 5 araba seçiyoruz
        random_cars = Car.objects.order_by('?')[:5]
        
        # Bütün şehirleri alıyoruz
        all_cities = City.objects.all()
        
        # Template'e arabaları ve şehirleri gönderiyoruz
        context = {
           'today': date.today(),
            'cars': random_cars,
            'cities': all_cities
        }
        
        return render(request, 'index.html', context)



def services(request):
 return render(request, 'services.html')

def cars(request):
    car_list = Car.objects.all()

    if car_list.count() <= 6:
            return render(request, 'cars.html', {'cars': car_list})

    paginator = Paginator(car_list, 6)

    page = request.GET.get('page')
    cars = paginator.get_page(page)

    return render(request, 'cars.html', {'cars': cars})

from django.shortcuts import render, redirect
from .models import Car, City


def about(request):
 return render(request, 'about.html')

def rent(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        rented_car_id = request.POST.get('RentedCar')
        rental_city_id = request.POST.get('Rentalcity')
        dropoff_city_id = request.POST.get('Dropoffcity')
        rental_start_date_str = request.POST.get('start_date')
        rental_end_date_str  = request.POST.get('return_date')
        total_price_from_form = request.POST.get('total_price')

        # Dizeleri datetime.date formatına dönüştür
        rental_start_date = datetime.strptime(rental_start_date_str, "%Y-%m-%d").date()
        rental_end_date = datetime.strptime(rental_end_date_str, "%Y-%m-%d").date()

        rented_car = Car.objects.get(id=rented_car_id)

        rental_city = City.objects.filter(id=rental_city_id).first()
        if not rental_city:
            # Uygun bir hata mesajı göster
            messages.error(request, "Invalid rental city selected!")
            return redirect('rent')

        dropoff_city = City.objects.filter(id=dropoff_city_id).first()
        if not dropoff_city:
            # Uygun bir hata mesajı göster
            messages.error(request, "Invalid dropoff city selected!")
            return redirect('rent')

        booking = Booking(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            rented_car=rented_car,
            rental_city=rental_city,
            dropoff_city=dropoff_city,
            rental_start_date=rental_start_date,
            rental_end_date=rental_end_date,
            total_price=total_price_from_form
        )

        try:
            booking.save()
            messages.success(request, "Thank you! Your booking has been successfully registered.")
        except ValidationError as e:
            messages.error(request, e.message)
            return render(request, 'rent.html')

        # Kullanıcıyı başka bir sayfaya yönlendirebiliriz, örneğin teşekkür sayfasına
        return render(request, 'rent.html')
    else:
        # GET talebiyle sayfaya erişildiğinde burası çalışır
        all_cities = City.objects.all()
        all_cars = Car.objects.all()

        context = {
            'cities': all_cities,
            'cars': all_cars
        }

        return render(request, 'rent.html', context)
