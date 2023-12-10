import json

from django.contrib.auth.models import Group
from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView


from core.pos.forms import VehicleForm, Vehicle
from core.security.mixins import ModuleMixin, PermissionMixin


class VehicleListView(PermissionMixin, ListView):
    model = Vehicle
    template_name = 'crm/vehicle/list.html'
    permission_required = 'view_vehicle'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('vehicle_create')
        context['title'] = 'Listado de vehículos'
        return context

class VehicleCreateView(PermissionMixin, CreateView):
    model = Vehicle
    template_name = 'crm/vehicle/create.html'
    form_class = VehicleForm
    success_url = reverse_lazy('vehicle_list')
    permission_required = 'add_vehicle'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = Vehicle.objects.all()
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                if pattern == 'name':
                    data['valid'] = not queryset.filter(name__iexact=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de vehículo'
        context['action'] = 'add'
        return context

class VehicleUpdateView(PermissionMixin, UpdateView):
    model = Vehicle
    template_name = 'crm/vehicle/create.html'
    form_class = VehicleForm
    success_url = reverse_lazy('vehicle_list')
    permission_required = 'change_vehicle'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = Vehicle.objects.all().exclude(id=self.get_object().id)
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                if pattern == 'name':
                    data['valid'] = not queryset.filter(name__iexact=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Vehículo'
        context['action'] = 'edit'
        return context

class VehicleDeleteView(PermissionMixin, DeleteView):
    model = Vehicle
    template_name = 'crm/vehicle/delete.html'
    success_url = reverse_lazy('vehicle_list')
    permission_required = 'delete_vehicle'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.get_object().delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context
