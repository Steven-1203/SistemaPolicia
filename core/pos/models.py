import os
from datetime import datetime
from crum import get_current_user
from django.db import models
from django.forms import model_to_dict
from config import settings
from core.user.models import User
from core.pos.choices import *

class Personal(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.CharField(max_length=10, verbose_name='Fecha de nacimiento')
    typeblood = models.CharField(max_length=100, null=True, blank=True, verbose_name='Tipo de Sangre')
    citybirth = models.CharField(max_length=100, null=True, blank=True, verbose_name='Ciudad de nacimiento')
    mobile = models.CharField(max_length=10, unique=True, verbose_name='Teléfono')
    grade = models.CharField(max_length=100, null=True, blank=True, verbose_name='Grado')

    def __str__(self):
        return self.user
    
    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return self.user.get_full_name()
    
    def toJSON(self):
        item = model_to_dict(self)
        item['user'] = self.user.toJSON()
        return item

    def delete(self, using=None, keep_parents=False):
        super(Personal, self).delete()
        try:
            self.user.delete()
        except:
            pass

    class Meta:
        verbose_name = 'Personal'
        verbose_name_plural = 'Personal'
        ordering = ['-id']

class Vehicle(models.Model):

    type = models.CharField(max_length=15, choices=TYPE_VEHICLE, default=TYPE_VEHICLE[0][0], verbose_name='Tipo de vehículo')
    placa = models.CharField(max_length=7, null=True, blank=True, verbose_name='Placa del vehículo')
    chasis = models.CharField(max_length=18, null=True, blank=True, verbose_name='Chasis del vehículo')
    model = models.CharField(max_length=10, null=True, blank=True, verbose_name='modelo del vehículo')
    motor = models.CharField(max_length=18, null=True, blank=True, verbose_name='Motor de vehículo')
    km = models.IntegerField(default=0,  null=True, blank=True, verbose_name='Kilometraje del vehículo')
    cylinder = models.CharField(max_length=4, null=True, blank=True, verbose_name='Cilindraje de vehículo')
    capacitycarga = models.CharField(max_length=1, null=True, blank=True, verbose_name='Capacidad de carga')
    capacitypeople = models.CharField(max_length=1, null=True, blank=True, verbose_name='Capacidad de pasajeros')

    def __str__(self):
        return self.type

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículo'
        ordering = ['-id']

class District(models.Model):
    
    name = models.CharField(max_length=150, null=True, blank=True, verbose_name='Nombre')
    code = models.CharField(max_length=8, unique=True, verbose_name='Código')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item
    
    class Meta:
        verbose_name = 'Distrito'
        verbose_name_plural = 'Distrito'
        ordering = ['-id']
    
class Circuit(models.Model):
    
    district = models.ForeignKey(District, on_delete=models.PROTECT, verbose_name='Distrito')
    name = models.CharField(max_length=150, null=True, blank=True, verbose_name='Nombre')
    code = models.CharField(max_length=8, unique=True, verbose_name='Código')
    
    def __str__(self):
        return self.name

    def get_name_district(self):
        return f'{self.district.name}'
    
    def get_personal_circuito(self):
        return [s.personal for s in SubCircuit.objects.filter(Circuit = self).all()]
    
    def toJSON(self):
        item = model_to_dict(self)
        item['district'] = self.get_or_create_district()
        return item

    def get_or_create_district(self, name):
        district = District()
        search = District.objects.filter(name=name)
        if search.exists():
            district = search[0]
        else:
            district.name = name
            district.save()
        return district

    class Meta:
        verbose_name = 'Circuito'
        verbose_name_plural = 'Circuito'
        ordering = ['id']

class SubCircuit(models.Model):

    name = models.CharField(max_length=150, null=True, blank=True, verbose_name='Nombre')
    code = models.CharField(max_length=12, unique=True, verbose_name='Código')
    circuit = models.ForeignKey(Circuit, on_delete=models.PROTECT, verbose_name='Circuito')
    personal = models.ForeignKey(Personal, on_delete=models.PROTECT, verbose_name='Personal')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT, verbose_name='Vehículo')

    def __str__(self):
        return self.get_full_name()
    
    def get_full_name(self):
        return f'{self.name} / {self.circuit.name} / {self.personal.user} ({self.personal.user.dni}) / {self.vehicle.type}'

    def get_short_name(self):
        return f'{self.name} / {self.circuit.name} / {self.personal.user} ({self.personal.user.dni}) / {self.vehicle.type}'

    def get_or_create_circuit(self, name):
        circuit = Circuit()
        search = Circuit.objects.filter(name=name)
        if search.exists():
            circuit = search[0]
        else:
            circuit.name = name
            circuit.save()
        return circuit

    def get_or_create_personal(self, name):
        personal = Personal()
        search = Personal.objects.filter(name=name)
        if search.exists():
            personal = search[0]
        else:
            personal.name = name
            personal.save()
        return personal
    
    def get_or_create_vehicle(self, name):
        vehicle = Vehicle()
        search = Vehicle.objects.filter(name=name)
        if search.exists():
            vehicle = search[0]
        else:
            vehicle.name = name
            vehicle.save()
        return vehicle
    
    def delete(self, using=None, keep_parents=False):
        try:
            os.remove(self.image.path)
        except:
            pass
        super(SubCircuit, self).delete()

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.get_full_name()
        item['short_name'] = self.get_short_name()
        item['circuit'] = self.circuit.toJSON()
        item['personal'] = self.personal.toJSON()
        item['vehicle'] = self.vehicle.toJSON()
        return item

