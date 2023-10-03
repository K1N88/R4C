from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import Order
from robots.models import Robot
from R4C.settings import EMAIL_HOST_USER


def message(email, robot):
    send_mail(
        '{} в наличии'.format(robot.serial),
        '''Добрый день!,
        Недавно вы интересовались нашим роботом модели {}, версии {}.
        Этот робот теперь в наличии.
        Если вам подходит этот вариант - пожалуйста, свяжитесь с нами'''.format(
            robot.model, robot.version
        ),
        EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )


@receiver(post_save, sender=Order)
def check_robot(sender, instance, created, **kwargs):
    if created:
        model, version = instance.robot_serial.split('-')
        robots = Robot.objects.filter(model=model, version=version)
        if robots.exists():
            message(instance.customer.email, robots.first())
