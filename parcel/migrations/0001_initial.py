# Generated by Django 5.0.6 on 2024-07-18 08:34

import django.db.models.deletion
import django.utils.timezone
import parcel.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aircraft',
            fields=[
                ('aircraft_id', models.AutoField(primary_key=True, serialize=False)),
                ('aircraft_name', models.CharField(help_text='Enter Aircraft Name', max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Airline',
            fields=[
                ('airline_id', models.AutoField(primary_key=True, serialize=False)),
                ('airline_name', models.CharField(help_text='Enter Airline Name', max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('airport_id', models.AutoField(primary_key=True, serialize=False)),
                ('airport_name', models.CharField(help_text='Enter Airport Name', max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(help_text='Enter your first name', max_length=200)),
                ('last_name', models.CharField(help_text='Enter your last name', max_length=200)),
                ('phone_number', models.CharField(help_text='Enter your phone number', max_length=200)),
                ('email_address', models.EmailField(help_text='Enter your email address', max_length=200, unique=True)),
                ('password_hash', models.CharField(help_text='Enter your password', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Fee',
            fields=[
                ('fee_id', models.AutoField(primary_key=True, serialize=False)),
                ('mass_range', models.CharField(help_text='Enter Mass Range', max_length=255, unique=True)),
                ('parcel_transit_cost', models.IntegerField(help_text='Enter Parcel Transit Cost')),
            ],
        ),
        migrations.CreateModel(
            name='PasswordResetToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('token', models.CharField(max_length=32)),
                ('expiry_timestamp', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('flight_id', models.AutoField(primary_key=True, serialize=False)),
                ('departure_time', models.DateTimeField(help_text='Enter Departure Time')),
                ('arrival_time', models.DateTimeField(help_text='Enter Arrival Time')),
                ('aircraft_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parcel.aircraft')),
                ('airline_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parcel.airline')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parcel.airport')),
            ],
        ),
        migrations.CreateModel(
            name='Parcel',
            fields=[
                ('parcel_id', models.AutoField(primary_key=True, serialize=False)),
                ('sender', models.EmailField(help_text='Enter email address of the sender', max_length=200)),
                ('reciever', models.EmailField(help_text='Enter email address of the reciever', max_length=200)),
                ('parcel_description', models.CharField(help_text='Enter Parcel Description', max_length=255)),
                ('submitted_at', models.DateTimeField(default=django.utils.timezone.now, help_text='Enter Submittion Time')),
                ('reciept_number', models.CharField(help_text=' Enter Valid Reciept Number', max_length=255, unique=True)),
                ('delivery_status', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', help_text='Choose a valid delivery status', max_length=3, validators=[parcel.models.validate_delivery_status])),
                ('fee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parcel.fee')),
                ('flight_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parcel.flight')),
            ],
        ),
    ]