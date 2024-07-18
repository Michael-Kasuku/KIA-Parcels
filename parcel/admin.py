from django.contrib import admin

from .models import Customer, Airport, Airline, Aircraft, Flight, Fee, Parcel, ContactMessage,PasswordResetToken

models_to_register = [Customer, Airport, Airline, Aircraft, Flight, Fee, Parcel,ContactMessage,PasswordResetToken]

for model in models_to_register:
    admin.site.register(model)

