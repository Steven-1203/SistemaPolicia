import json

from django.contrib.auth.models import Group
from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from core.pos.forms import OrderfuelForm, Orderfuel
from core.security.mixins import ModuleMixin, PermissionMixin

class OrderfuelListView(PermissionMixin, ListView):
    model = Orderfuel
    template_name = 'crm/orderfuel/list.html'
    permission_required = 'view_orderfuel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('orderfuel_create')
        context['title'] = 'Listado de ordenes de combustible'
        return context

class OrderfuelCreateView(PermissionMixin, CreateView):
    model = Orderfuel
    template_name = 'crm/orderfuel/create.html'
    form_class = OrderfuelForm
    success_url = reverse_lazy('orderfuel_list')
    permission_required = 'add_orderfuel'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = Orderfuel.objects.all()
                type = request.POST['km']
                if type == 'name':
                    name = request.POST['name'].strip()
                    data['valid'] = not queryset.filter(name__iexact=name).exists()
                elif type == 'fuel':
                    data['valid'] = not queryset.filter(fuel__iexact=request.POST['fuel']).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una orden de combustible'
        context['action'] = 'add'
        return context

class OrderfuelUpdateView(PermissionMixin, UpdateView):
    model = Orderfuel
    template_name = 'crm/orderfuel/create.html'
    form_class = OrderfuelForm
    success_url = reverse_lazy('orderfuel_list')
    permission_required = 'change_orderfuel'

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
                queryset = Orderfuel.objects.all().exclude(id=self.get_object().id)
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
        context['title'] = 'Edición de una orden de combustible'
        context['action'] = 'edit'
        return context

class OrderfuelDeleteView(PermissionMixin, DeleteView):
    model = Orderfuel
    template_name = 'crm/orderfuel/delete.html'
    success_url = reverse_lazy('orderfuel_list')
    permission_required = 'delete_orderfuel'

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
