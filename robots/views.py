import json
import jsonschema
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Robot
from .schemas import ROBOT_SCHEMA


@csrf_exempt
def add_robot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            jsonschema.validate(data, ROBOT_SCHEMA)
            robot = Robot.objects.create(
                serial=data['model'] + '-' + data['version'],
                model=data['model'],
                version=data['version'],
                created=data['created']
            )
            return HttpResponse(f'created robot {robot.id}', status=201)
        except jsonschema.ValidationError as e:
            return HttpResponse(str(e), status=400)
        except Exception as e:
            return HttpResponse(str(e), status=400)
    else:
        return HttpResponse('Invalid request method', status=405)
