from django.urls import path
from core.pos.views.crm.personal.views import *
from core.pos.views.crm.vehicle.views import *
from core.pos.views.crm.district.views import *
from core.pos.views.crm.circuit.views import *
from core.pos.views.crm.subcircuit.views import *
from core.pos.views.crm.suggestion.views import *
from core.pos.views.crm.recommendation.views import *
from core.pos.views.crm.requestsmaintenance.views import *
from core.pos.views.crm.ordermaintenance.views import *
from core.pos.views.crm.taller.views import *
from core.pos.views.crm.orderfuel.views import *

urlpatterns = [
    # Personal
    path('crm/personal/', PersonalListView.as_view(), name='personal_list'),
    path('crm/personal/add/', PersonalCreateView.as_view(), name='personal_create'),
    path('crm/personal/update/<int:pk>/', PersonalUpdateView.as_view(), name='personal_update'),
    path('crm/personal/delete/<int:pk>/', PersonalDeleteView.as_view(), name='personal_delete'),
    path('crm/personal/update/profile/', PersonalUpdateProfileView.as_view(), name='personal_update_profile'),

    # Vehículo
    path('crm/vehicle/', VehicleListView.as_view(), name='vehicle_list'),
    path('crm/vehicle/add/', VehicleCreateView.as_view(), name='vehicle_create'),
    path('crm/vehicle/update/<int:pk>/', VehicleUpdateView.as_view(), name='vehicle_update'),
    path('crm/vehicle/delete/<int:pk>/', VehicleDeleteView.as_view(), name='vehicle_delete'),

    # Distrito
    path('crm/district/', DistrictListView.as_view(), name='district_list'),
    path('crm/district/add/', DistrictCreateView.as_view(), name='district_create'),
    path('crm/district/update/<int:pk>/', DistrictUpdateView.as_view(), name='district_update'),
    path('crm/district/delete/<int:pk>/', DistrictDeleteView.as_view(), name='district_delete'),
    
    # Circuito
    path('crm/circuit/', CircuitListView.as_view(), name='circuit_list'),
    path('crm/circuit/add/', CircuitCreateView.as_view(), name='circuit_create'),
    path('crm/circuit/update/<int:pk>/', CircuitUpdateView.as_view(), name='circuit_update'),
    path('crm/circuit/delete/<int:pk>/', CircuitDeleteView.as_view(), name='circuit_delete'),
    
    # Subcircuito
    path('crm/subcircuit/', SubCircuitListView.as_view(), name='subcircuit_list'),
    path('crm/subcircuit/add/', SubCircuitCreateView.as_view(), name='subcircuit_create'),
    path('crm/subcircuit/update/<int:pk>/', SubCircuitUpdateView.as_view(), name='subcircuit_update'),
    path('crm/subcircuit/delete/<int:pk>/', SubCircuitDeleteView.as_view(), name='subcircuit_delete'),
    
    # Sugerencias
    path('crm/suggestion/', SuggestionListView.as_view(), name='suggestion_list'),
    path('crm/suggestion/add/', SuggestionCreateView.as_view(), name='suggestion_create'),
    path('crm/suggestion/update/<int:pk>/', SuggestionUpdateView.as_view(), name='suggestion_update'),
    path('crm/suggestion/delete/<int:pk>/', SuggestionDeleteView.as_view(), name='suggestion_delete'),

    # Recomendaciones
    path('crm/recommendation/', RecommendationListView.as_view(), name='recommendation_list'),
    path('crm/recommendation/add/', RecommendationCreateView.as_view(), name='recommendation_create'),
    path('crm/recommendation/update/<int:pk>/', RecommendationUpdateView.as_view(), name='recommendation_update'),
    path('crm/recommendation/delete/<int:pk>/', RecommendationDeleteView.as_view(), name='recommendation_delete'),
    
    # Solcitudes de mantenimiento
    path('crm/requestsmaintenance/', RequestsmaintenanceListView.as_view(), name='requestsmaintenance_list'),
    path('crm/requestsmaintenance/add/', RequestsmaintenanceCreateView.as_view(), name='requestsmaintenance_create'),
    path('crm/requestsmaintenance/update/<int:pk>/', RequestsmaintenanceUpdateView.as_view(), name='requestsmaintenance_update'),
    path('crm/requestsmaintenance/delete/<int:pk>/', RequestsmaintenanceDeleteView.as_view(), name='requestsmaintenance_delete'),
    
    # Orden de mantenimiento
    path('crm/ordermaintenance/', OrdermaintenanceListView.as_view(), name='ordermaintenance_list'),
    path('crm/ordermaintenance/add/', OrdermaintenanceCreateView.as_view(), name='ordermaintenance_create'),
    path('crm/ordermaintenance/update/<int:pk>/', OrdermaintenanceUpdateView.as_view(), name='ordermaintenance_update'),
    path('crm/ordermaintenance/delete/<int:pk>/', OrdermaintenanceDeleteView.as_view(), name='ordermaintenance_delete'),
    
    # Taller
    path('crm/taller/', TallerListView.as_view(), name='taller_list'),
    path('crm/taller/add/', TallerCreateView.as_view(), name='taller_create'),
    path('crm/taller/update/<int:pk>/', TallerUpdateView.as_view(), name='taller_update'),
    path('crm/taller/delete/<int:pk>/', TallerDeleteView.as_view(), name='taller_delete'),

    # Combustible
    path('crm/orderfuel/', OrderfuelListView.as_view(), name='orderfuel_list'),
    path('crm/orderfuel/add/', OrderfuelCreateView.as_view(), name='orderfuel_create'),
    path('crm/orderfuel/update/<int:pk>/', OrderfuelUpdateView.as_view(), name='orderfuel_update'),
    path('crm/orderfuel/delete/<int:pk>/', OrderfuelDeleteView.as_view(), name='orderfuel_delete'),

]
