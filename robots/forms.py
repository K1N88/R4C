from django import forms
from .models import Robot


class RobotForm(forms.Form):
    class Meta:
        model = Robot
        fields = ('model', 'version', 'created')
