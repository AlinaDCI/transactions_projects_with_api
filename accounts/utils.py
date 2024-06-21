import requests
from django.conf import settings


def get_exchange_rate(from_currency, to_currency):
    api_key = settings.EXCHANGE_RATE_API_KEY
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["conversion_rates"].get(to_currency, None)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rates: {e}")
        return None


def convert_currency(amount, from_currency, to_currency):
    if from_currency == to_currency:
        return amount
    rate = get_exchange_rate(from_currency, to_currency)
    if rate is None:
        raise ValueError(
            f"Could not retrieve exchange rate from {from_currency} to {to_currency}"
        )
    return amount * rate
