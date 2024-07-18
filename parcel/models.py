from django.utils import timezone
import django
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200, help_text="Enter your first name")
    last_name = models.CharField(max_length=200, help_text="Enter your last name")
    phone_number = models.CharField(max_length=200, help_text="Enter your phone number")
    email_address = models.EmailField(max_length=200, unique=True, help_text="Enter your email address")
    password_hash = models.CharField(max_length=128, help_text="Enter your password")

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

    def clean(self):
        # Custom validation for password field
        if len(self.password_hash) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

    def __str__(self):
        return self.email_address

class Airport(models.Model):
    airport_id = models.AutoField(primary_key=True)
    airport_name = models.CharField(max_length=255, unique=True, help_text="Enter Airport Name")

    def __str__(self):
        return self.airport_name

class Airline(models.Model):
    airline_id = models.AutoField(primary_key=True)
    airline_name = models.CharField(max_length=255, unique=True, help_text="Enter Airline Name")

    def __str__(self):
        return self.airline_name

class Aircraft(models.Model):
    aircraft_id = models.AutoField(primary_key=True)
    aircraft_name = models.CharField(max_length=255, unique=True, help_text="Enter Aircraft Name")

    def __str__(self):
        return self.aircraft_name
        
class Flight(models.Model):
    flight_id = models.AutoField(primary_key=True)
    airline_id = models.ForeignKey(Airline, on_delete=models.CASCADE)
    aircraft_id = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE)
    departure_time =  models.DateTimeField(help_text="Enter Departure Time")
    arrival_time =  models.DateTimeField(help_text="Enter Arrival Time")

    def __str__(self):
        departure_time_formatted = timezone.localtime(self.departure_time).strftime('%Y-%m-%d %I:%M %p')
        return f"{self.aircraft_id} of {self.airline_id} to {self.destination} at {departure_time_formatted}"
    
def validate_delivery_status(value):
    if value not in ['Yes', 'No']:
        raise ValidationError('Delivery status can either be "Yes" or "No"')

class Fee(models.Model):
    fee_id = models.AutoField(primary_key=True)
    mass_range = models.CharField(max_length=255, unique=True, help_text="Enter Mass Range")
    parcel_transit_cost =  models.IntegerField(help_text="Enter Parcel Transit Cost")

    def __str__(self):
        return f"{self.mass_range}: Ksh. {self.parcel_transit_cost}"

class Parcel(models.Model):
    parcel_id = models.AutoField(primary_key=True)
    sender = models.EmailField(max_length=200, unique=False, help_text="Enter email address of the sender")
    flight_id = models.ForeignKey(Flight, on_delete=models.CASCADE)
    reciever = models.EmailField(max_length=200, unique=False, help_text="Enter email address of the reciever")
    parcel_description = models.CharField(max_length=255, help_text="Enter Parcel Description")
    fee_id = models.ForeignKey(Fee, on_delete=models.CASCADE)
    submitted_at =  models.DateTimeField(default=django.utils.timezone.now,help_text="Enter Submittion Time")
    reciept_number=models.CharField(max_length=255,unique=True,help_text=" Enter Valid Reciept Number")
    DELIVERY_STATUS_CHOICES = [
            ('Yes', 'Yes'),
            ('No', 'No'),
        ]
    delivery_status = models.CharField(
        max_length=3,
        choices=DELIVERY_STATUS_CHOICES,
        help_text="Choose a valid delivery status",
        validators=[validate_delivery_status],
        default='No'
    )

    def __str__(self):
        return f"{self.reciept_number}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email}) on {self.timestamp}"

class PasswordResetToken(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=32)
    expiry_timestamp = models.DateTimeField()