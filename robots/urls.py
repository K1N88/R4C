from django.urls import path
from .views import add_robot, export_report


urlpatterns = [
    path('add_robot/', add_robot, name='add_robot'),
    path('export_report/', export_report, name='export_report'),
]
