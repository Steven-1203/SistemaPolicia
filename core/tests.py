from config.wsgi import *
import random
import string
from core.security.models import *
from django.contrib.auth.models import Permission
from core.pos.models import *

numbers = list(string.digits)

dashboard = Dashboard()
dashboard.name = 'SISPOL'
dashboard.icon = 'fa-solid fa-building-shield'
dashboard.layout = 1
dashboard.navbar = 'navbar-dark navbar-primary'
dashboard.sidebar = 'sidebar-dark-primary'
dashboard.save()

moduletype = ModuleType()
moduletype.name = 'Administración'
moduletype.icon = 'fas fa-address-book'
moduletype.save()
print(f'insertado {moduletype.name}')

module = Module()
module.module_type_id = 1
module.name = 'Personal'
module.url = '/pos/crm/personal/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-users'
module.description = 'Permite administrar los clientes del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=Personal._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 1
module.name = 'Vehiculos'
module.url = '/pos/crm/vehicle/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-car'
module.description = 'Permite administrar los vehículos del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=Vehicle._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 1
module.name = 'Distrito'
module.url = '/pos/crm/district/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-university'
module.description = 'Permite administrar los distritos del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=District._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 1
module.name = 'Circuito'
module.url = '/pos/crm/circuit/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-microchip'
module.description = 'Permite administrar los circuitos del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=Circuit._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 1
module.name = 'Sub Circuito'
module.url = '/pos/crm/subcircuit/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-magnet'
module.description = 'Permite administrar los sub circuitos del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=SubCircuit._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

moduletype = ModuleType()
moduletype.name = 'Informativo'
moduletype.icon = 'fas fa-info-circle'
moduletype.save()
print(f'insertado {moduletype.name}')

module = Module()
module.name = 'Sugerencias'
module.module_type_id = 2
module.url = '/pos/crm/suggestion/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-comments'
module.description = 'Permite administrar las sugerencias del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=Suggestion._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.name = 'Recomendaciones'
module.module_type_id = 2
module.url = '/pos/crm/recommendation/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-info-circle'
module.description = 'Permite administrar las recomendaciones del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=Recommendation._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

moduletype = ModuleType()
moduletype.name = 'Mantenimiento'
moduletype.icon = 'fas fa-wrench'
moduletype.save()
print(f'insertado {moduletype.name}')

module = Module()
module.module_type_id = 3
module.name = 'Solicitud'
module.url = '/pos/crm/requestsmaintenance/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-solid fa-bell'
module.description = 'Permite administrar las solcitudes de mantenimiento del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=Requestsmaintenance._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 3
module.name = 'Orden'
module.url = '/pos/crm/ordermaintenance/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-spinner'
module.description = 'Permite administrar las ordenes de mantenimiento del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=Ordermaintenance._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 3
module.name = 'Taller'
module.url = '/pos/crm/taller/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-list-alt'
module.description = 'Permite administrar los talleres del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=Taller._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

moduletype = ModuleType()
moduletype.name = 'Reportes'
moduletype.icon = 'fas fa-chart-pie'
moduletype.save()
print(f'insertado {moduletype.name}')

module = Module()
module.module_type_id = 4
module.name = 'Sugerencia'
module.url = '/reports/suggestion/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de las sugerencias'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 4
module.name = 'Recomendaciones'
module.url = '/reports/recommendation/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de las recomendaciones'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 4
module.name = 'Taller'
module.url = '/reports/taller/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de las talleres'
module.save()
print(f'insertado {module.name}')

moduletype = ModuleType()
moduletype.name = 'Seguridad'
moduletype.icon = 'fas fa-boxes'
moduletype.save()
print(f'insertado {moduletype.name}')

module = Module()
module.module_type_id = 5
module.name = 'Tipos de Módulos'
module.url = '/security/module/type/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-door-open'
module.description = 'Permite administrar los tipos de módulos del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=ModuleType._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 5
module.name = 'Módulos'
module.url = '/security/module/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-th-large'
module.description = 'Permite administrar los módulos del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=Module._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 5
module.name = 'Grupos'
module.url = '/security/group/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-users'
module.description = 'Permite administrar los grupos de usuarios del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=Group._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 5
module.name = 'Respaldos'
module.url = '/security/database/backups/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-database'
module.description = 'Permite administrar los respaldos de base de datos'
module.save()
for i in Permission.objects.filter(content_type__model=DatabaseBackups._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 5
module.name = 'Conf. Dashboard'
module.url = '/security/dashboard/update/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-tools'
module.description = 'Permite configurar los datos de la plantilla'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 5
module.name = 'Accesos'
module.url = '/security/access/users/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user-secret'
module.description = 'Permite administrar los accesos de los usuarios'
module.save()
for i in Permission.objects.filter(content_type__model=AccessUsers._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 5
module.name = 'Usuarios'
module.url = '/user/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-truck'
module.description = 'Permite administrar a los administradores del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=User._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.name = 'Cambiar password'
module.url = '/user/update/password/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-key'
module.description = 'Permite cambiar tu password de tu cuenta'
module.save()
print(f'insertado {module.name}')

module = Module()
module.name = 'Editar perfil'
module.url = '/user/update/profile/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-user'
module.description = 'Permite cambiar la información de tu cuenta'
module.save()
print(f'insertado {module.name}')

module = Module()
module.name = 'Editar perfil'
module.url = '/pos/crm/personal/update/profile/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-user'
module.description = 'Permite cambiar la información de tu cuenta'
module.save()
print(f'insertado {module.name}')

group = Group()
group.name = 'Administrador'
group.save()
print(f'insertado {group.name}')
for m in Module.objects.filter().exclude(url__in=['/pos/crm/personal/update/profile/']):
    gm = GroupModule()
    gm.module = m
    gm.group = group
    gm.save()
    for p in m.permits.all():
        group.permissions.add(p)
        grouppermission = GroupPermission()
        grouppermission.module_id = m.id
        grouppermission.group_id = group.id
        grouppermission.permission_id = p.id
        grouppermission.save()

group = Group()
group.name = 'Personal'
group.save()
print(f'insertado {group.name}')
for m in Module.objects.filter(url__in=['/pos/crm/personal/update/profile/', '/user/update/password/']).exclude():
    gm = GroupModule()
    gm.module = m
    gm.group = group
    gm.save()
    for p in m.permits.all():
        group.permissions.add(p)
        grouppermission = GroupPermission()
        grouppermission.module_id = m.id
        grouppermission.group_id = group.id
        grouppermission.permission_id = p.id
        grouppermission.save()

user = User()
user.names = 'Anderson Steven Criollo Arcos'
user.username = 'admin'
user.dni = ''.join(random.choices(numbers, k=10))
user.email = 'steven120338@gmail.com'
user.is_active = True
user.is_superuser = True
user.is_staff = True
user.set_password('admin')
user.save()
group = Group.objects.get(pk=1)
user.groups.add(group)
print(f'Bienvenido {user.names}')
