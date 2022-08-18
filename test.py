import asyncio
import time
from urllib.parse import parse_qs

import requests
from paynow import Paynow

users = {"wesley": "0785564315", "tanaka": "0777386229"}

paynow = Paynow(
    "14959",
    "6dc94c86-c5ce-40d1-ae8e-bff66e8c821b",
    "https://3dab-102-128-79-47.eu.ngrok.io/response",
    "https://3dab-102-128-79-47.eu.ngrok.io/response",
)

payment = paynow.create_payment("Order1", "wmambinge@gmail.com")
payment.add("Payment for 1 day subscription", 1)
response = paynow.send_mobile(payment, users["wesley"], "ecocash")
# response = paynow.send_mobile(payment, users["tanaka"], "ecocash")


def status_res(url):
    transaction_status = paynow.check_transaction_status(url)
    res = parse_qs(requests.get(url).text)
    print(f"{res}\n")
    status = res.get("status")[0]

    if status == "Sent":
        time.sleep(5)
        return status_res(url)

    return status, transaction_status.paid


if response.success == True:
    poll_url = response.poll_url
    # print("Poll Url: ", poll_url)

    payment_status = status_res(poll_url)

    # print(payment_status)

    if payment_status[1] == True:
        print("paid\n")
    else:
        print("failed\n")

    # print("Payment Status: ", response.status)
