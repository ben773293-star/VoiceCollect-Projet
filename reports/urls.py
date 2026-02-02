from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('supervisor/', views.supervisor_dashboard, name='supervisor_dashboard'),
    path('export-pdf/', views.export_pdf, name='export_pdf'),
    path('delete/<int:report_id>/', views.delete_report, name='delete_report'),
]