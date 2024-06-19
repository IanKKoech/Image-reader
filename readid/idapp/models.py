from django.db import models

class IDData(models.Model):
    serial_number = models.CharField(max_length=100, null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.CharField(max_length=100, null=True, blank=True)  
    sex = models.CharField(max_length=10, null=True, blank=True)
    place_of_birth = models.CharField(max_length=100, null=True, blank=True)
    district_of_birth = models.CharField(max_length=100, null=True, blank=True)
    id_number = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.full_name or "ID Data"

class LogBookData(models.Model):
    registration = models.CharField(max_length=100, null=True, blank=True)
    vehicle_make = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    fuel_type = models.CharField(max_length=100, null=True, blank=True)
    rating_cc = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    owner_name = models.CharField(max_length=100, null=True, blank=True)
    pin = models.CharField(max_length=100, null=True, blank=True)
    axles = models.CharField(max_length=100, null=True, blank=True)
    