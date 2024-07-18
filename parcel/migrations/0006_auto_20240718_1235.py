from django.db import migrations
import openpyxl
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

def insert_flights(apps, schema_editor):
    Airline = apps.get_model('parcel', 'Airline')
    Aircraft = apps.get_model('parcel', 'Aircraft')
    Airport = apps.get_model('parcel', 'Airport')
    Flight = apps.get_model('parcel', 'Flight')

    try:
        # Load data from Excel workbook
        wb = openpyxl.load_workbook('parcel/data/kia.xlsx')
        sheet = wb['Flight']

        # Iterate over rows in the Excel sheet and extract flight information
        flights_data = []
        for row in sheet.iter_rows(min_row=2, values_only=True):  # Assuming data starts from second row
            airline_name = row[0]  # Assuming airline name is in the first column
            aircraft_name = row[1]  # Assuming aircraft name is in the second column
            airport_name = row[2]  # Assuming airport name is in the third column
            departure_time = row[3]  # Assuming departure time is in the fourth column
            arrival_time = row[4]  # Assuming arrival time is in the fifth column
            
            # Fetch airline, aircraft, and airport objects from the database
            try:
                airline_id = Airline.objects.get(airline_name=airline_name)
                aircraft_id = Aircraft.objects.get(aircraft_name=aircraft_name)
                airport_id = Airport.objects.get(airport_name=airport_name)
            except ObjectDoesNotExist as e:
                print(f"Error: {e}")
                continue  # Skip this row if any object doesn't exist
            
            # Make departure_time and arrival_time timezone-aware
            departure_time = timezone.make_aware(departure_time, timezone.get_default_timezone())
            arrival_time = timezone.make_aware(arrival_time, timezone.get_default_timezone())
            
            # Create dictionary for flight
            flight_data = {
                'airline_id': airline_id,
                'aircraft_id': aircraft_id,
                'destination': airport_id,
                'departure_time': departure_time,
                'arrival_time': arrival_time,
            }
            
            # Append flight data to list
            flights_data.append(flight_data)

        # Insert data into the model
        for data in flights_data:
            Flight.objects.create(**data)
    except FileNotFoundError:
        print("File not found. Please check the path to the Excel file.")
    except Exception as e:
        print(f"An error occurred: {e}")

class Migration(migrations.Migration):

    dependencies = [
        ('parcel', '0005_auto_20240718_1221'),
    ]

    operations = [
        migrations.RunPython(insert_flights)
    ]
