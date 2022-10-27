from django.db import (
    transaction,
    models,
)
from .utils import (
    NotFoundException,
    ServiceError,
)
from .models import (
    DetailServices,
    ServiceSchedules,
    Doctors,
    ServicesDetails,
    Clinic,
    AddDoctor,
)


class DoctorLogic:

    def create_doctor(self, request):
        data = AddDoctor(**request.data)
        data.detail_services = [DetailServices(**details) for details in data.detail_services]
        try:
            with transaction.atomic():
                doctor = Doctors.objects.create(
                    name=data.name,
                    phone_number=data.phone_number
                )
                for detail in data.detail_services:
                    schedules = {key.upper(): val for key, val in detail.schedules.items()}
                    detail.schedules = ServiceSchedules(**schedules)
                    service_detail = ServicesDetails.objects.create(
                        fee=detail.fee,
                        service_id=detail.services_id,
                        doctor=doctor,
                        schedules=detail.schedules.as_dict,
                    )
                    clinic = Clinic.objects.create(
                        doctor=doctor,
                        service=service_detail,
                        district_id=detail.district_id,
                        address=detail.clinic_address
                    )
            result = data.as_dict
            result["id"] = doctor.id
            return result
        except Exception as e:
            raise ServiceError()
    
    @property
    def fetch_all_doctors(self):
        doctors = Doctors.objects.filter(is_active=True).prefetch_related("clinic", "clinic__service")
        results = []
        for doctor in doctors:
            results.append(
                {
                    "id":doctor.id,
                    "name":doctor.name,
                    "phone_number":doctor.phone_number,
                    "detail_services":doctor.clinic.annotate(
                        clinic_address=models.F("address"), 
                        districts=models.F("district__area"), 
                        services=models.F("service__service__service"), 
                        fee=models.F("service__fee"),
                        schedule=models.F("service__schedules")
                    ).values(
                        "clinic_address",
                        "districts",
                        "services",
                        "fee",
                        "schedule"
                    )
                }
            )
        return results

    def get_doctor(self, doctor_id):
        try:
            doctor = Doctors.objects.get(id=doctor_id)
        except Doctors.DoesNotExist:
            raise NotFoundException(detail="Doctor does not exist.")
        
        result = {
            "id":doctor.id,
            "name":doctor.name,
            "phone_number":doctor.phone_number,
            "detail_services":doctor.clinic.annotate(
                clinic_address=models.F("address"), 
                districts=models.F("district__area"), 
                services=models.F("service__service__service"), 
                fee=models.F("service__fee"),
                schedule=models.F("service__schedules")
            ).values(
                "clinic_address",
                "districts",
                "services",
                "fee",
                "schedule"
            )
        }

        return result
