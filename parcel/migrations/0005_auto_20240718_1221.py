# Generated by Django 5.0.6 on 2024-07-18 09:21

from django.db import migrations
import openpyxl

def insert_fees(apps, schema_editor):
    Fee = apps.get_model('parcel', 'Fee')

    try:
        # Load data from Excel workbook
        wb = openpyxl.load_workbook('parcel/data/kia.xlsx')
        sheet = wb['Fee']

        # Iterate over rows in the Excel sheet and extract ward information
        fees_data = []
        for row in sheet.iter_rows(min_row=2, values_only=True):  # Assuming data starts from second row
            mass_range = row[0]  # Assuming mass range is in the first column
            parcel_transit_cost = row[1]  # Assuming parcel transit cost is in the second column
            
            # Create dictionary for fee data
            fee_data = {
                'mass_range': mass_range,
                'parcel_transit_cost': parcel_transit_cost
            }
            
            # Append fee data to list
            fees_data.append(fee_data)

        # Insert data into the model
        for data in fees_data:
            Fee.objects.create(**data)
    except FileNotFoundError:
        print("File not found. Please check the path to the Excel file.")
    except Exception as e:
        print(f"An error occurred: {e}")

class Migration(migrations.Migration):

    dependencies = [
        ('parcel', '0004_auto_20240718_1213'),
    ]

    operations = [
        migrations.RunPython(insert_fees)
    ]