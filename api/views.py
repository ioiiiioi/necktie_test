from unittest import result
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .controller import DoctorLogic

# Create your views here.
"""
bulk create doctors
create doctor
get doctor with id
get all doctors
"""


@api_view(["POST"])
def add_doctor(request):
    controller = DoctorLogic()
    result = controller.create_doctor(request)
    return Response(result, status=200)

@api_view(["GET"])
def get_all_doctors(request):
    controller = DoctorLogic()
    result = controller.fetch_all_doctors
    return Response(result, status=200)

@api_view(["GET"])
def get_doctor(request, doctor_id):
    controller = DoctorLogic()
    result = controller.get_doctor(doctor_id)
    return Response(result, status=200)