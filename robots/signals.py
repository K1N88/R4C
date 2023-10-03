from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.signals import message
from .models import Robot, Order


@receiver(post_save, sender=Robot)
def check_order(sender, instance, created, **kwargs):
    if created:
        orders = Order.objects.filter(robot=instance)
        if orders.exists():
            message(orders.first().customer.email, instance)
