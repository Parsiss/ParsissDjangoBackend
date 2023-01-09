from django.urls import path
from . import views

urlpatterns = [
    path('dated/', views.OperatorsDatedReportView.as_view()),
    path('success/', views.GetSuccessRateView),
    path('hospitals/', views.HospitalsDatedReportView.as_view()),
]