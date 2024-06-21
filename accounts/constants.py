# Transaction type choices
DEBIT = "debit"
CREDIT = "credit"
TRANSACTION_TYPE_CHOICES = [
    (DEBIT, "Debit"),
    (CREDIT, "Credit"),
]

# Transaction status choices
TRANSACTION_STATUS_SUCCESS = "success"
TRANSACTION_STATUS_FAILED = "failed"
TRANSACTION_STATUS_CHOICES = [
    (TRANSACTION_STATUS_SUCCESS, "Success"),
    (TRANSACTION_STATUS_FAILED, "Failed"),
]


# Currency choices

# CURRENCY_CHOICES = (
#     ("USD", "United States Dollar ($)"),
#     ("EUR", "Euro (€)"),
#     ("GBP", "British Pound Sterling (£)"),
#     ("CHF", "Swiss Franc (CHF)"),
# )
