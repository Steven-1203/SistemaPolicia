import json

from django.contrib.auth.models import Group
from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.pos.forms import TallerForm, Taller
from django.views import View
from core.pos.models import *
from django.http import HttpResponse
from core.security.mixins import PermissionMixin

class TallerListView(PermissionMixin, ListView):
    model = Taller
    template_name = 'crm/taller/list.html'
    permission_required = 'view_taller'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('taller_create')
        context['title'] = 'Listado de taller'
        return context

class TallerCreateView(PermissionMixin,CreateView):
    model = Taller
    template_name = 'crm/taller/create.html'
    form_class = TallerForm
    success_url = reverse_lazy('taller_list')
    permission_required = 'add_taller'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = Taller.objects.all()
                type = request.POST['state']
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
        context['title'] = 'Nuevo registro de un taller'
        context['action'] = 'add'
        return context

class TallerUpdateView(PermissionMixin, UpdateView):
    model = Taller
    template_name = 'crm/taller/create.html'
    form_class = TallerForm
    success_url = reverse_lazy('taller_list')
    permission_required = 'change_taller'

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
                queryset = Taller.objects.all().exclude(id=self.get_object().id)
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
        context['title'] = 'Edición de un taller'
        context['action'] = 'edit'
        return context

class TallerDeleteView(PermissionMixin, DeleteView):
    model = Taller
    template_name = 'crm/taller/delete.html'
    success_url = reverse_lazy('taller_list')
    permission_required = 'delete_taller'

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
