from django.urls import path
from .views import add_robot


urlpatterns = [
    path('add_robot/', add_robot),
]
