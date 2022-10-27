from ctypes import Union
from dataclasses import dataclass
import uuid
from django.db import models
from typing import Dict, List
from .utils import NotFoundException


class BaseModels(models.Model):
    id = models.UUIDField(primary_key=True, unique=True,default=uuid.uuid4)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    remove_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract=True


class Services(models.Model):
    id = models.UUIDField(primary_key=True, unique=True,default=uuid.uuid4)
    service = models.CharField(max_length=60)

    def __str__(self) -> str:
        return self.service


class District(models.Model):
    id = models.UUIDField(primary_key=True, unique=True,default=uuid.uuid4)
    area = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.area


class Doctors(BaseModels):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, null=True, blank=True)


class ServicesDetails(BaseModels):
    fee = models.IntegerField()
    service = models.ForeignKey(Services, on_delete=models.CASCADE, related_name="service_detail")
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE, related_name="service_detail")
    schedules = models.JSONField(default=dict)


class Clinic(BaseModels):
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE, related_name="clinic")
    service = models.ForeignKey(ServicesDetails, on_delete=models.CASCADE, related_name="clinic")
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    address = models.TextField()


@dataclass
class ServiceSchedules:
    SUNDAY:str = None
    MONDAY:str = None
    TUESDAY:str = None
    WEDNESDAY:str = None
    THURSDAY:str = None
    FRIDAY:str = None
    SATURDAY:str = None
    PUBLIC_HOLIDAY:str = None
    TIMEZONE:str = "UTC"

    @property
    def as_dict(self):
        return {
            "SUNDAY":self.SUNDAY,
            "MONDAY":self.MONDAY,
            "TUESDAY":self.TUESDAY,
            "WEDNESDAY":self.WEDNESDAY,
            "THURSDAY":self.THURSDAY,
            "FRIDAY":self.FRIDAY,
            "SATURDAY":self.SATURDAY,
            "PUBLIC_HOLIDAY":self.PUBLIC_HOLIDAY,
            "TIMEZONE":self.TIMEZONE,
        }


@dataclass
class DetailServices:
    services_id:uuid.UUID
    fee:int
    clinic_address:str
    district_id:uuid.UUID
    schedules:ServiceSchedules
    service:Services = None
    district:District = None

    def __post_init__(self):
        try:
            self.service = Services.objects.get(id=self.services_id)
        except Services.DoesNotExist:
            raise NotFoundException(detail=f"services with id: {self.services_id}, does not exist.")
        
        try:
            self.district = District.objects.get(id=self.district_id)
        except District.DoesNotExist:
            raise NotFoundException(detail=f"district with id: {self.district_id}, does not exist.")

    @property
    def as_dict(self):
        return {
            "services":self.service.service,
            "fee":self.fee,
            "clinic_address":self.clinic_address,
            "district":self.district.area,
            "schedules":self.schedules.as_dict,
        }


@dataclass
class AddDoctor:
    name:str
    phone_number:str
    detail_services:List[DetailServices]

    @property
    def as_dict(self):
        return {
            "name":self.name,
            "phone_number":self.phone_number,
            "detail_services":[detail.as_dict for detail in self.detail_services],
        }

    