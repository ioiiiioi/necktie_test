from dataclasses import dataclass
from django.test import TestCase
from typing import Dict
from .controller import DoctorLogic
from .models import (
    Services, 
    District,
)
from .management.commands.pre_populate import services, districts

# Create your tests here.

@dataclass
class MockRequest:
    data:Dict

class ApiTestCase(TestCase):

    def setUp(self) -> None:
        self.sample = {
            "name":"Dr.Richard",
            "phone_number":"+62899288390",
            "detail_services": [
                {
                    "services_id":"00a4546e-e978-4308-9147-c11c4ae97a5e", # General Practitioner
                    "fee":520,
                    "clinic_address":"Random clinic address",
                    "district_id":"1ec7a113-eeef-451d-9e75-59469d46b71d", # Kwun Tong
                    "schedules": {
                        "sunday" : "18.00 - 20.00",
                        "monday": "18.00 - 20.00",
                        "tuesday": "18.00 - 20.00",
                        "wednesday": "18.00 - 20.00",
                        "thursday": "18.00 - 20.00",
                        "friday": "18.00 - 20.00",
                        "saturday": "18.00 - 20.00",
                        "public_holiday": "18.00 - 20.00"
                    }
                }
            ]
            
        }

        services_list = []
        for service_name in services:
            services_list.append(Services(
                **service_name
            ))

        Services.objects.bulk_create(services_list)

        district_list = []
        for district in districts:
            district_list.append(District(
                **district
            ))
        
        District.objects.bulk_create(district_list)

    def add_doctor(self):
        payload = MockRequest(
            data=self.sample
        )

        api = DoctorLogic()
        request = api.create_doctor(request=payload)
        return request, request['id']

    def test_add_doctor(self):
        request, _ = self.add_doctor()
        request_detail = request["detail_services"]
        for detail in request_detail:
            self.assertEqual(detail["services"] ,"General Practitioner")
            self.assertEqual(detail["district"] ,"Kwun Tong")

        detail_services = self.sample['detail_services']
        self.assertEqual(request["name"], self.sample["name"])
        self.assertEqual(request["phone_number"], self.sample["phone_number"])
        self.assertEqual(len(detail_services), len(request_detail))

    def test_get_all_doctors(self):
        _ = self.add_doctor()
        request = DoctorLogic()
        response = request.fetch_all_doctors
        self.assertEqual(len(response), 1)
        for data in response:
            self.assertEqual(data["name"], self.sample["name"])
    
    def test_get_doctor(self):
        _, id = self.add_doctor()
        request = DoctorLogic()
        response = request.get_doctor(doctor_id=id)
        self.assertEqual(id, response["id"])
        self.assertEqual(self.sample["name"], response["name"])


