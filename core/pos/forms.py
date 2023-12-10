from django.forms import ModelForm
from django import forms
from .models import *

class PersonalForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = User
        
        fields = '__all__'
        widgets = {    
            'names': forms.TextInput(attrs={'placeholder': 'Ingrese sus nombres'}),
            'dni': forms.TextInput(attrs={'placeholder': 'Ingrese su número de cédula'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ingrese su correo electrónico'}),
        }
        exclude = ['username', 'groups', 'password', 'date_joined', 'last_login', 'is_superuser', 'email_reset_token', 'is_active', 'is_staff', 'is_change_password', 'user_permissions']

    birthdate = forms.DateField(widget=forms.DateInput(
        attrs={
        'class': 'js-datepicker',
        'value': datetime.now().strftime('%Y-%m-%d'),
        }), label='Fecha de nacimiento')

    mobile = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese un teléfono celular',
        'autocomplete': 'off'
    }), max_length=10, label='Teléfono celular')

    citybirth = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese la ciudad de nacimiento',
        'autocomplete': 'off'
    }), max_length=500, label='Ciudad de nacimiento')

    grade = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese el grado',
        'autocomplete': 'off'
    }), max_length=500, label='Grado')
    
    typeblood = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese el tipo de sangre',
        'style': 'width: 100%;',
    }), max_length=500, label='Tipo de sangre')

class VehicleForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].widget.attrs['autofocus'] = True

    class Meta:
        model = Vehicle
        fields = '__all__'
        widgets = {

            'type': forms.TextInput(attrs={'placeholder': 'Ingrese el tipo de vehículo'}),
            'placa': forms.TextInput(attrs={'placeholder': 'Ingrese la placa del vehículo'}),
            'chasis': forms.TextInput(attrs={'placeholder': 'Ingrese el chasis del vehículo'}),
            'model': forms.TextInput(attrs={'placeholder': 'Ingrese el modelo del vehículo'}),
            'motor': forms.TextInput(attrs={'placeholder': 'Ingrese el motor del vehículo'}),
            'km': forms.TextInput(attrs={'placeholder': 'Ingrese el Kilometraje del vehículo'}),
            'cylinder': forms.TextInput(attrs={'placeholder': 'Ingrese el cilindrjae del vehículo'}),
            'capacitycarga': forms.TextInput(attrs={'placeholder': 'Ingrese la capacidad de carga'}),
            'capacitypeople': forms.TextInput(attrs={'placeholder': 'Ingrese la capacidad de pasajeros'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class DistrictForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = District
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese nombre del distrito'}),
            'code': forms.TextInput(attrs={'placeholder': 'Ingrese codigo del distrito'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class CircuitForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['district'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = Circuit
        fields = '__all__'
        widgets = {
            'district': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese nombre del distrito'}),
            'code': forms.TextInput(attrs={'placeholder': 'Ingrese codigo del distrito'}),
        }
        
    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class SubcircuitForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['circuit'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = SubCircuit
        fields = '__all__'
        widgets = {
            'circuit': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'personal': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'vehicle': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese nombre del distrito'}),
            'code': forms.TextInput(attrs={'placeholder': 'Ingrese codigo del distrito'}),
        }
    
    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class SuggestionForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = Suggestion
        fields = '__all__'
        widgets = {
            'names': forms.TextInput(attrs={'placeholder': 'Ingrese nombre del distrito'}),
            'subcircuit': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}), 
            'circuit': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}), 
            'email': forms.TextInput(attrs={'placeholder': 'Ingrese el correro electrònico'}),
            'mobile': forms.TextInput(attrs={'placeholder': 'Ingrese número de celular'}),
            'description': forms.TextInput(attrs={'placeholder': 'Ingrese la descripción'}),
            'date_joined': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'date_joined',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#date_joined'
            }),  
        }
        
        exclude = ['date_joined']
    
    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    
class RecommendationForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = Recommendation
        fields = '__all__'
        widgets = {
            'subcircuit': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}), 
            'description': forms.TextInput(attrs={'placeholder': 'Ingrese la descripción'}),
             'date_joined': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'date_joined',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#date_joined'
            }),  
        }
        exclude = ['date_joined']
    
    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class RequestsmaintenanceForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['typemaintenance'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = Requestsmaintenance
        fields = '__all__'
        widgets = {
            'typemaintenance': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'observations': forms.Textarea(attrs={'placeholder': 'Ingrese las observaciones'}),
            'km': forms.TextInput(attrs={'placeholder': 'Ingrese el Kilometraje del vehículo'}),
            'personal': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'vehicle': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
        }
    
    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class OrdermaintenanceForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['requests'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = Ordermaintenance
        fields = '__all__'
        widgets = {
            'requests': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'description': forms.Textarea(attrs={'placeholder': 'Ingrese las observaciones'}),
            'progress': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            
        }
    
    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class TallerForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['state'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = Taller
        fields = '__all__'
        widgets = {
            'number': forms.TextInput(attrs={'placeholder': 'Ingrese un número de factura', 'class': 'form-control', 'autocomplete': 'off'}),
            'valor': forms.TextInput(attrs={'placeholder': 'Ingrese un número de factura', 'class': 'form-control', 'autocomplete': 'off'}),       
            'description': forms.Textarea(attrs={'placeholder': 'Ingrese las observaciones'}),
            'state': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'order': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'subcircuit': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'date_joined': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'date_joined',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#date_joined'
            }),  
        }
        
        exclude = ['date_joined']
    
    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data
