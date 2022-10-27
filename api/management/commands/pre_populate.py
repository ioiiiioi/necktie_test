from django.core.management.base import BaseCommand
from api.models import (
    Services,
    District
)
from typing import Any, Optional

services = [
    {"id":"6b712140-6a6f-4cab-9fa6-fefa4d8df6c3",  "service":"General Practitioner"},
    {"id":"b3833250-af5d-4f34-87b6-23c31e7c0b1c",  "service":"Allergy and immunology"},
    {"id":"a0c44655-a416-473f-8638-8698bdf57f45",  "service":"Anesthesiology"},
    {"id":"fd4b5c05-ce2a-479e-ac69-9f7f33609b24",  "service":"Dermatology"},
    {"id":"e41e1050-1902-4f04-b1fd-8adad1265f04",  "service":"Diagnostic radiology"},
    {"id":"e81813bf-dd6d-40ef-b88b-0f93c2957c48",  "service":"Emergency medicine"},
    {"id":"b789ef57-4156-4b9f-a824-98972cdf4300",  "service":"Family medicine"},
    {"id":"1798204a-3fa3-4b31-8e51-f13c2110d21e",  "service":"Internal medicine"},
    {"id":"de00d328-9731-4cb8-a73c-fb4cf74cf787",  "service":"Medical genetics"},
    {"id":"c08d5621-88fb-4aab-8eb0-4472e0eed5b4",  "service":"Neurology"},
    {"id":"d8611cc5-cbd8-4771-9b64-c5d25127b483",  "service":"Nuclear medicine"},
    {"id":"165872fc-7c4d-4788-bd35-195bdf22cb04",  "service":"Obstetrics and gynecology"},
    {"id":"8cad0398-4887-4645-b17d-fb714643eb40",  "service":"Ophthalmology"},
    {"id":"4dd5b257-79ef-4968-9dbb-cd2b4a7520ab",  "service":"Pathology"},
    {"id":"6e5a0dc0-90c8-4d7d-90ec-267e047c325a",  "service":"Pediatrics"},
    {"id":"1a482702-aa2f-4c6a-8867-ea8124c95902",  "service":"Physical medicine and rehabilitation"},
    {"id":"51020f53-0b56-435a-aa25-528b8565cf20",  "service":"Preventive medicine"},
    {"id":"e35c0b0d-2960-4752-b89d-dcc6e9e74064",  "service":"Psychiatry"},
    {"id":"45fae754-1408-46fe-98b8-e4624acc7987",  "service":"Radiation oncology"},
    {"id":"9abe39f2-e5a5-4706-836f-43575a21df3e",  "service":"Surgery"},
    {"id":"f86f2e4c-1162-4126-9644-b250e4341c39",  "service":"Urology"},
    {"id":"074b1bc1-f1c5-46f6-899b-341aa42f59a6",  "service":"Dentist"},
    {"id":"00a4546e-e978-4308-9147-c11c4ae97a5e",  "service":"General Practitioner"},
    {"id":"ba8fa457-f793-46d4-9652-a7f9c13ee222",  "service":"Allergy and immunology"},
    {"id":"46920c1d-bb15-4d7e-98c3-877e5b56f333",  "service":"Anesthesiology"},
    {"id":"1d988812-171e-4b8c-9ba6-dd607948c295",  "service":"Dermatology"},
    {"id":"bed3a4f0-2167-4240-bfd5-a1c2cec841c9",  "service":"Diagnostic radiology"},
    {"id":"cbe00595-4daa-46d2-8e1b-7edcac5a37d2",  "service":"Emergency medicine"},
    {"id":"f883000e-ee14-4bfb-951d-82d5def9d777",  "service":"Family medicine"},
    {"id":"f90dfe3a-dc8b-49ba-8ddc-f28bba03b4b2",  "service":"Internal medicine"},
    {"id":"c3a1c02c-fc60-4c32-829e-3da42bc0f7f2",  "service":"Medical genetics"},
    {"id":"e506181f-870d-4358-aa0c-fbdc14f00242",  "service":"Neurology"},
    {"id":"5773e131-2b6a-4fdc-ac9f-0fd0bfe1990b",  "service":"Nuclear medicine"},
    {"id":"e58e96e9-ae68-4e80-adbc-1010e77c7f33",  "service":"Obstetrics and gynecology"},
    {"id":"abe6c129-b7a8-4c8b-b360-e9d0f589e064",  "service":"Ophthalmology"},
    {"id":"ab8d3688-0cdc-4b94-88d9-e41edd5fab6f",  "service":"Pathology"},
    {"id":"cdc5184f-3970-45fd-9712-4878f1348a0e",  "service":"Pediatrics"},
    {"id":"726fa539-8b4b-42f7-a2c5-889f4697221c",  "service":"Physical medicine and rehabilitation"},
    {"id":"68e49f68-d0d6-441a-bfd6-c5ce79b25ce0",  "service":"Preventive medicine"},
    {"id":"07a4bae1-3a61-48d3-91aa-ba4e8331160f",  "service":"Psychiatry"},
    {"id":"af9537b2-8816-4c64-8cde-795f3b6eb057",  "service":"Radiation oncology"},
    {"id":"7c63ba5a-9a22-453d-95ff-045e7a48baba",  "service":"Surgery"},
    {"id":"7fa2b8ec-7481-42c7-b446-575ef15faa35",  "service":"Urology"},
    {"id":"0b2e8ea1-ad61-4e92-8f8a-c08ddb65c8f3",  "service":"Dentist"},
]

