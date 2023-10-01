from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError

from .forms import RobotForm


@csrf_exempt
def add_robot(request):
    if request.method == 'POST':
        form = RobotForm(request.POST or None)
        print(form.validate())
        try:
            if form.is_valid():
                robot = form.save()
                return HttpResponse(f'robot_id {str(robot.id)}', status=201)
            else:
                return HttpResponse(form.is_valid(), status=400)
        except Exception as e:
            return HttpResponse(str(e), status=400)
    else:
        return HttpResponse('Invalid request method', status=405)
