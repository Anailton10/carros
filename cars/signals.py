from django.db.models import Sum
from django.db.models.signals import post_delete, post_save, pre_save  # noqa: E501
from django.dispatch import receiver

from cars.models import Car, CarInventory

# from openai_api.client import get_car_ai_bio


def cars_inventory_update():
    """
    Update inventory...
    """
    cars_count = Car.objects.all().count()
    cars_value = Car.objects.aggregate(total_value=Sum("value"))["total_value"]
    CarInventory.objects.create(cars_count=cars_count, cars_value=cars_value)


@receiver(pre_save, sender=Car)
def car_pre_save(sender, instance, **kwargs):
    if not instance.bio:
        instance.bio = "Bio criada via signals"
        # # ai_bio = get_car_ai_bio(instance.model, instance.brand, instance.year) # noqa: E501
        # instance.bio = ai_bio


@receiver(post_save, sender=Car)
def car_post_save(sender, instance, **kwargs):
    cars_inventory_update()


@receiver(post_delete, sender=Car)
def car_post_delete(sender, instance, **kwargs):
    cars_inventory_update()
