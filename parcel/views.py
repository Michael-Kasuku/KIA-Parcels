import uuid
from django.shortcuts import render, redirect
from django.views import View
from .forms import LoginForm, RegisterForm, SendParcelForm, ContactForm, PasswordResetForm
from .models import Customer, Parcel,Airport, Airline, Aircraft, Flight, ContactMessage, PasswordResetToken,Fee
from django.contrib.auth import logout
from django.utils import timezone
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email_address = form.cleaned_data['email_address']
            password = form.cleaned_data['password']
            customer = Customer.objects.filter(email_address=email_address).first()
            if customer and customer.check_password(password):
                # Authentication successful
                request.session['email_address'] = customer.email_address
                return redirect('dashboard')
            else:
                # Authentication failed
                form.add_error(None, "Incorrect email address or password!")
                return render(request, self.template_name, {'form': form}, status=400)
        else:
            return render(request, self.template_name, {'form': form}, status=400)

class RegisterView(View):
    template_name = 'signup.html'

    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            email_address = form.cleaned_data['email_address']

            # REQ-1: Check if account already exists
            if Customer.objects.filter(email_address=email_address).exists():
                form.add_error(None, "This email address has already been used!")
                return render(request, self.template_name, {'form': form})
            else:
                # Create the account
                # Save the application
                new_account = form.save(commit=False)
                new_account.set_password(form.cleaned_data['password_hash'])
                new_account.save()
                
                # Redirect to success page
                return redirect('register_success')
        else:
            # If the form is not valid, render the template with the form and errors
            return render(request, self.template_name, {'form': form})

class PasswordResetView(View):
    template_name = 'forgot_password.html'

    def get(self, request):
        form = PasswordResetForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            email_address = form.cleaned_data['email_address']

            # REQ-1: Check if the email address exists
            if not Customer.objects.filter(email_address=email_address).exists():
                form.add_error(None, "Invalid email address!")
            else:
                # Generate a unique token
                token = get_random_string(length=32)

                # Store the token along with the user's email address and expiration timestamp
                PasswordResetToken.objects.create(
                    email=email_address,
                    token=token,
                    expiry_timestamp=timezone.now() + timezone.timedelta(hours=1)  # Token expires in 1 hour
                )

                # Construct the password reset link
                reset_link = request.build_absolute_uri(f'/password-reset/{token}')

                # Send email with the reset link
                send_mail(
                    'Password Reset Link',
                    f'Click the following link to reset your password: {reset_link}',
                    'support@kia-parcels.com',
                    [email_address],
                    fail_silently=False,
                )

                # Redirect to a success page or display a success message
                return redirect('password_reset_success',email_address=email_address)
            
        # If there are errors, render the template with the form and errors
        return render(request, self.template_name, {'form': form})

class PasswordResetSuccessView(View):
    def get(self, request):
        email_address = self.kwargs.get('email_address', None)
        return render(request, 'password_reset_success.html', {'email_address': email_address})
    
class DashboardView(View):
    template_name = 'dashboard.html'

    def get(self, request):
        airports = Airport.objects.all()
        airlines = Airline.objects.all()
        aircrafts = Aircraft.objects.all()
        current_time = timezone.now()
        future_flights = Flight.objects.filter(departure_time__gt=current_time)
        past_flights = Flight.objects.filter(departure_time__lte=current_time)
        parcel_transit_cost = Fee.objects.all()
        
        context = {
            'airports': airports,
            'airlines': airlines,
            'aircrafts': aircrafts,
            'future_flights': future_flights,
            'past_flights': past_flights,
            'parcel_transit_cost': parcel_transit_cost,
        }
        
        return render(request, self.template_name, context)

class SendParcelView(View):
    template_name = 'send_parcels.html'

    def get(self, request):
        form = SendParcelForm()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = SendParcelForm(request.POST)
        if form.is_valid():
            reciept_number = uuid.uuid4().hex[:10].upper()  # Generate ticket number
            sender =  request.session['email_address']
            send_parcel_form = form.save(commit=False)
            send_parcel_form.sender = sender
            send_parcel_form.reciept_number = reciept_number
            send_parcel_form.save()
            # Store the ticket number in the session
            request.session['reciept_number'] = reciept_number
            
            return redirect('sending_success')  # Redirect to sending success page
        else:
            return render(request, 'send_parcels.html', {'form': form})

class AboutUsView(View):
    template_name = 'about_us.html'

    def get(self, request):
        return render(request, self.template_name)

class ContactUsView(View):
    template_name = 'contact_us.html'

    def get(self, request):
        form = ContactForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the form data to the ContactMessage model
            contact_message = ContactMessage(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            contact_message.save()

            # Optionally, send a success message
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact_us_success')
        return render(request, self.template_name, {'form': form})

class ContactUsSuccessPageView(View):
    template_name = 'contact_us_success.html'
    
    def get(self, request):
        return render(request, self.template_name )

class FAQsView(View):
    template_name = 'faqs.html'

    def get(self, request):
        faqs = [
            {
                "question": "What is KIA Parcels?",
                "answer": "KIA Parcels is a parcel management platform developed in July 2024 for Kisumu International Airport by Kasuku Tech Junction."
            },
            {
                "question": "How can I send a parcel?",
                "answer": "To send a parcel, simply navigate to the 'Send Parcel' section on our platform, fill in the necessary details, and follow the instructions."
            },
            {
                "question": "How can I track my sent parcels?",
                "answer": "You can track your sent parcels by visiting the 'Sent Parcels' section and entering your tracking number."
            },
            {
                "question": "How can I receive a parcel?",
                "answer": "You will be notified when a parcel addressed to you arrives. You can then visit the 'Received Parcels' section to check its status."
            },
            {
                "question": "How do I contact support?",
                "answer": "For any assistance, please visit our 'Contact Us' page where you can find our contact details and a form to send us a message."
            },
        ]
        return render(request, self.template_name, {'faqs': faqs})

def sending_success(request):
    # Retrieve the ticket number from the session (or database, if applicable)
    reciept_number = request.session.get('reciept_number')
    return render(request, 'sending_success.html', {'reciept_number': reciept_number})

def logout_view(request):
    # Log out the user
    logout(request)
    # Clear the session data
    request.session.flush()
    # Redirect the user to a specific page (optional)
    return redirect('login')  # Redirect to the home page after logout

def sent_parcels(request):
    # Retrieve future events from the database
    sent_parcels = Parcel.objects.filter(sender=request.session['email_address'])
    return render(request, 'sent_parcels.html', {'sent_parcels': sent_parcels})

def received_parcels(request):
    received_parcels = Parcel.objects.filter(reciever=request.session['email_address'])
    return render(request, 'recieved_parcels.html', {'recieved_parcels': received_parcels})

class RegisterSuccessPageView(View):
    template_name = 'register_success.html'
    
    def get(self, request):
        return render(request, self.template_name )
