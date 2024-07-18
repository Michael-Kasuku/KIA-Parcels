from django.contrib import admin
from django.urls import include, path

urlpatterns=[
    path("kiaparcels/customer/", include("parcel.urls")),
    path("kiaparcels/admin/",admin.site.urls),
]