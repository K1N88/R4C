from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
import openpyxl

from .forms import RobotForm
from .models import Robot


@csrf_exempt
def add_robot(request):
    if request.method == 'POST':
        form = RobotForm(request.POST or None)
        try:
            if form.is_valid():
                robot = form.save(commit=False)
                robot.serial = robot.model + '-' + robot.version
                robot.save()
                return HttpResponse(f'create robot {str(robot.id)}', status=201)
            else:
                errors = form.errors
                return HttpResponse(form.is_valid(), status=400)
        except Exception as e:
            return HttpResponse(str(e), status=400)
    else:
        return HttpResponse('Invalid request method', status=405)


def export_report(request):
    robots = Robot.objects.filter(created__gte=datetime.now()-timedelta(days=7)).values('model', 'version').annotate(count=Count('id'))
    models = robots.values('model').annotate(count=Count('id')
                                             
    wb = openpyxl.Workbook()

    for model in models:
        ws = wb.create_sheet(title=robot['model'])
        ws.append(['Модель', 'Версия', 'Количество за неделю'])
        data = robots.filter(model=model.model)
        for row in data:
            ws.append([row['model'], row['version'], row['count']])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="robots.xlsx"'
    wb.save(response)

    return response
