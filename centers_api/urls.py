
from django.urls import path

from . import views

urlpatterns = [
    path('centers_detail/', views.CentersDetailView.as_view()),
    path('devices/', views.DevicesView.as_view())
]