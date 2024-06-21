from django.db import models
from django.core.exceptions import ValidationError
from accounts.utils import convert_currency
from accounts.constants import (
    DEBIT,
    CREDIT,
    TRANSACTION_TYPE_CHOICES,
    TRANSACTION_STATUS_SUCCESS,
    TRANSACTION_STATUS_FAILED,
    TRANSACTION_STATUS_CHOICES,
)


class Account(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    preferred_currency = models.CharField(max_length=5, default="EUR")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def update_wallet_currency(self, new_currency):
        """
        Update the currency of the associated wallet.
        """
        if hasattr(self, "wallet"):
            self.wallet.currency = new_currency
            self.wallet.save()
        else:
            raise ValueError("This account does not have a wallet.")


class Wallet(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.00)
    currency = models.CharField(max_length=5, default="EUR")

    def __str__(self):
        return f"Wallet of account {self.account}: {self.currency} {self.balance}"


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_time = models.DateTimeField(auto_now_add=True)
    transaction_amount = models.FloatField(default=0.00)
    transaction_amount_currency = models.CharField(max_length=5, default="EUR")
    transaction_type = models.CharField(
        max_length=10, choices=TRANSACTION_TYPE_CHOICES, default=DEBIT
    )
    transaction_status = models.CharField(
        max_length=10,
        choices=TRANSACTION_STATUS_CHOICES,
        default=TRANSACTION_STATUS_SUCCESS,
    )
    current_balance = models.FloatField(default=0.00)

    def __str__(self):
        return f"Transaction of {self.transaction_amount} {self.transaction_amount_currency} for {self.account.email} at {self.transaction_time}"

    def save(self, *args, **kwargs):
        # Retrieve the wallet associated with the account
        wallet = Wallet.objects.get(account=self.account)

        # Convert transaction amount to wallet's currency
        try:
            converted_amount = convert_currency(
                self.transaction_amount,
                self.transaction_amount_currency,
                wallet.currency,
            )
        except ValueError as e:
            raise ValidationError(str(e))

        # Calculate new balance after the transaction
        if self.transaction_type == DEBIT:
            if wallet.balance < converted_amount:
                self.transaction_status = TRANSACTION_STATUS_FAILED
                # If the balance is insufficient, do not modify the balance
                new_balance = wallet.balance
            else:
                new_balance = wallet.balance - converted_amount
        else:  # CREDIT
            new_balance = wallet.balance + converted_amount

        # Update wallet balance if the transaction is successful
        if self.transaction_status != TRANSACTION_STATUS_FAILED:
            wallet.balance = new_balance
            wallet.save()

        # Set current balance after the transaction
        self.current_balance = new_balance

        # Log the transaction
        self.log_transaction(wallet, wallet.balance, converted_amount)

        # Call the superclass's save() method
        super().save(*args, **kwargs)

    def log_transaction(self, wallet, balance_before, converted_amount):
        TransactionLog.objects.create(
            account=self.account,
            transaction_type=self.transaction_type,
            transaction_status=self.transaction_status,
            transaction_amount=self.transaction_amount,
            transaction_currency=self.transaction_amount_currency,
            converted_amount=converted_amount,
            wallet_currency=wallet.currency,
            current_balance=self.current_balance,
        )


class TransactionLog(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    wallet_currency = models.CharField(max_length=5, default="EUR")
    transaction_time = models.DateTimeField(auto_now=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    transaction_currency = models.CharField(max_length=5, default="EUR")
    transaction_amount = models.FloatField()
    converted_amount = models.FloatField(null=True)
    transaction_status = models.CharField(
        max_length=10,
        choices=TRANSACTION_STATUS_CHOICES,
        default=TRANSACTION_STATUS_SUCCESS,
    )
    current_balance = models.FloatField()

def save(self, *args, **kwargs):
    # Format transaction_amount, converted_amount, and current_balance to have 2 digits after the decimal point
    if isinstance(self.transaction_amount, (float, int)):
        self.transaction_amount = "{:.2f}".format(self.transaction_amount)
    if self.converted_amount is not None and isinstance(self.converted_amount, (float, int)):
        self.converted_amount = "{:.2f}".format(self.converted_amount)
    if isinstance(self.current_balance, (float, int)):
        self.current_balance = "{:.2f}".format(self.current_balance)

    super().save(*args, **kwargs)

    def __str__(self):
        return f"TransactionLog for {self.account.email} at {self.transaction_time}"
