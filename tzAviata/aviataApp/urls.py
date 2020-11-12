from aviataApp import views
from django.urls import path

urlpatterns = [
    path('aviata/', views.aviata_booking_test, name='aviata_check_for_1_day_for_all_direction'),
    path('aviata2/', views.aviata_booking_for_month, name='aviata_booking_for_months'),
    # path('aviata3/', views.flights_checked, name='confirmation'),
    path('test/', views.test, name='test')
]
