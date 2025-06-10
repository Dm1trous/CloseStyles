from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from .models import Stock, clothes


@receiver([post_save, post_delete], sender=Stock)
def update_product_status_on_stock_change(sender, instance, **kwargs):
    product = instance.product

    total_quantity = Stock.objects.filter(product=product).aggregate(
        total=Sum('quantity')
    )['total']

    if total_quantity is None or total_quantity <= 0:
        if product.statuss is True:
            product.statuss = False
            product.save(update_fields=['statuss'])
    else:
        if product.statuss is False:
            product.statuss = True
            product.save(update_fields=['statuss'])