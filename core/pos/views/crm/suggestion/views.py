import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.pos.forms import Suggestion, SuggestionForm
from core.security.mixins import PermissionMixin

class SuggestionListView(PermissionMixin, ListView):
    model = Suggestion
    template_name = 'crm/suggestion/list.html'
    permission_required = 'view_suggestion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('suggestion_create')
        context['title'] = 'Listado de sugerencias'
        return context

class SuggestionCreateView(CreateView):
    model = Suggestion
    template_name = 'crm/suggestion/create.html'
    form_class = SuggestionForm
    success_url = reverse_lazy('suggestion_list')
    permission_required = 'add_suggestion'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = Suggestion.objects.all()
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
        context['title'] = 'Nuevo registro de una sugerencia'
        context['action'] = 'add'
        return context

class SuggestionUpdateView(PermissionMixin, UpdateView):
    model = Suggestion
    template_name = 'crm/suggestion/create.html'
    form_class = SuggestionForm
    success_url = reverse_lazy('suggestion_list')
    permission_required = 'change_suggestion'

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
                queryset = Suggestion.objects.all().exclude(id=self.get_object().id)
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
        context['title'] = 'Edición de una sugerencia'
        context['action'] = 'edit'
        return context

class SuggestionDeleteView(PermissionMixin, DeleteView):
    model = Suggestion
    template_name = 'crm/suggestion/delete.html'
    success_url = reverse_lazy('suggestion_list')
    permission_required = 'delete_suggestion'

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
