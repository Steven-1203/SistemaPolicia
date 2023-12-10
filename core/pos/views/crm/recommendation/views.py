import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.pos.forms import Recommendation, RecommendationForm
from core.security.mixins import PermissionMixin

class RecommendationListView(PermissionMixin, ListView):
    model = Recommendation
    template_name = 'crm/recommendation/list.html'
    permission_required = 'view_recommendation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('recommendation_create')
        context['title'] = 'Listado de recomendaciones'
        return context

class RecommendationCreateView(PermissionMixin, CreateView):
    model = Recommendation
    template_name = 'crm/recommendation/create.html'
    form_class = RecommendationForm
    success_url = reverse_lazy('recommendation_list')
    permission_required = 'add_recommendation'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = Recommendation.objects.all()
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
        context['title'] = 'Nuevo registro de una recomendación'
        context['action'] = 'add'
        return context

class RecommendationUpdateView(PermissionMixin, UpdateView):
    model = Recommendation
    template_name = 'crm/recommendation/create.html'
    form_class = RecommendationForm
    success_url = reverse_lazy('recommendation_list')
    permission_required = 'change_recommendation'

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
                queryset = Recommendation.objects.all().exclude(id=self.get_object().id)
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

class RecommendationDeleteView(PermissionMixin, DeleteView):
    model = Recommendation
    template_name = 'crm/recommendation/delete.html'
    success_url = reverse_lazy('recommendation_list')
    permission_required = 'delete_recommendation'

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
