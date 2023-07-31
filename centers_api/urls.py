
from django.urls import path

from . import views

urlpatterns = [
    path('centers/<id>/', views.CentersDetailView.as_view()),
    path('centers/', views.CentersListView.as_view()),
    
    path('devices/<id>/', views.DevicesDetailView.as_view()),
    path('devices/', views.DevicesListView.as_view()),

    path('events/', views.EventsListView.as_view()),
    path('events/<id>/', views.EventsDetailView.as_view()),
    path('events/search/<device_id>/', views.EventsFilteredView.as_view()),
]