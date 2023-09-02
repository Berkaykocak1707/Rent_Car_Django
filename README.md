# Rent_Car_Django Project

## Overview

This project is a car rental service built with Django. Users can browse available cars and rent them for a specified period. The admin panel allows for the approval of reservations, which in turn updates the corresponding car's information.

## Features

- Browse available cars with filters
- Rent a car for a specified period
- Manage ongoing and past rentals
- Admin interface: Admins can approve reservations and update car information

## Installation & Setup

### Prerequisites

- Python 3.x +
- pip

### Steps

1. **Clone the Repository**

    ```bash
    git clone https://github.com/your-username/Rent_Car_Django.git
    ```

2. **Navigate to the Project Directory**

    ```bash
    cd Rent_Car_Django
    ```

3. **Install Required Packages**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run Migrations**

    ```bash
    python manage.py migrate
    ```

5. **Start the Development Server**

    ```bash
    python manage.py runserver
    ```

    You can now access the application at `http://localhost:8000/`.

## Usage

- To browse available cars, simply go to the Cars Page.
- To rent a car, you can make a reservation.
- Reservations are activated once approved from the admin panel.

## Database

The project uses SQLite for development. You can easily switch to another database by modifying the `DATABASES` setting in `settings.py`.

