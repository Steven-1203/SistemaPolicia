import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.pos.forms import Circuit, CircuitForm
from core.security.mixins import PermissionMixin

class CircuitListView(PermissionMixin, ListView):
    model = Circuit
    template_name = 'crm/circuit/list.html'
    permission_required = 'view_circuit'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('circuit_create')
        context['title'] = 'Listado de circuitos'
        return context

class CircuitCreateView(PermissionMixin, CreateView):
    model = Circuit
    template_name = 'crm/circuit/create.html'
    form_class = CircuitForm
    success_url = reverse_lazy('circuit_list')
    permission_required = 'add_circuit'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un circuito'
        context['action'] = 'add'
        return context

class CircuitUpdateView(PermissionMixin, UpdateView):
    model = Circuit
    template_name = 'crm/circuit/create.html'
    form_class = CircuitForm
    success_url = reverse_lazy('circuit_list')
    permission_required = 'change_circuit'

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
                queryset = Circuit.objects.all().exclude(id=self.get_object().id)
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
        context['title'] = 'Edición de un circuito'
        context['action'] = 'edit'
        return context

class CircuitDeleteView(PermissionMixin, DeleteView):
    model = Circuit
    template_name = 'crm/circuit/delete.html'
    success_url = reverse_lazy('circuit_list')
    permission_required = 'delete_circuit'

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
