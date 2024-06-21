from django.urls import path
from accounts.views import (
    CreateAccountView,
    AccountDetailView,
    Transaction,
    AccountBalanceAPIView,
    AccountTransactionList,
    TransactionListAPIView,
    AccountListAPIView,
)

urlpatterns = [
    path("account/create/", CreateAccountView.as_view(), name="create-account"),
    path("account/<int:pk>/", AccountDetailView.as_view(), name="show-account"),
    path("transaction/", Transaction.as_view(), name="create-transaction"),
    path(
        "wallet/<int:account_id>/", AccountBalanceAPIView.as_view(), name="show-balance"
    ),
    path(
        "transaction/<int:account_id>/",
        AccountTransactionList.as_view(),
        name="create-transaction",
    ),
    path("transactions/", TransactionListAPIView.as_view(), name="transaction-list"),
    path("accounts/", AccountListAPIView.as_view(), name="account-list"),
]
