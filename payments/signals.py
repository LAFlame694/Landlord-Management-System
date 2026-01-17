from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from payments.models import Payment

@receiver(post_save, sender=Payment)
def update_rent_record_on_payment(sender, instance, **kwargs):
    instance.rent_record.recalculate_payment_status()

@receiver(post_delete, sender=Payment)
def update_rent_record_on_payment_delete(sender, instance, **kwargs):
    instance.rent_record.recalculate_payment_status()