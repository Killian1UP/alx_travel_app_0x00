
# ALX Travel App

This project is a simplified travel booking API built using Django and Django REST Framework. It enables hosts to create listings and guests to make bookings, leave reviews, and interact with a basic system that mimics popular travel rental services.

## Features

- **User Management:** Supports host and guest roles via Django’s built-in User model.
- **Listings:** Hosts can create listings including title, description, location, price, and guest capacity.
- **Bookings:** Guests can make bookings for listings with constraints like availability and guest limits.
- **Reviews:** Guests can leave reviews and ratings (1–5) for listings they booked.
- **Validation:** Models include `clean()` methods to validate business logic.
- **Seeding Script:** A management command is available to populate the database with sample listing data.

## Project Structure

```
alx_travel_app/
├── listings/
│   ├── models.py
│   ├── serializers.py
│   ├── management/
│   │   └── commands/
│   │       └── seed.py
│   └── views.py
├── users/ (if using custom auth)
├── manage.py
└── README.md
```

## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/your-username/alx_travel_app.git
cd alx_travel_app
```

2. **Set up virtual environment and install dependencies**

```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

3. **Run migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Create a superuser (optional)**

```bash
python manage.py createsuperuser
```

5. **Seed the database with sample data**

```bash
python manage.py seed
```

This will populate the database with sample listing entries for quick testing.

## Testing

You can run the development server:

```bash
python manage.py runserver
```

Then access the API via endpoints like:
- `/api/listings/`
- `/api/bookings/`

## Notes

- Ensure your app is listed in `INSTALLED_APPS`.
- The `seed` command is located under `listings/management/commands/seed.py` and uses the Django management command framework.

---

© 2025 | ALX Backend Python Project