districts = [
    {"id":"225d587d-421f-45c5-b9fc-94b5a5ed253c", "area":"Central and Western"},
    {"id":"f1c97954-b2af-429e-a462-e1732bdf3120", "area":"Eastern"},
    {"id":"d9605778-7cb2-4681-9230-f5fb80392366", "area":"Southern"},
    {"id":"25e6c3ad-8359-491d-a9da-bd7779f96c84", "area":"Wan Chai"},
    {"id":"a1a98781-e0da-46be-bfaa-cba3b3e8c524", "area":"Kowloon City"},
    {"id":"1ec7a113-eeef-451d-9e75-59469d46b71d", "area":"Kwun Tong"},
    {"id":"179cc2aa-48a2-4ed3-b429-8b19cc56c76e", "area":"Sham Shui Po"},
    {"id":"297c0ed6-66f4-4077-89a7-68679cc7130c", "area":"Wong Tai Sin"},
    {"id":"6bab913f-454b-4c3b-9f5e-dcbd8f7cb5f5", "area":"Yau Tsim Mong"},
    {"id":"a1d97581-d99e-4ebf-91fa-c56efcd29cdb", "area":"Islands"},
    {"id":"3f402012-333d-490a-9e0f-b445613fc3a1", "area":"Kwai Tsing"},
    {"id":"e821194e-47bb-4d42-892a-6cfb29b61ff9", "area":"North"},
    {"id":"d1767bc5-b697-4d25-bcc7-535b73162f4d", "area":"Sai Kung"},
    {"id":"df180d63-0e91-40df-b3ac-8811ba51e398", "area":"Sha Tin"},
    {"id":"92a39511-48a6-4165-b1c5-5eefb0657250", "area":"Tai Po"},
    {"id":"63086d13-3170-46d6-b2d8-c05389e64050", "area":"Tsuen Wan"},
    {"id":"ae14e804-29fe-46de-86c9-76ad59816bd9", "area":"Tuen Mun"},
    {"id":"294151cd-d93d-44fc-b471-e8f032f98a7c", "area":"Yuen Long"},
    {"id":"88dd9c92-77af-4069-8b1d-7311375f9e52", "area":"Central and Western"},
    {"id":"8e7f1f03-c323-4916-8923-655292fe7ebc", "area":"Eastern"},
    {"id":"5e5055f2-8faf-4fcb-9b20-8b66ad985fa9", "area":"Southern"},
    {"id":"550061c9-1c34-422f-a408-31d63214f70b", "area":"Wan Chai"},
    {"id":"407ce7e9-b998-475a-80ef-b8ef0b6bd7d8", "area":"Kowloon City"},
    {"id":"a0704f40-9b83-4a4f-9bfb-188b8ba18109", "area":"Kwun Tong"},
    {"id":"3ae46aac-167f-4369-8710-f22f7074b68a", "area":"Sham Shui Po"},
    {"id":"7a8b3027-2598-47e5-9b8b-f8824bf9d164", "area":"Wong Tai Sin"},
    {"id":"3759399e-d6f9-4394-b56c-fb5109fcc12a", "area":"Yau Tsim Mong"},
    {"id":"47b76c77-6a1c-4ee2-b05f-3b7e7f441134", "area":"Islands"},
    {"id":"9abe4047-4472-400c-a285-d86c2eebf9c3", "area":"Kwai Tsing"},
    {"id":"452abd58-68e3-41b9-ba51-883cfbb7e4cf", "area":"North"},
    {"id":"90f1f821-5d30-40db-bab6-3732de76a378", "area":"Sai Kung"},
    {"id":"e9b0e441-a007-44e8-a1fd-d156e8f56439", "area":"Sha Tin"},
    {"id":"beb9a2e7-a830-4007-a59f-42bc8da14254", "area":"Tai Po"},
    {"id":"a2834cd7-e55c-4385-b56b-baa34fd3e0f7", "area":"Tsuen Wan"},
    {"id":"e8b9849f-aa2a-488c-ad3e-d9376a4a5430", "area":"Tuen Mun"},
    {"id":"e95cad83-321d-4c46-9943-0189a6d06526", "area":"Yuen Long"},
]

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        check_services = Services.objects.all()
        check_district = District.objects.all()
        
        if not check_services.exists():
            services_list = []
            for service_name in services:
                services_list.append(Services(
                    **service_name
                ))

            Services.objects.bulk_create(services_list)

        if not check_district.exists():
            district_list = []
            for district in districts:
                district_list.append(District(
                    **district
                ))
            
            District.objects.bulk_create(district_list)


