from rest_framework import serializers
from accounts.models import Account, Wallet, Transaction, TransactionLog
from django.core.exceptions import ValidationError


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"


class AccountDetailSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer()

    class Meta:
        model = Account
        fields = ["id", "first_name", "last_name", "email", "date_of_birth", "wallet"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class TransactionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionLog
        fields = "__all__"
