import django.dispatch
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Product, ProductOptions


# @receiver(pre_save, sender=ProductOptions)
# def my_handler(sender, **kwargs):
#     print(kwargs)
#     print(kwargs['instance'].__dict__, '-------------------------------------------------------')
#     print(kwargs['instance'], '-------------------------------------------------------')
#     # print(kwargs['instance'].product_id)