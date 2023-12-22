import json

from django.contrib.auth.models import Group
from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView

from config import settings
from core.pos.forms import PersonalForm, User, Personal
from core.security.mixins import ModuleMixin, PermissionMixin


class PersonalListView(PermissionMixin, TemplateView):
    template_name = 'crm/personal/list.html'
    permission_required = 'view_personal'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Personal.objects.filter():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('personal_create')
        context['title'] = 'Listado de personal'
        return context

class PersonalCreateView(PermissionMixin, CreateView):
    model = User
    template_name = 'crm/personal/create.html'
    form_class = PersonalForm
    success_url = reverse_lazy('personal_list')
    permission_required = 'add_personal'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                with transaction.atomic():
                    user = User()
                    user.names = request.POST['names']
                    user.dni = request.POST['dni']
                    user.username = user.dni
                    if 'image' in request.FILES:
                        user.image = request.FILES['image']
                    user.create_or_update_password(user.dni)
                    user.email = request.POST['email']
                    user.save()
                    personal = Personal()
                    personal.user_id = user.id
                    personal.mobile = request.POST['mobile']
                    personal.typeblood = request.POST['typeblood']
                    personal.citybirth = request.POST['citybirth']
                    personal.grade = request.POST['grade']
                    personal.birthdate = request.POST['birthdate']
                    personal.save()
                    group = Group.objects.get(pk=settings.GROUPS.get('personal'))
                    user.groups.add(group)
            elif action == 'validate_data':
                data = {'valid': True}
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                queryset = Personal.objects.all()
                if pattern == 'dni':
                    data['valid'] = not queryset.filter(user__dni=parameter).exists()
                elif pattern == 'mobile':
                    data['valid'] = not queryset.filter(mobile=parameter).exists()
                elif pattern == 'email':
                    data['valid'] = not queryset.filter(user__email=parameter).exists() 
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Personal'
        context['action'] = 'add'
        return context

class PersonalUpdateView(PermissionMixin, UpdateView):
    model = Personal
    template_name = 'crm/personal/create.html'
    form_class = PersonalForm
    success_url = reverse_lazy('personal_list')
    permission_required = 'change_personal'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = PersonalForm(instance=instance.user, initial={
            'mobile': instance.mobile,
            'typeblood': instance.typeblood,
            'citybirth': instance.citybirth,
            'grade': instance.grade,
            'birthdate': instance.birthdate,
        })
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                with transaction.atomic():
                    user = self.get_object().user
                    user.names = request.POST['names']
                    user.dni = request.POST['dni']
                    user.username = user.dni
                    if 'image-clear' in request.POST:
                        user.remove_image()
                    if 'image' in request.FILES:
                        user.image = request.FILES['image']
                    user.email = request.POST['email']
                    user.save()
                    personal = self.get_object()
                    personal.mobile = request.POST['mobile']
                    personal.typeblood = request.POST['typeblood']
                    personal.citybirth = request.POST['citybirth']
                    personal.grade = request.POST['grade']
                    personal.birthdate = request.POST['birthdate']
                    personal.save()
            elif action == 'validate_data':
                data = {'valid': True}
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                queryset = Personal.objects.all().exclude(id=self.get_object().id)
                if pattern == 'dni':
                    data['valid'] = not queryset.filter(user__dni=parameter).exists()
                elif pattern == 'mobile':
                    data['valid'] = not queryset.filter(mobile=parameter).exists()
                elif pattern == 'email':
                    data['valid'] = not queryset.filter(user__email=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Personal'
        context['action'] = 'edit'
        return context

class PersonalDeleteView(PermissionMixin, DeleteView):
    model = Personal
    template_name = 'crm/personal/delete.html'
    success_url = reverse_lazy('personal_list')
    permission_required = 'delete_personal'

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

class PersonalUpdateProfileView(ModuleMixin, UpdateView):
    model = User
    template_name = 'crm/personal/profile.html'
    form_class = PersonalForm
    success_url = settings.LOGIN_REDIRECT_URL

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = PersonalForm(instance=instance, initial={
            'mobile': instance.personal.mobile,
            'typeblood': instance.personal.typeblood,
            'citybirth': instance.personal.citybirth,
            'grade': instance.personal.grade,
            'birthdate': instance.personal.birthdate,
        })
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                with transaction.atomic():
                    user = self.get_object()
                    user.names = request.POST['names']
                    user.dni = request.POST['dni']
                    user.username = user.dni
                    if 'image-clear' in request.POST:
                        user.remove_image()
                    if 'image' in request.FILES:
                        user.image = request.FILES['image']
                    user.email = request.POST['email']
                    user.save()

                    personal = user.personal
                    personal.user_id = user.id
                    personal.mobile = request.POST['mobile']
                    personal.typeblood = request.POST['typeblood']
                    personal.citybirth = request.POST['citybirth']
                    personal.grade = request.POST['grade']
                    personal.birthdate = request.POST['birthdate']
                    personal.save()
            elif action == 'validate_data':
                data = {'valid': True}
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                queryset = Personal.objects.all().exclude(id=self.get_object().personal.id)
                if pattern == 'dni':
                    data['valid'] = not queryset.filter(user__dni=parameter).exists()
                elif pattern == 'mobile':
                    data['valid'] = not queryset.filter(mobile=parameter).exists()
                elif pattern == 'email':
                    data['valid'] = not queryset.filter(user__email=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de Perfil'
        context['action'] = 'edit'
        return context
