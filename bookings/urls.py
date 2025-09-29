from django.urls import path

from . import views

app_name = "bookings"

urlpatterns = [
    path("bookings/create", views.create_booking, name="create_booking"),
    path("bookings/delete", views.delete_booking, name="delete_booking"),
    path("bookings/list", views.list_bookings, name="list_bookings"),
]
