import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.pos.forms import SubCircuit, SubcircuitForm
from core.security.mixins import PermissionMixin

class SubCircuitListView(PermissionMixin, ListView):
    model = SubCircuit
    template_name = 'crm/subcircuit/list.html'
    permission_required = 'view_subcircuit'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('subcircuit_create')
        context['title'] = 'Listado de sub circuitos'
        return context

class SubCircuitCreateView(PermissionMixin, CreateView):
    model = SubCircuit
    template_name = 'crm/subcircuit/create.html'
    form_class = SubcircuitForm
    success_url = reverse_lazy('subcircuit_list')
    permission_required = 'add_subcircuit'

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
        context['title'] = 'Nuevo registro de un sub circuito'
        context['action'] = 'add'
        return context

class SubCircuitUpdateView(PermissionMixin, UpdateView):
    model = SubCircuit
    template_name = 'crm/subcircuit/create.html'
    form_class = SubcircuitForm
    success_url = reverse_lazy('subcircuit_list')
    permission_required = 'change_subcircuit'

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
                queryset = SubCircuit.objects.all().exclude(id=self.get_object().id)
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
        context['title'] = 'Edición de un sub circuito'
        context['action'] = 'edit'
        return context

class SubCircuitDeleteView(PermissionMixin, DeleteView):
    model = SubCircuit
    template_name = 'crm/subcircuit/delete.html'
    success_url = reverse_lazy('subcircuit_list')
    permission_required = 'delete_subcircuit'

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
