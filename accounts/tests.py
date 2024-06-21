from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from accounts.models import Account, Wallet, Transaction, TransactionLog
from accounts.serializers import (
    AccountSerializer,
    TransactionSerializer,
    TransactionLogSerializer,
    AccountDetailSerializer,
)
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from django.utils.timezone import now


class CreateAccountViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

    def test_create_account(self):
        url = reverse("create-account")
        data = {
            "username": "newuser",
            "password": "newpassword",
            "email": "new@example.com",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_account_existing(self):
        url = reverse("create-account")
        data = {
            "username": self.user.username,
            "password": "newpassword",
            "email": "new@example.com",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AccountDetailViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))
        self.account = Account.objects.create(
            username="testuser", email="test@example.com"
        )

    def test_get_account_detail(self):
        url = reverse("show-account", args=[self.account.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_account_detail_nonexistent(self):
        url = reverse("show-account", args=[1000])  # Non-existent account ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_account(self):
        url = reverse("show-account", args=[self.account.pk])
        data = {"username": "updatedusername"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_account_nonexistent(self):
        url = reverse("show-account", args=[1000])  # Non-existent account ID
        data = {"username": "updatedusername"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_account(self):
        url = reverse("show-account", args=[self.account.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_account_nonexistent(self):
        url = reverse("show-account", args=[1000])  # Non-existent account ID
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TransactionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

    def test_create_transaction(self):
        url = reverse("create-transaction")
        data = {"amount": 100, "description": "Test transaction", "timestamp": now()}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_transactions(self):
        url = reverse("create-transaction")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class AccountTransactionListTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))
        self.account = Account.objects.create(
            username="testuser", email="test@example.com"
        )
        self.transaction = Transaction.objects.create(
            amount=100, description="Test transaction"
        )
        self.transaction_log = TransactionLog.objects.create(
            account=self.account, transaction=self.transaction
        )

    def test_list_account_transactions(self):
        url = reverse("create-transaction", args=[self.account.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TransactionListAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))
        self.transaction = Transaction.objects.create(
            amount=100, description="Test transaction"
        )

    def test_list_transactions(self):
        url = reverse("transaction-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AccountBalanceAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))
        self.account = Account.objects.create(
            username="testuser", email="test@example.com"
        )
        self.wallet = Wallet.objects.create(account=self.account, balance=100)

    def test_get_account_balance(self):
        url = reverse("show-account", args=[self.account.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AccountListAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))
        self.account = Account.objects.create(
            username="testuser", email="test@example.com"
        )

    def test_list_accounts(self):
        url = reverse("account-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
