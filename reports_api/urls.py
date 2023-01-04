from django.urls import path
from . import views

urlpatterns = [
    path('dated/', views.MonthlyReportView.as_view()),
]