from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import Account, Wallet, Transaction, TransactionLog
from accounts.serializers import (
    AccountSerializer,
    WalletSerializer,
    TransactionSerializer,
    TransactionLogSerializer,
    AccountDetailSerializer,
)
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.permissions import (
    IsAuthenticated,
)  # Import IsAuthenticated permission
from rest_framework_simplejwt.authentication import (
    JWTAuthentication,
)  # Import JWTAuthentication

from django.db import IntegrityError


class CreateAccountView(APIView):
    """
    API view to create a new account.

    Requires authentication.

    Methods:
    - post(request): Create a new account.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            serializer = AccountSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response(
                {"message": "Account already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete an existing account.

    Requires authentication.

    Methods:
    - get(request, *args, **kwargs): Retrieve account details.
    - put(request, *args, **kwargs): Update account details.
    - delete(request, *args, **kwargs): Delete the account.
    """

    authentication_classes = [
        JWTAuthentication
    ]  # Add JWTAuthentication for authentication
    permission_classes = [IsAuthenticated]  # Add IsAuthenticated permission

    queryset = Account.objects.all()
    serializer_class = AccountDetailSerializer

    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Http404:
            return Response(
                {"message": "Account not found."}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # Check if 'preferred_currency' is in request.data
            if "preferred_currency" in request.data:
                new_currency = request.data["preferred_currency"]
                instance.update_wallet_currency(new_currency)

            return Response(serializer.data)
        except Http404:
            return Response(
                {"message": "Account not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            return Response(
                {"message": "No such account found."}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            instance.delete()
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(
            {"message": "Account deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class Transaction(APIView):
    """
    API view to retrieve or create transactions.

    Requires authentication.

    Methods:
    - get(request): Retrieve transactions.
    - post(request): Create a new transaction.
    """

    authentication_classes = [
        JWTAuthentication
    ]  # Add JWTAuthentication for authentication
    permission_classes = [IsAuthenticated]  # Add IsAuthenticated permission

    def get(self, request):
        try:
            transactions = Transaction.objects.all()
            serializer = TransactionSerializer(transactions, many=True)
            return Response(serializer.data)
        except Http404:
            return Response(
                {"message": "Transaction not found."}, status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountTransactionList(ListAPIView):
    """
    API view to list transactions associated with a specific account.

    Requires authentication.

    Methods:
    - list(request, *args, **kwargs): List transactions for the account.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionLogSerializer

    def get_queryset(self):
        account_id = self.kwargs.get(
            "account_id"
        )  # Get the account_id from URL parameters
        account = get_object_or_404(
            Account, id=account_id
        )  # Retrieve the account object
        return TransactionLog.objects.filter(
            account=account
        )  # Filter transactions by account

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            return Response(
                {"message": "Transactions for this account not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


class TransactionListAPIView(ListAPIView):
    """
    API view to list all transactions.

    Requires authentication.

    Methods:
    - get_queryset(): Retrieve all transactions.
    """

    authentication_classes = [
        JWTAuthentication
    ]  # Add JWTAuthentication for authentication
    permission_classes = [IsAuthenticated]  # Add IsAuthenticated permission

    serializer_class = TransactionLogSerializer

    def get_queryset(self):
        try:
            return TransactionLog.objects.all()
        except Http404:
            return Response(
                {"message": "Transactions not found."}, status=status.HTTP_404_NOT_FOUND
            )


class AccountBalanceAPIView(APIView):
    """
    API view to retrieve the balance of a specific account.

    Requires authentication.

    Methods:
    - get(request, account_id): Retrieve the balance of the account.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, account_id):
        try:
            account = Account.objects.get(id=account_id)
            wallet = Wallet.objects.get(account=account)
            owner_details = {
                "first_name": account.first_name,
                "last_name": account.last_name,
                "email": account.email,
                "date_of_birth": account.date_of_birth,
            }
            return Response(
                {"account_owner": owner_details, "wallet currency": wallet.currency,"balance": wallet.balance},
                status=status.HTTP_200_OK,
            )
        except Account.DoesNotExist:
            return Response(
                {"error": f"Account with id {account_id} does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Wallet.DoesNotExist:
            return Response(
                {"error": f"Wallet for account with id {account_id} does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AccountListAPIView(APIView):
    """
    API view to retrieve a list of all accounts.

    Requires authentication.

    Methods:
    - get(request): Retrieve a list of all accounts.
    - get_queryset(): Retrieve queryset of all accounts.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer

    def get(self, request):
        try:
            queryset = self.get_queryset()
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_queryset(self):
        return Account.objects.all()
