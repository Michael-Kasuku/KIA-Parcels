# Generated by Django 5.0.6 on 2024-07-18 09:13

from django.db import migrations
import openpyxl
from django.core.exceptions import ValidationError

def insert_aircrafts(apps, schema_editor):
    Aircraft = apps.get_model('parcel', 'Aircraft')
    
    try:
        # Load data from Excel workbook
        wb = openpyxl.load_workbook('parcel/data/kia.xlsx')
        sheet = wb['Aircraft']
        
        # Extract Aircraft names from the Excel sheet
        aircrafts_data = []
        for row in sheet.iter_rows(min_row=2, values_only=True):  # Assuming data starts from second row
            aircraft_name = row[0]  # Assuming aircraft name is in the first column
            aircrafts_data.append({'aircraft_name': aircraft_name})
        
        # Insert data into the model
        for data in aircrafts_data:
            try:
                Aircraft.objects.create(**data)
            except ValidationError as e:
                print(f"Validation Error: {e}")
    except FileNotFoundError:
        print("File not found. Please check the path to the Excel file.")
    except Exception as e:
        print(f"An error occurred: {e}")

class Migration(migrations.Migration):

    dependencies = [
        ('parcel', '0003_auto_20240718_1145'),
    ]

    operations = [
        migrations.RunPython(insert_aircrafts)
    ]