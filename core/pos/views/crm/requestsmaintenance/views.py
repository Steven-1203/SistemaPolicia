import json

from django.contrib.auth.models import Group
from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from core.pos.forms import RequestsmaintenanceForm, Requestsmaintenance
from core.security.mixins import ModuleMixin, PermissionMixin

class RequestsmaintenanceListView(PermissionMixin, ListView):
    model = Requestsmaintenance
    template_name = 'crm/requestsmaintenance/list.html'
    permission_required = 'view_requestsmaintenance'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('requestsmaintenance_create')
        context['title'] = 'Listado de solicitud de mantenimiento'
        return context

class RequestsmaintenanceCreateView(PermissionMixin, CreateView):
    model = Requestsmaintenance
    template_name = 'crm/requestsmaintenance/create.html'
    form_class = RequestsmaintenanceForm
    success_url = reverse_lazy('requestsmaintenance_list')
    permission_required = 'add_requestsmaintenance'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = Requestsmaintenance.objects.all()
                type = request.POST['typemaintenance']
                if type == 'name':
                    name = request.POST['name'].strip()
                    data['valid'] = not queryset.filter(name__iexact=name).exists()
                elif type == 'observations':
                    data['valid'] = not queryset.filter(observations__iexact=request.POST['observations']).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una solicitud de mantenimiento'
        context['action'] = 'add'
        return context

class RequestsmaintenanceUpdateView(PermissionMixin, UpdateView):
    model = Requestsmaintenance
    template_name = 'crm/requestsmaintenance/create.html'
    form_class = RequestsmaintenanceForm
    success_url = reverse_lazy('requestsmaintenance_list')
    permission_required = 'change_requestsmaintenance'

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
                queryset = Requestsmaintenance.objects.all().exclude(id=self.get_object().id)
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
        context['title'] = 'Edición de una solicitud de mantenimiento'
        context['action'] = 'edit'
        return context

class RequestsmaintenanceDeleteView(PermissionMixin, DeleteView):
    model = Requestsmaintenance
    template_name = 'crm/requestsmaintenance/delete.html'
    success_url = reverse_lazy('requestsmaintenance_list')
    permission_required = 'delete_requestsmaintenance'

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
