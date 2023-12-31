from datetime import datetime, timedelta, date
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
import json
import jsonschema
from openpyxl import Workbook

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


def export_report(request):
    robots = Robot.objects.filter(
        created__gte=datetime.now()-timedelta(days=7)
    ).values('model', 'version').annotate(count=Count('id'))
    models = robots.values('model').annotate(count=Count('id'))
    wb = Workbook()

    for model in models:
        ws = wb.create_sheet(title=model['model'])
        ws.append(['Модель', 'Версия', 'Количество за неделю'])
        data = robots.filter(model=model['model'])
        for row in data:
            ws.append([row['model'], row['version'], row['count']])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="{}_robots.xlsx"'.format(date.today())
    wb.save(response)

    return response
