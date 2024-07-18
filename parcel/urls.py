from django.urls import path
from .views import LoginView, DashboardView, RegisterView,SendParcelView, AboutUsView, ContactUsView,FAQsView,PasswordResetView,PasswordResetSuccessView,RegisterSuccessPageView,ContactUsSuccessPageView
from .views import sent_parcels,received_parcels,sending_success,logout_view

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('dashboard/',DashboardView.as_view(), name='dashboard'),
    path('register/', RegisterView.as_view(), name='register'),
    path('send/', SendParcelView.as_view(), name='send_parcel'),
    path('sent/', sent_parcels, name='sent_parcels'),
    path('received/', received_parcels, name='received_parcels'),
    path('success/', sending_success, name='sending_success'),
    path('about_us/', AboutUsView.as_view(), name='about_us'),
    path('contact_us/', ContactUsView.as_view(), name='contact_us'),
    path('faqs/', FAQsView.as_view(), name='faqs'),
    path('logout/', logout_view, name='logout'),
    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_success/<str:email_address>/', PasswordResetSuccessView.as_view(), name='password_reset_success'),
    path('register/success/', RegisterSuccessPageView.as_view(), name='register_success'),
    path('contact_us/success/', ContactUsSuccessPageView.as_view(), name='contact_us_success'),
]
