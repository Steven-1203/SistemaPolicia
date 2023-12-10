from django.urls import path
from .views.suggestion_report.views import SuggestionReportView
from .views.recommendation_report.views import RecommendationReportView
from .views.taller_report.views import TallerReportView

urlpatterns = [
    path('suggestion/', SuggestionReportView.as_view(), name='suggestion_report'),
    path('recommendation/', RecommendationReportView.as_view(), name='recommendation_report'),
    path('taller/', TallerReportView.as_view(), name='taller_report'),
]
