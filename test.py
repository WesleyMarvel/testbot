from paynow import Paynow
import time
import asyncio

paynow = Paynow(
    '14959', 
    '6dc94c86-c5ce-40d1-ae8e-bff66e8c821b',
    'https://3dab-102-128-79-47.eu.ngrok.io/response',
    'https://3dab-102-128-79-47.eu.ngrok.io/response'
    )

payment = paynow.create_payment('Order1', 'wmambinge@gmail.com')
payment.add('Payment for 1 day subscription', 10)
response = paynow.send_mobile(payment, '0785564315', 'ecocash')
print (response)
if(response.success == True):
    
    poll_url = response.poll_url

    print("Poll Url: ", poll_url)

    status = paynow.check_transaction_status(poll_url)
    
    if status.paid == True:
        
        print("paid")

    

    print("Payment Status: ", response.status)