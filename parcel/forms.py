from django import forms
from .models import Customer,Parcel, Flight, Fee
from django.utils import timezone

class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'})
    )

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone_number', 'email_address', 'password_hash']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'phone_number': 'Phone Number',
            'email_address': 'Email Address',
            'password_hash': 'Password',
            'confirm_password': 'Confirm Password',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'password_hash': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password_hash")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password and confirm password do not match")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.set_password(self.cleaned_data["password_hash"])
        if commit:
            instance.save()
        return instance

class LoginForm(forms.Form):
    email_address = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class SendParcelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter flights with departure times in the future
        self.fields['flight_id'].queryset = Flight.objects.filter(departure_time__gt=timezone.now())

    flight_id = forms.ModelChoiceField(
        queryset=Flight.objects.none(),  # Initialize with an empty queryset
        required=True,
        label='Flight',
        widget=forms.Select(attrs={'class': 'blue-input-box', 'placeholder': 'Select prefered flight'}),
    )
    fee_id = forms.ModelChoiceField(
        queryset=Fee.objects.all(),
        required=True,
        label='Mass Range',
        widget=forms.Select(attrs={'class': 'blue-input-box', 'placeholder': 'Choose Your Mass Range'}),
    )

    class Meta:
        model = Parcel
        fields = ['flight_id', 'reciever', 'parcel_description', 'fee_id']
        labels = {
            'flight_id': 'Preffered Flight',
            'reciever': 'Reciever Email Address',
            'parcel_description': 'Parcel Description',
            'fee_id': 'Mass Range',
        }
        widgets = {
            'reciever': forms.EmailInput(attrs={'class': 'blue-input-box', 'placeholder': 'Enter Reciever Email Address'}),
            'parcel_description': forms.TextInput(attrs={'class': 'blue-input-box', 'placeholder': 'Enter Parcel Description'}),
        }

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your Email'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your Message'}))

class PasswordResetForm(forms.Form):
    email_address = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'})
    )

    def clean_email_address(self):
        email = self.cleaned_data.get('email_address')
        if not Customer.objects.filter(email_address=email).exists():
            raise forms.ValidationError("This email address is not associated with any account!")
        return email
