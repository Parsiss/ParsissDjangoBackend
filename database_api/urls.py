
from django.urls import path

from . import views

urlpatterns = [
    path('options/', views.GetOptions),
    path('report/filtered/', views.GetFilteredReport),
    path('report/upload/', views.UploadDB),
    
    path('rest/', views.PatientListView.as_view()),
    path('rest/<int:id>/', views.PatientDetailView.as_view()),

    path('jdsfl;ajsdflkjasdklfja;sdfjas/', views.ready)
]