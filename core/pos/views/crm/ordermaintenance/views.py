import json

from django.contrib.auth.models import Group
from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from core.pos.forms import OrdermaintenanceForm, Ordermaintenance
from core.security.mixins import ModuleMixin, PermissionMixin

class OrdermaintenanceListView(PermissionMixin, ListView):
    model = Ordermaintenance
    template_name = 'crm/ordermaintenance/list.html'
    permission_required = 'view_ordermaintenance'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('ordermaintenance_create')
        context['title'] = 'Listado de orden de mantenimiento'
        return context

class OrdermaintenanceCreateView(PermissionMixin, CreateView):
    model = Ordermaintenance
    template_name = 'crm/ordermaintenance/create.html'
    form_class = OrdermaintenanceForm
    success_url = reverse_lazy('ordermaintenance_list')
    permission_required = 'add_ordermaintenance'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = Ordermaintenance.objects.all()
                type = request.POST['progress']
                if type == 'name':
                    name = request.POST['name'].strip()
                    data['valid'] = not queryset.filter(name__iexact=name).exists()
                elif type == 'description':
                    data['valid'] = not queryset.filter(description__iexact=request.POST['description']).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una oren de mantenimiento'
        context['action'] = 'add'
        return context

class OrdermaintenanceUpdateView(PermissionMixin, UpdateView):
    model = Ordermaintenance
    template_name = 'crm/ordermaintenance/create.html'
    form_class = OrdermaintenanceForm
    success_url = reverse_lazy('ordermaintenance_list')
    permission_required = 'change_ordermaintenance'

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
                queryset = Ordermaintenance.objects.all().exclude(id=self.get_object().id)
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
        context['title'] = 'Edición de una orden de mantenimiento'
        context['action'] = 'edit'
        return context

class OrdermaintenanceDeleteView(PermissionMixin, DeleteView):
    model = Ordermaintenance
    template_name = 'crm/ordermaintenance/delete.html'
    success_url = reverse_lazy('ordermaintenance_list')
    permission_required = 'delete_ordermaintenance'

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
