from orders.signals import message
from .models import Robot, Order


@receiver(post_save, sender=Robot)
def check_order(sender, instance, created, **kwargs):
    if not created:
        orders = Order.objects.filter(robot=instance, status='in_progress')
        if orders.exists():
            message(orders.first().customer.email, instance)
