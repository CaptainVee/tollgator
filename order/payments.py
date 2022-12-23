from django.conf import settings
import json
import requests


def initiate_paystack_url(email, amount, transaction_ref, currency, callback_url):
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }
    email = email
    amount = amount * 100
    payload = json.dumps(
        {
            "email": email,
            "amount": str(amount),
            "currency": currency,
            "reference": transaction_ref,
            "callback_url": callback_url,
        }
    )
    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.content)
    # context = {"response" : response['data']['authorization_url']}


def verify_transaction(transaction_ref):

    url = f"https://api.paystack.co/transaction/verify/{transaction_ref}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }
    payload = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    return json.loads(response.content)
