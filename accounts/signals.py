from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account, Wallet


@receiver(post_save, sender=Account)
def create_wallet(sender, instance, created, **kwargs):
    """
    Signal receiver function to create a Wallet when an Account is created,
    if a Wallet doesn't already exist for the Account.
    """
    if created and not hasattr(instance, "wallet"):
        Wallet.objects.create(account=instance, currency=instance.preferred_currency)