class Suggestion(models.Model):

    names = models.CharField(max_length=150, null=True, blank=True, verbose_name='Nombre')
    email = models.EmailField(null=True, blank=True, verbose_name='Correo electrónico')
    mobile = models.CharField(max_length=10, null=True, verbose_name='Teléfono')
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    circuit = models.ForeignKey(Circuit, on_delete=models.PROTECT, verbose_name='Elegir Circuito')
    subcircuit = models.ForeignKey(SubCircuit, on_delete=models.PROTECT, verbose_name='Elegir Sub circuito')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de Registro')

    def get_full_subcircuit(self):
        return f'{self.subcircuit.name}'
    
    def get_full_circuit(self):
        return f'{self.circuit.name}'

    def __str__(self):
        return self.names

    def toJSON(self):
        item = model_to_dict(self)
        item['subcircuit'] = self.get_full_subcircuit()
        item['circuit'] = self.get_full_circuit()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        return item
    
    class Meta:
        verbose_name = 'Sugerencia'
        verbose_name_plural = 'Sugerencias'
        ordering = ['id']

class Recommendation(models.Model):

    description = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    subcircuit = models.ForeignKey(SubCircuit,on_delete=models.PROTECT, verbose_name='Elegir subcircuito')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de Registro')
    
    def get_full_name(self):
        return f'{self.subcircuit.name}'
    
    def get_full_personal(self):
        return f'{self.subcircuit.personal.user}'
    
    def get_full_circuit(self):
        return f'{self.subcircuit.circuit.name}'
    
    def get_or_create_subcircuit(self, name):
        subcircuit = SubCircuit()
        search = SubCircuit.objects.filter(name=name)
        if search.exists():
            subcircuit = search[0]
        else:
            subcircuit.name = name
            subcircuit.save()
        return subcircuit
    
    def toJSON(self):
        item = model_to_dict(self)
        item['subcircuit'] = self.get_full_name()
        item['personal'] = self.get_full_personal()
        item['circuit'] = self.get_full_circuit()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        return item
    
    def save (self, force_insert=False, force_update=False, usign=None, 
                update_fields=None):
            user = get_current_user()
            if user is not None:
                if not self.pk:
                    self.user_actual = user
                else:
                    self.user_actual = user
            super(Recommendation, self).save()

class Requestsmaintenance(models.Model):
    
    personal = models.ForeignKey(Personal, on_delete=models.PROTECT, verbose_name='Personal')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT, verbose_name='Vehículo')
    typemaintenance = models.CharField(max_length=100, choices=MAINTENANCE_TYPE, default=MAINTENANCE_TYPE[0][0], verbose_name='Tipo de mantenimiento')
    km = models.IntegerField(default=0,  null=True, blank=True, verbose_name='Kilometraje del vehículo')
    observations = models.CharField(max_length=500, null=True, blank=True, verbose_name='Observaciones')
    
    def __str__(self):
        return self.get_full_name()
    
    def get_full_name(self):
        return f'({self.personal.user}) ({self.vehicle.type})'

    def get_short_name(self):
        return f'({self.personal.user}) ({self.vehicle.type})'
    
    def get_or_create_personal(self, name):
        personal = Personal()
        search = Personal.objects.filter(name=name)
        if search.exists():
            personal = search[0]
        else:
            personal.name = name
            personal.save()
        return personal
    
    def get_or_create_vehicle(self, name):
        vehicle = Vehicle()
        search = Vehicle.objects.filter(name=name)
        if search.exists():
            vehicle = search[0]
        else:
            vehicle.name = name
            vehicle.save()
        return vehicle
    
    def delete(self, using=None, keep_parents=False):
        try:
            os.remove(self.image.path)
        except:
            pass
        super(Requestsmaintenance, self).delete()

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.get_full_name()
        item['short_name'] = self.get_short_name()
        item['personal'] = self.personal.toJSON()
        item['vehicle'] = self.vehicle.toJSON()
        return item

