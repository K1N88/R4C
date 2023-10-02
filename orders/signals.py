from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Robot, Order


def message(email, robot):
    send_mail(
        'Добрый день!',
        'Недавно вы интересовались нашим роботом модели {}, версии {}.'.format(
            robot.model, robot.version
        ),
        'Этот робот теперь в наличии.'
        'Если вам подходит этот вариант - пожалуйста, свяжитесь с нами',
        [email],
        fail_silently=False,
    )


@receiver(post_save, sender=Order)
def check_robot(sender, instance, created, **kwargs):
    if created:
        robots = Robot.objects.filter(
            model=instance.model, version=instance.version
        ).exclude(order__status='in_progress')
        if robots.exists():
            message(instance.customer.email, robots.first())
