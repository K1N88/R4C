from django.urls import path
from .views import add_robot, week_report


urlpatterns = [
    path('add_robot/', add_robot, name='add_robot'),
    path('week_report/', week_report, name='week_report'),
]