class Ordermaintenance(models.Model):

    requests = models.ForeignKey(Requestsmaintenance, on_delete=models.PROTECT, verbose_name='Solicitud')
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    progress = models.CharField(max_length=100, choices=MAINTENANCEORDER_TYPE, default=MAINTENANCEORDER_TYPE[0][0], verbose_name='Progreso')
    
    def __str__(self):
        return self.get_full_name()
    
    def get_full_name(self):
        return f'{self.description}'

    def get_short_name(self):
        return f'{self.description}'
    
    def get_or_create_requests(self, name):
        requests = Requestsmaintenance()
        search = Requestsmaintenance.objects.filter(name=name)
        if search.exists():
            requests = search[0]
        else:
            requests.name = name
            requests.save()
        return requests
    
    def delete(self, using=None, keep_parents=False):
        try:
            os.remove(self.image.path)
        except:
            pass
        super(Ordermaintenance, self).delete()

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.get_full_name()
        item['short_name'] = self.get_short_name()
        item['requests'] = self.requests.toJSON()
        return item

class Taller(models.Model):

    number = models.CharField(max_length=8, unique=True, verbose_name='Número de factura')
    valor = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    order = models.ForeignKey(Ordermaintenance, on_delete=models.PROTECT, verbose_name='Orden de mantenimiento')
    subcircuit = models.ForeignKey(SubCircuit, on_delete=models.PROTECT, verbose_name='Subcircuito') 
    state = models.CharField(max_length=100, choices=STATE_TYPE, default=STATE_TYPE[0][0], verbose_name='Estado')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de Registro')
    
    def get_full_name(self):
        return f'{self.subcircuit.name}'
         
    def get_full_order(self):
        return f'{self.order.description}'
    
    def get_or_create_order(self, name):
        order = Ordermaintenance()
        search = Ordermaintenance.objects.filter(name=name)
        if search.exists():
            order = search[0]
        else:
            order.name = name
            order.save()
        return order
    
    def get_or_create_subcircuit(self, name):
        subcircuit = SubCircuit()
        search = SubCircuit.objects.filter(name=name)
        if search.exists():
            subcircuit = search[0]
        else:
            subcircuit.name = name
            subcircuit.save()
        return subcircuit
    
    def delete(self, using=None, keep_parents=False):
        try:
            os.remove(self.image.path)
        except:
            pass
        super(Taller, self).delete()

    def toJSON(self):
        item = model_to_dict(self)
        item['valor'] = f'{self.valor:.2f}'
        item['order'] = self.get_full_order()
        item['subcircuit'] = self.get_full_name()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        return item

class Orderfuel(models.Model):

    personal = models.ForeignKey(Personal, on_delete=models.PROTECT, verbose_name='Personal')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT, verbose_name='Vehículo')
    km = models.IntegerField(default=0,  null=True, blank=True, verbose_name='Kilometraje de llegada del vehículo')
    valor = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    fuel = models.CharField(max_length=10, choices=FUEL_TYPE, default=FUEL_TYPE[0][0], verbose_name='Tipo de combustible')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de Registro')

    def __str__(self):
        return self.get_full_name()
    
    def get_full_name(self):
        return f'({self.personal.user}) ({self.vehicle.type})'

    def get_short_name(self):
        return f'({self.personal.user}) ({self.vehicle.type})'
    
    def get_or_create_personal(self, name):
        personal = Personal()
        search = Personal.objects.filter(name=name)
        if search.exists():
            personal = search[0]
        else:
            personal.name = name
            personal.save()
        return personal
    
    def get_or_create_vehicle(self, name):
        vehicle = Vehicle()
        search = Vehicle.objects.filter(name=name)
        if search.exists():
            vehicle = search[0]
        else:
            vehicle.name = name
            vehicle.save()
        return vehicle
    
    def delete(self, using=None, keep_parents=False):
        try:
            os.remove(self.image.path)
        except:
            pass
        super(Orderfuel, self).delete()

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.get_full_name()
        item['short_name'] = self.get_short_name()
        item['personal'] = self.personal.toJSON()
        item['vehicle'] = self.vehicle.toJSON()
        return item