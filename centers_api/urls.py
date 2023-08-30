
from django.urls import path

from . import views

urlpatterns = [
    path('file/upload/', views.DeviceFilesUploadView.as_view()),
    path('file/delete/<id>/', views.DeviceFilesDeleteView.as_view()),

    path('centers/<id>/', views.CentersDetailView.as_view()),
    path('centers/', views.CentersListView.as_view()),
    
    path('devices/files/<device_id>/', views.DeviceFilesView.as_view()),
    path('devices/<id>/', views.DevicesDetailView.as_view()),
    path('devices/', views.DevicesListView.as_view()),

    path('events/', views.EventsListView.as_view()),
    path('events/<id>/', views.EventsDetailView.as_view()),
    path('events/search/<device_id>/', views.EventsFilteredView.as_view()),
]
