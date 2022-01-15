from django.db import models
from django.utils import timezone
import math
import numpy as np
import re
# Create your models here.


class VehicleType(models.Model):
    name = models.CharField(max_length=32)
    max_capacity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=32)
    passengers = models.PositiveIntegerField()
    vehicle_type = models.ForeignKey(VehicleType, null=True, on_delete=models.SET_NULL)
    number_plate = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name

    def can_start(self) -> bool:
        return self.vehicle_type.max_capacity >= self.passengers

    #Obtener distribucion - TEST CAMILA
    def get_distribution(self):
        rows_for_passanger=math.ceil((self.passengers/2))
        number_of_rows = 2
        max_capaxity=self.vehicle_type.max_capacity

        if max_capaxity<self.passengers:
            rows_for_passanger=math.ceil((max_capaxity/2))

        matriz = np.full([number_of_rows, rows_for_passanger], True, dtype=bool)
        
        if self.passengers % 2 != 0:
            matriz[math.floor((self.passengers/2))][1]=False

        print(matriz)

        return matriz
    
    #Validar patente -TEST CAMILA
    def validate_number_plate(plate) -> bool:
        plateclean=re.sub(r'[^\w\s]','',plate)
        plateclean=plateclean.upper()
        print(plateclean)

        plateclean=plateclean.replace(" ","")
        print(plateclean)

        platelist=list(plateclean)
        print(platelist)

        platelist1=False
        platelist2=False
        platelist3=False
        platelist4=False
        platelist5=False
        platelist6=False

        if (platelist[0] >= 'A' and platelist[0] <= 'Z'):
            platelist1=True
        if (platelist[1] >= 'A' and platelist[1] <= 'Z'):
            platelist2=True
        if (platelist[2] >= '0' and platelist[2] <= '9'): 
            platelist3=True
        if (platelist[3] >= '0' and platelist[3] <= '9'): 
            platelist4=True
        if (platelist[4] >= '0' and platelist[4] <= '9'): 
            platelist5=True
        if (platelist[5] >= '0' and platelist[5] <= '9'):
            platelist6=True

        if platelist1==True and platelist2==True and platelist3==True and platelist4==True and platelist5==True and platelist6==True:
            print(True)
            return True
        else:
            print(False)
            return False

class Journey(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.vehicle.name} ({self.start} - {self.end})"

    #Viaje Finalizado - TEST CAMILA
    def is_finished(self) -> bool:
        if self.end <= timezone.now().date():
            return True
        else:
            return False