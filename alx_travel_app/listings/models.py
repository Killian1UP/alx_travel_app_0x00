import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class Status(models.TextChoices):
    PENDING = 'pending', 'Pending'
    CONFIRMED = 'confirmed', 'Confirmed'
    CANCELLED = 'cancelled', 'Cancelled'

class Listing(models.Model):
    listing_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=150)
    description = models.TextField()
    location = models.CharField(max_length=150)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    max_guests = models.IntegerField(null=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def clean(self):
        # Ensure price is not negative
        if self.price_per_night < 0:
            raise ValidationError({'price_per_night': 'Price must be zero or greater.'})
        
        # Ensure max_guests is at least 1
        if self.max_guests < 1:
            raise ValidationError({'max_guests': 'Listing must allow at least 1 guest.'})
        
    def __str__(self):
        return self.title
    
class Booking(models.Model):
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    num_guests = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        # Ensure check-in is before check-out
        if self.check_in_date >= self.check_out_date:
            raise ValidationError({'check_out_date': 'Check-out must be after check-in.'})

        # Ensure guest count does not exceed listing limit
        if self.listing and self.num_guests > self.listing.max_guests:
            raise ValidationError({'num_guests': 'Number of guests exceeds listing capacity.'})

        # Ensure at least 1 guest
        if self.num_guests < 1:
            raise ValidationError({'num_guests': 'Must book for at least 1 guest.'})
        
    def __str__(self):
        return f'Booking {self.booking_id} by {self.guest}'
        
class Review(models.Model):
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        # Ensure reviewer is the same as booking.guest
        if self.booking and self.reviewer != self.booking.guest:
            raise ValidationError("Reviewer must be the guest who made the booking.")

        # Ensure review is for the correct listing
        if self.booking and self.listing != self.booking.listing:
            raise ValidationError("Listing must match the one in the booking.")
        
    def __str__(self):
        return f'Review {self.review_id} ({self.rating}/5)'