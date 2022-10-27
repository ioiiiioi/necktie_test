from audioop import add
from django.urls import path
from .views import (
    add_doctor,
    get_all_doctors,
    get_doctor,
)

urlpatterns = [
    path("add-doctor/", add_doctor, name="add-doctor"),
    path("doctor/", get_all_doctors, name="all-doctor"),
    path("doctor/<str:doctor_id>/", get_doctor, name="get-doctor"),
]