from flask import Flask, request, jsonify
from os import getenv
from heyoo import WhatsApp
from dotenv import load_dotenv
import datetime
from datetime import timedelta
from flask_mysqldb import MySQL
import os
import json
import requests
from paynow import Paynow
import random

app = Flask(__name__)
app.secret_key = "secret key"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'WesleyMambinge$kudzi'

mysql = MySQL(app)

messenger = WhatsApp('EAAUuI61kKewBAHPlDs1PT0uiNrfyRzbN4SuekMdIiQ2oNhsqr0auTQ80j29w95QsY1miEVbfn1HxBiI5ikRNiQ1KsEBJHXttAPHzegd5SHgPlOCdZAz1Juib6lZAFG6euucSEqWJTYXvIwkw5wbZCqrKiyZChhMBOnl0tD7chqbEEUUNDSaxdkKEjiRUoMtZAZCgpHsLMnVHXNXdnwxLTR6VVGJrcHZCkAZD', phone_number_id='101780209235905')
VERIFY_TOKEN = "Wesley13"
load_dotenv()

paynow = Paynow(
    '14959', 
    '6dc94c86-c5ce-40d1-ae8e-bff66e8c821b',
    'https://9931-102-128-79-47.eu.ngrok.io/response', 
    'https://9931-102-128-79-47.eu.ngrok.io/response'
    )

@app.route('/hook', methods=["GET", "POST"])
def hello():
    if request.method == "POST":
        enter = request.get_json()
        trimmed = enter['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
        resipient = enter['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']
        username = enter['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']
       

#Paynow Integration
        try:
            if "*2000*" in trimmed:
                wes = random.randint(1,29999)
                ref = "ref" + str(wes)
                payment = paynow.create_payment(ref, 'wmambinge@gmail.com')
                payment.add('Payment for 1 day subscription', 10)
                number = trimmed.replace("*2000*", "")
                response = paynow.send_mobile(payment, number, 'ecocash')
                if response.success == True:
                    poll_url = response.poll_url
                    status = paynow.check_transaction_status(poll_url)
                    print(status)
                    if status.paid:
                        start_date = datetime.datetime.now()
                        plus = start_date + timedelta(hours=24)
                        mycursor = mysql.connection.cursor()
                        mycursor.execute("UPDATE subscribers SET reg_time='%s' WHERE number='%s'" %(plus,resipient))
                        mysql.connection.commit()
                        mycursor = mysql.connection.cursor()
                        mycursor.execute("UPDATE subscribers SET status='paid' WHERE number='%s'" %(resipient))
                        mysql.connection.commit()
                        return(messenger.send_message(
                        message="Payment successful 1 day added",
                                recipient_id=resipient   
                        ))
                    else:
                        return(messenger.send_message(
                        message="Sorry it seems the transaction has failed",
                                recipient_id=resipient   
                        ))
                else:
                        return(messenger.send_message(
                        message="Sorry there is a network issue",
                                recipient_id=resipient   
                        ))
        except ConnectionError():
            return (messenger.send_message(
                            message="There seems to be a network challenge",
                            recipient_id=resipient
                            )
                    )
            
        try:
            if "*2100*" in trimmed:
                wes = random.randint(1,29999)
                ref = "ref" + str(wes)
                payment = paynow.create_payment(ref, 'wmambinge@gmail.com')
                payment.add('Payment for 1 week subscription', 11)
                number = trimmed.replace("*2000*", "")
                response = paynow.send_mobile(payment, '%s', 'ecocash'%number)
        except ConnectionError():
            return (messenger.send_message(
                            message="There seems to be a network challenge",
                            recipient_id=resipient
                            )
                    )
        try:    
            if "*2200*" in trimmed:
                wes = random.randint(1,29999)
                ref = "ref" + str(wes)
                payment = paynow.create_payment(ref, 'wmambinge@gmail.com')
                payment.add('Payment for 1 month subscription', 12)
                number = trimmed.replace("*2000*", "")
                response = paynow.send_mobile(payment, number, 'ecocash')
                
        except ConnectionError():
            return (messenger.send_message(
                            message="There seems to be a network challenge",
                            recipient_id=resipient
                            )
                    )

#Greeting messages section

        if "hi" == trimmed.lower():

            print(trimmed)

            mycursor = mysql.connection.cursor()
            mycursor.execute("SELECT name,number FROM subscribers WHERE number='%s'" %resipient)
            myresi = mycursor.fetchall()

            for r in myresi:
                if resipient in r[1]:
                    mycursor = mysql.connection.cursor()
                    mycursor.execute("SELECT img FROM headimg")

                    imgg = mycursor.fetchall()

                    for idc in imgg:
                        global idcf10

                        idcf10 = idc[0]
                        resp=messenger.send_message(
                            message= "Welcome back " + str(r[0]),
                            recipient_id=resipient
                            )

                    resp=messenger.send_message(
                        message= "_______________________\n*-ZIMBABWE-*\n*PROPERTY CLASSIFIEDS.*\n_______________________\nWelcome to Zimbabwe’s LITE classifieds for properties. Covering Houses, industrials, shops, stands, farms, hospitality etc.\n*Rentals, Sales and accommodation Bookings.*\n \n*S1*: View Houses to rent\n*S2*:  View Commercial/Shops to rent \n*S3*: View Farms to rent\n*S4*: View Industrials to rent\n*S5*:View Houses for sale\n*S6*:View Shops for sale\n*S7*:View Industrials for sale\n*S8*:View Farms for sale\n*S9*:View Stands for Sale\n*S10*:Request Valuation Service\n*S11*:HOLIDAY ACCOMMODATION\n*S12*:HOLIDAY ACCOMMODATION FOR SALE\n \n_______________________\n*PROPERTY ADVERTISERS*\nIf you wish to upload a property kindly send UPL1 or follow\n https://wa.me/263774767325?text=UPL1\n_______________________\nTo subscribe to regular morning news on property investments and tips, send SUBS1 or follow\nhttps://wa.me/263774767325?text=SUBS1",
                        recipient_id=resipient
                            )
                    return(resp)
            return(messenger.send_message(
                message="_______________________\n*-WELCOME-*\n*PROPERTY ADVERTS.*\n_______________________\nGreetings\n\nThis is C-Lite Zimbabwe. Would you kindly give me your name so that I recognise you every time we chat :-)\n\n*Simply enter* *name Full Name\n\n*Example>* *name Grace Chiwocha\n\n*Please include the '*' when adding your name\n\n*Example>* *name Grace Chiwocha",
                recipient_id=resipient
                    ))
               

        #Normal registration section
        elif "*name" in trimmed:

            mycursor = mysql.connection.cursor()

            mycursor.execute("SELECT img FROM headimg")

            imgg = mycursor.fetchall()

            for idc in imgg:
                global idcf12


                idcf12 = idc[0]


            mycursor = mysql.connection.cursor()

            mycursor.execute("SELECT img1 FROM headimg")

            imgg1 = mycursor.fetchall()

            for idc in imgg1:
                global idcf13


                idcf13 = idc[0]

            nam = trimmed.replace("*name", "")

            start_day = datetime.datetime.now()
            plus1 = start_day + timedelta(days=4)
            sqli = "INSERT INTO subscribers (name, number, reg_time, status) VALUES (%s, %s, %s, %s)"
            vali = (nam, resipient, plus1, "paid")
            mycursor = mysql.connection.cursor()
            mycursor.execute(sqli, vali)

            mysql.connection.commit()

            resp=messenger.send_message(
                message="_______________________\n*-WELCOME-*\n*PROPERTY ADVERTS.*\n_______________________\nThank you, %s\n\nCongratulations! You have been awarded 4 days of free access to the prime services. Proceed to explore our services in this chatbot.\n\n*Use the following format to subscribe now:*\n*2000*your Ecocash number# - Daily Sub $10ZWL\n*2100*your Ecocash number – Weekly Sub $40ZWL\n*2200*your Ecocash number# Monthly Sub $90ZWL"%nam,
                recipient_id=resipient
                    )
                
            resp=messenger.send_message(
                message="nice to meet you %s\n\n_______________________\n*-ZIMBABWE-*\n*PROPERTY CLASSIFIEDS.*\n_______________________\nWelcome to Zimbabwe’s LITE classifieds for properties. Covering Houses, industrials, shops, stands, farms, hospitality.\n*Rentals, Sales and accommodation Bookings.*\n \n*S1*: View Houses to rent\n*S2*:  View Commercial/Shops to rent \n*S3*: View Farms to rent\n*S4*: View Industrials to rent\n*S5*:View Houses for sale\n*S6*:View Shops for sale\n*S7*:View Industrials for sale\n*S8*:View Farms for sale\n*S9*:View Stands for Sale\n*S10*:Request Valuation Service\n*S11*:HOLIDAY ACCOMMODATION\n*S12*:HOLIDAY ACCOMMODATION FOR SALE\n \n_______________________\n*PROPERTY ADVERTISERS*\nIf you wish to upload a property kindly send UPL1 or follow\n https://wa.me/263774767325?text=UPL1\n_______________________\nTo subscribe to regular morning news on property investments and tips, send SUBS1 or follow\nhttps://wa.me/263774767325?text=SUBS1"%(nam),
                recipient_id=resipient
                )
            
            return(resp)
        
        if trimmed.lower() == "sr":

            mycursor = mysql.connection.cursor()

            mycursor.execute("SELECT img FROM headimg")

            imgg = mycursor.fetchall()

            for idc in imgg:
                global idcf11

                idcf11 = idc[0]

            mycursor = mysql.connection.cursor()

            mycursor.execute("SELECT img1 FROM headimg")

            imgg1 = mycursor.fetchall()

            for idc in imgg1:

                idcf15 = idc[0]

            dc = messenger.send_message(
                    message="_______________________\n*-ZIMBABWE-*\n*PROPERTY CLASSIFIEDS.*\n_______________________\nWelcome to Zimbabwe’s LITE classifieds for properties. Covering Houses, industrials, shops, stands, farms, hospitality.\n*Rentals, Sales and accommodation Bookings.*\n \n*S1*: View Houses to rent\n*S2*:  View Commercial/Shops to rent \n*S3*: View Farms to rent\n*S4*: View Industrials to rent\n*S5*:View Houses for sale\n*S6*:View Shops for sale\n*S7*:View Industrials for sale\n*S8*:View Farms for sale\n*S9*:View Stands for Sale\n*S10*:Request Valuation Service\n*S11*:HOLIDAY ACCOMMODATION\n*S12*:HOLIDAY ACCOMMODATION FOR SALE\n \n_______________________\n*PROPERTY ADVERTISERS*\nIf you wish to upload a property kindly send UPL1 or follow\n https://wa.me/263774767325?text=UPL1\n_______________________\nTo subscribe to regular morning news on property investments and tips, send SUBS1 or follow\nhttps://wa.me/263774767325?text=SUBS1",
                    recipient_id=resipient
                    )
                
            return (dc)

        elif trimmed.upper() == "SUBS1":

            mycursor = mysql.connection.cursor()

            mycursor.execute("SELECT img1 FROM headimg")

            imgg1 = mycursor.fetchall()

            for idc in imgg1:

                idcf15 = idc[0]

            dt = messenger.send_message(
                    message="*In order to view detailed info and be able to communicate with the advertisers directly.*\n_______________________\n*Use the following format to subscribe now:*\n*2000*your Ecocash number - Daily Sub $40ZWL\n*2100*your Ecocash number – Weekly Sub $270ZWL\n*2200*your Ecocash number Monthly Sub $972ZWL\nExample *2100*772345684",
                    recipient_id=resipient)
               
            return (dt)

        elif request.method =="POST":

            #Advert viewing section

            if trimmed.upper() == "S1":
                
                try:

                    mycursor = mysql.connection.cursor()
                    mycursor.execute("SELECT code,location,price,date FROM advert WHERE adcode='%s'" %trimmed.upper())
                    myresult = mycursor.fetchall()

                    # # sq=messenger.send_message(
                    #         message="Wait your information is loading\nEnter Advert code to view more details about the advert",
                    #         recipient_id=resipient
                    #         )

                    S1_list = []

                    str1 = "\n"

                    for row in myresult:

                        S1_list.append("*Advert Code* :" + row[0] + "\n" + "*Location* :" + row[1] + "\n" + row[2] +  "\n" + row[3] + "\n" + "\n")

                        real = str1.join(S1_list)

                    mycursor = mysql.connection.cursor()

                    mycursor.execute("SELECT img FROM headimg")

                    imgg = mycursor.fetchall()

                    for idc in imgg:
                        global idcf100

                        idcf100 = idc[0]
                    sq = messenger.send_message(
                            message=real,
                            recipient_id=resipient
                            )
                        

                    return (sq)
                
                except UnboundLocalError:

                    return (messenger.send_message(
                            message="*Oops* This advert code is still empty\nsend *SR* to return to main menu and try another one",
                            recipient_id=resipient
                            )
                    )

            elif trimmed.upper() == "S2":

                try:
                    mycursor = mysql.connection.cursor()
                    mycursor.execute("SELECT code,location,price,date FROM advert WHERE adcode='%s'" %trimmed.upper())
                    myresult = mycursor.fetchall()

                    sq=messenger.send_message(
                        message="Wait your information is loading\nEnter Advert code to view more details about the advert",
                        recipient_id=resipient
                            )

                    S2_list = []

                    str1 = "\n"

                    for row in myresult:


                        intiu = "*Advert Code* :" + row[0] + "\n" + "*Location* :" + row[1] + "\n" + row[2] +  "\n" + row[3] + "\n" + "\n"

                        S2_list.append(intiu)

                        real2 = str1.join(S2_list)

                    mycursor = mysql.connection.cursor()

                    mycursor.execute("SELECT img FROM headimg")

                    imgg = mycursor.fetchall()

                    for idc in imgg:
                        global idcf101

                        idcf101 = idc[0]
                    sq = messenger.send_message(
                            message=real2,
                            recipient_id=resipient
                            )
                        #sq.media(idcf101)

                    return (sq)
                except UnboundLocalError:

                    return (messenger.send_message(
                            message="*Oops* This advert code is still empty\nsend *SR* to return to main menu and try another one",
                            recipient_id=resipient
                            )

                    )
            elif trimmed.upper() == "S3":

                try:
                    mycursor = mysql.connection.cursor()
                    mycursor.execute("SELECT code,location,price,date FROM advert WHERE adcode='%s'" %trimmed.upper())
                    myresult = mycursor.fetchall()

                    messenger.send_message(
                            message="Wait your information is loading\nEnter Advert code to view more details about the advert",
                            recipient_id=resipient
                            )

                    S3_list = []

                    str1 = "\n"

                    for row in myresult:


                        intiu = "*Advert Code* :" + row[0] + "\n" + "*Location* :" + row[1] + "\n" + row[2] +  "\n" + row[3] + "\n" + "\n"

                        S3_list.append(intiu)

                        real3 = str1.join(S3_list)

                    mycursor = mysql.connection.cursor()

                    mycursor.execute("SELECT img FROM headimg")

                    imgg = mycursor.fetchall()

                    for idc in imgg:
                        global idcf102

                        idcf102 = idc[0]
                    sq = messenger.send_message(
                            message=real3,
                            recipient_id=resipient
                            )
                        #sq.media(idcf102)

                    return (sq)

                except UnboundLocalError:

                    return (messenger.send_message(
                            message="*Oops* This advert code is still empty\nsend *SR* to return to main menu and try another one",
                            recipient_id=resipient)
                            )
                            
            elif trimmed.upper() == "S4":

                try:
                    mycursor = mysql.connection.cursor()
                    mycursor.execute("SELECT code,location,price,date FROM advert WHERE adcode='%s'" %trimmed.upper())
                    myresult = mycursor.fetchall()

                    messenger.send_message(
                            message="Wait your information is loading\nEnter Advert code to view more details about the advert",
                            recipient_id=resipient
                            )

                    S4_list = []

                    str1 = "\n"

                    for row in myresult:


                        intiu = "*Advert Code* :" + row[0] + "\n" + "*Location* :" + row[1] + "\n" + row[2] +  "\n" + row[3] + "\n" + "\n"

                        S4_list.append(intiu)

                        real4 = str1.join(S4_list)

                    mycursor = mysql.connection.cursor()

                    mycursor.execute("SELECT img FROM headimg")

                    imgg = mycursor.fetchall()

                    for idc in imgg:
                        global idcf103

                        idcf103 = idc[0]
                    sq = messenger.send_message(
                            message=real4,
                            recipient_id=resipient
                            )
                        #sq.media(idcf103)
                    return (sq)

                except UnboundLocalError:

                    return (messenger.send_message(
                            message="*Oops* This advert code is still empty\nsend *SR* to return to main menu and try another one",
                            recipient_id=resipient
                            )

                        )

            elif trimmed.upper() == "S5":

                try:
                    mycursor = mysql.connection.cursor()
                    mycursor.execute("SELECT code,location,price,date FROM advert WHERE adcode='%s'" %trimmed.upper())
                    myresult = mycursor.fetchall()

                    messenger.send_message(
                            message="Wait your information is loading\nEnter Advert code to view more details about the advert",
                            recipient_id=resipient
                            )

                    S5_list = []

                    str1 = "\n"

                    for row in myresult:


                        intiu = "*Advert Code* :" + row[0] + "\n" + "*Location* :" + row[1] + "\n" + row[2] +  "\n" + row[3] + "\n" + "\n"

                        S5_list.append(intiu)

                        real5 = str1.join(S5_list)

                    mycursor = mysql.connection.cursor()

                    mycursor.execute("SELECT img FROM headimg")

                    imgg = mycursor.fetchall()

                    for idc in imgg:
                        global idcf104

                        idcf104 = idc[0]
                    sq = messenger.send_message(
                            message=real5,
                            recipient_id=resipient)
                     
                    return str(sq)

                except UnboundLocalError:

                    return (messenger.send_message(
                            message="*Oops* This advert code is still empty\nsend *SR* to return to main menu and try another one",
                            recipient_id=resipient
                            )

                        )

            elif trimmed.upper() == "S6":

                try:
                    mycursor = mysql.connection.cursor()
                    mycursor.execute("SELECT code,location,price,date FROM advert WHERE adcode='%s'" %trimmed.upper())
                    myresult = mycursor.fetchall()

                    messenger.send_message(
                            message="Wait your information is loading\nEnter Advert code to view more details about the advert",
                            recipient_id=resipient
                            )

                    S6_list = []

                    str1 = "\n"

                    for row in myresult:


                        intiu = "*Advert Code* :" + row[0] + "\n" + "*Location* :" + row[1] + "\n" + row[2] +  "\n" + row[3] + "\n" + "\n"

                        S6_list.append(intiu)

                        real6 = str1.join(S6_list)

                    mycursor = mysql.connection.cursor()

                    mycursor.execute("SELECT img FROM headimg")

                    imgg = mycursor.fetchall()

                    for idc in imgg:
                        global idcf105

                        idcf105 = idc[0]
                    sq = messenger.send_message(
                            message=real6,
                            recipient_id=resipient
                            )
                        #sq.media(idcf105)
                    return (sq)

                except UnboundLocalError:

                    return (messenger.send_message(
                            message="*Oops* This advert code is still empty\nsend *SR* to return to main menu and try another one",
                            recipient_id=resipient
                            )
                        )

            elif trimmed.upper() == "S7":

                try:
                    mycursor = mysql.connection.cursor()
                    mycursor.execute("SELECT code,location,price,date FROM advert WHERE adcode='%s'" %trimmed.upper())
                    myresult = mycursor.fetchall()

                    messenger.send_message(
                            message="Wait your information is loading\nEnter Advert code to view more details about the advert",
                            recipient_id=resipient
                            )

                    S7_list = []

                    str1 = "\n"

                    for row in myresult:


                        intiu = "*Advert Code* :" + row[0] + "\n" + "*Location* :" + row[1] + "\n" + row[2] +  "\n" + row[3] + "\n" + "\n"

                        S7_list.append(intiu)

                        real7 = str1.join(S7_list)

                    mycursor = mysql.connection.cursor()

                    mycursor.execute("SELECT img FROM headimg")

                    imgg = mycursor.fetchall()

                    for idc in imgg:
                        global idcf106

                        idcf106 = idc[0]
                    sq = messenger.send_message(
                            message=real7,
                            recipient_id=resipient
                            )
                        #sq.media(idcf106)
                    return (sq)

                except UnboundLocalError:

                    return (messenger.send_message(
                            message="*Oops* This advert code is still empty\nsend *SR* to return to main menu and try another one",
                            recipient_id=resipient
                            )

                        )

            elif trimmed.upper() == "S8":

                try:
                    mycursor = mysql.connection.cursor()
                    mycursor.execute("SELECT code,location,price,date FROM advert WHERE adcode='%s'" %trimmed.upper())
                    myresult = mycursor.fetchall()

                    messenger.send_message(
                            message="Wait your information is loading\nEnter Advert code to view more details about the advert",
                            recipient_id=resipient
                            )

                    S8_list = []

                    str1 = "\n"

                    for row in myresult:


                        intiu = "*Advert Code* :" + row[0] + "\n" + "*Location* :" + row[1] + "\n" + row[2] +  "\n" + row[3] + "\n" + "\n"

                        S8_list.append(intiu)

                        real8 = str1.join(S8_list)

                    mycursor = mysql.connection.cursor()

                    mycursor.execute("SELECT img FROM headimg")

                    imgg = mycursor.fetchall()

                    for idc in imgg:
                        global idcf107

                        idcf107 = idc[0]
                    sq = messenger.send_message(
                            message=real8,
                            recipient_id=resipient
                            )
                        #sq.media(idcf107)
                    return (sq)

                except UnboundLocalError:

                    messenger.send_message(
                            message="*Oops* This advert code is still empty\nsend *SR* to return to main menu and try another one",
                            recipient_id=resipient
                            )

            elif trimmed.upper() == "S9":

                try:
                    mycursor = mysql.connection.cursor()
                    mycursor.execute("SELECT code,location,price,date FROM advert WHERE adcode='%s'" %trimmed.upper())
                    myresult = mycursor.fetchall()

                    messenger.send_message(
                            message="Wait your information is loading\nEnter Advert code to view more details about the advert",
                            recipient_id=resipient
                            )

                    S9_list = []

                    str1 = "\n"

                    for row in myresult:


                        intiu = "*Advert Code* :" + row[0] + "\n" + "*Location* :" + row[1] + "\n" + row[2] +  "\n" + row[3] + "\n" + "\n"

                        S9_list.append(intiu)

                        real9 = str1.join(S9_list)

                    mycursor = mysql.connection.cursor()

                    mycursor.execute("SELECT img FROM headimg")

                    imgg = mycursor.fetchall()

                    for idc in imgg:
                        global idcf108

                        idcf108 = idc[0]
                    sq = messenger.send_message(
                            message=real9,
                            recipient_id=resipient
                            )
                    return(sq)

                except UnboundLocalError:

                    messenger.send_message(
                            message="*Oops* This advert code is still empty\nsend *SR* to return to main menu and try another one",
                            recipient_id=resipient
                            )

            elif trimmed.upper() == "S10":

                return (messenger.send_message(
                        message="_______________________\n*-ZIMBABWE-*\n*REQUEST FOR PROPERTY VALUATION*\n_______________________\nProperty Valuation is an exercise carried out by certified professionals with financial expertise in almost every movable and immovable asset. Their valuation reports are a legal document recognised by the laws of Zimbabwe and the international laws at large.\n*Valuation is carried out for a variety of purposes. A few popular are as follows.*\n \n*VA1*: : Valuation for Accounting. Notes & Tips\n*VA2*:  Valuation for Real Estate Pricing. Notes & Tips \n*VA3*: Valuation for Asset Purchase. Notes & Tips\n*VA4*: Valuation for Estate Distribution. Notes & Tips\n*VA5*:Valuation for Insurance Purpose. Notes & Tips\n*VA6*:Valuation for Divorce cases. Notes & Tips\n*VA7*:Valuation for Zimra Taxes. Notes & Tips\n*BOOK A VALUATION WITH THE EXPERT*\n \n_______________________\nIf you wish to book for a property valuation, kindly send VAB or follow https://wa.me/263774767325?text=VAB  \n_______________________\nTo subscribe to regular morning news on property investments and tips, send SUBS1 or follow\nhttps://wa.me/263774767325?text=SUBS1",
                        recipient_id=resipient)

                )
                
            elif trimmed.upper() == "VA1":

                return (messenger.send_message(
                        message="_______________________\n*-ZIMBABWE-*\n*A1 VALUATION FOR ACCOUNTING*\n_______________________\nIn many other countries and Zimbabwe, in particular, the exercise is important especially during or after going through a hyper inflation period out by certified professionals with financial expertise in almost every movable and immovable asset. Their valuation reports are a legal document recognised by the laws of Zimbabwe and the international laws at large.\n*More to come…… *\n*BOOK A VALUATION WITH THE EXPERT*\n \n_______________________\nIf you wish to book for a property valuation, kindly send VAB or follow https://wa.me/263774767325?text=VAB  \n_______________________\nTo subscribe to regular morning news on property investments and tips, send SUBS1 or follow\nhttps://wa.me/263774767325?text=SUBS1",
                        recipient_id=resipient)

                    )

            elif trimmed.upper() == "VAB":

                return (messenger.send_message(
                        message="_______________________\n*-ZIMBABWE-*\n*A1 VALUATION FOR ACCOUNTING*\n_______________________\nIn many other countries and Zimbabwe, in particular, the exercise is important especially during or after going through a hyper inflation period out by certified professionals with financial expertise in almost every movable and immovable asset. Their valuation reports are a legal document recognised by the laws of Zimbabwe and the international laws at large.\n*More to come…… *\n*BOOK A VALUATION WITH THE EXPERT*\n \n_______________________\nIf you wish to book for a property valuation, kindly send VAB or follow https://wa.me/263774767325?text=VAB  \n_______________________\nTo subscribe to regular morning news on property investments and tips, send SUBS1 or follow\nhttps://wa.me/263774767325?text=SUBS1",
                        recipient_id=resipient)

                    )
                
            elif trimmed.upper() == "S11":

                try:
                    mycursor = mysql.connection.cursor()
                    mycursor.execute("SELECT code,location,price,date FROM advert WHERE adcode='%s'" %trimmed.upper())
                    myresult = mycursor.fetchall()

                    sq=messenger.send_message(
                            message="Wait your information is loading\nEnter Advert code to view more details about the advert",
                            recipient_id=resipient
                            )

                    S11_list = []

                    str1 = "\n"

                    for row in myresult:


                        intiu = "*Advert Code* :" + row[0] + "\n" + "*Location* :" + row[1] + "\n" + row[2] +  "\n" + row[3] + "\n" + "\n"

                        S11_list.append(intiu)

                        real11 = str1.join(S11_list)

                    mycursor = mysql.connection.cursor()

                    mycursor.execute("SELECT img FROM headimg")

                    imgg = mycursor.fetchall()

                    for idc in imgg:
                        global idcf109

                        idcf109 = idc[0]
                    sq = messenger.send_message(
                            message=real11,
                            recipient_id=resipient
                            )
                       
                    return (sq)

                except UnboundLocalError:

                    return(messenger.send_message(
                            message="*Oops* This advert code is still empty\nsend *SR* to return to main menu and try another one",
                            recipient_id=resipient
                            ))
                    
            elif trimmed.upper() == "S12":

                try:
                    mycursor = mysql.connection.cursor()
                    mycursor.execute("SELECT code,location,price,date FROM advert WHERE adcode='%s'" %trimmed.upper())
                    myresult = mycursor.fetchall()

                    sq=messenger.send_message(
                            message="Wait your information is loading\nEnter Advert code to view more details about the advert",
                            recipient_id=resipient
                            )

                    S12_list = []

                    str1 = "\n"

                    for row in myresult:


                        intiu = "*Advert Code* :" + row[0] + "\n" + "*Location* :" + row[1] + "\n" + row[2] +  "\n" + row[3] + "\n" + "\n"

                        S12_list.append(intiu)

                        real12 = str1.join(S12_list)

                    mycursor = mysql.connection.cursor()

                    mycursor.execute("SELECT img FROM headimg")

                    imgg = mycursor.fetchall()

                    for idc in imgg:
                        global idcf1011

                        idcf1011 = idc[0]
                    sq = messenger.send_message(
                            message=real12,
                            recipient_id=resipient)
                        #sq.media(idcf1011)
                    return (sq)
                
                except UnboundLocalError:
                    return(messenger.send_message(
                            message="*Oops* This advert code is still empty\nsend *SR* to return to main menu and try another one",
                            recipient_id=resipient
                            ))
                    
            elif trimmed.upper() == "UPL1":

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT img FROM headimg")

                imgg = mycursor.fetchall()

                for idc in imgg:
                    global idcf1012

                    idcf1012 = idc[0]
                sq = messenger.send_message(
                        message="_______________________\n*-UPLOADING- PROPERTY ADVERT.*\n_______________________\n*550 : Uploading Houses to RENT\n*560 : Uploading Commercial/Shops to RENT\n*570 : Uploading Farm to RENT\n*580 : Uploading Industrial to RENT\n*590 : Uploading Short Stay Accommodation\n_______________________\n*650 : Uploading Houses for SALE\n*660 : Uploading Commercial/Shops for SALE\n*670 : Uploading Farm for SALE\n*680 : Uploading Industrial for SALE\n*690 : Uploading Holiday Accommodation for SALE\n*540 : Uploading stand for SALE",
                        recipient_id=resipient
                        )
                    
                return (sq)
            
            elif "PR" in trimmed.upper():

                mycursor = mysql.connection.cursor()
                mycursor.execute("SELECT reg_time FROM subscribers WHERE number='%s' " % resipient)
                mytime = mycursor.fetchall()
                cur_date = datetime.datetime.now()

                for the_time in mytime:

                    format = "%Y-%m-%d %H:%M:%S.%f"
                    here = datetime.datetime.strptime(the_time[0], format)

                    if cur_date >= here:

                        mycursor = mysql.connection.cursor()

                        mycursor.execute("UPDATE subscribers SET status='unpaid' WHERE number='%s'" %resipient)

                        mysql.connection.commit()

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT * FROM subscribers WHERE status = 'paid'")

                result = mycursor.fetchall()

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT * FROM subscribers WHERE status = 'unpaid' AND number = '%s'"%resipient)

                results = mycursor.fetchall()

                for row in result:

                    if resipient in row:

                        messages.append(trimmed)
                        with io.open("messages.csv", "a", encoding="utf-8") as f1:

                            f1.write(str(messages))

                        mycursor = mysql.connection.cursor()

                        mycursor.execute("SELECT code, price, details, extras, location, date, whatsapp, img FROM advert WHERE code='%s' " % trimmed.upper())

                        myresult = mycursor.fetchall()

                        sr=messenger.send_message(
                                message="Advert loading...",
                                recipient_id=resipient
                                )


                        for row in myresult:



                            sr = messenger.send_message(
                                    message="*Advert Code* : "+row[0] + "\n" + row[1] + "\n" + "*Location* : " + row[4] +  "\n" + "*Details* : "+row[2] + "\n" + "*Extras* : "+row[3] + "\n" + row[5] + "\n" + "*Agent link* : "+row[6]+"?text=I%20am%20interested%20in%20your%20advert%20with%20code:%20"+row[0] + "\n\n\n" + "Enter *SR* to return to *main menu*",
                                    recipient_id=resipient
                                    )
                                #sr.media(row[7])

                        return (sr)

                for i in results:

                    if "unpaid" in i:

                        mycursor = mysql.connection.cursor()

                        mycursor.execute("SELECT img FROM headimg")

                        imgg = mycursor.fetchall()

                        for idc5678 in imgg:

                            global idcf10122

                            idcf10122 = idc5678[0]

                            sq = messenger.send_message(
                                    message="Ooops … . It looks like you forgot something! To view this section , please update your subscription . It could have expired.\n_______________________\n*In order to view detailed info and be able to communicate with the advertisers directly.*\n_______________________\n*Use the following format to subscribe now:*\n*2000*your Ecocash number - Daily Sub $40ZWL\n*2100*your Ecocash number – Weekly Sub $270ZWL\n*2200*your Ecocash number Monthly Sub $972ZWL\nExample *2100*772345684\n_______________________\n*If you are seeing this message whilst you are fully subscribed, kindly report to*\nhttps://wa.me/263734277826?text=Hi,%20%20I%20am%20having%20problems%20viewing%20adverts%20the%20section,%20can%20you%20check%20for%20me\nPlease accept our sincere apologies",
                                    recipient_id=resipient
                                    )

                return (sq)
            
            #Agent registration Process
                ###########################
                ###########################
                ###########################
                ###########################

            elif trimmed.upper() == "*550*1":

                return (messenger.send_message(
                        message="_______________________\n*ADVERTISER*\n*REGISTRATION PROCESS*\n_______________________\nTo advertise Y ou are required to register as an advertiser  To register, please enter the following code and your informatio\n*REG Full Name\n*Example* *REG John Hoko",
                        recipient_id=resipient
                        )

                    )

            elif "*REG" in trimmed.upper():

                ag = trimmed.upper().replace("*REG", "")

                agcd = random.randint(1,2999)

                agcod = "AG" + str(agcd)

                mycursor = mysql.connection.cursor()

                sq = "INSERT INTO agents (name,agentcode,number) VALUES (%s,%s,%s)"
                val0 = (ag, agcod, resipient)
                mycursor.execute(sq, val0)

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*ADVERTISER*\n*REGISTRATION PROCESS*\n_______________________\nHere is your agentcode %s. *Please keep safe*\nThank you %s,  Now enter *120 together with your National ID\n*Example* *120 63-21223-D-63"%(agcod,ag),
                        recipient_id=resipient
                        ))

            elif "*120" in trimmed.upper():

                idn = trimmed.upper().replace("*120", "")

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE agents SET idnumber='%s' WHERE number = '%s'" %(idn,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*ADVERTISER*\n*REGISTRATION PROCESS*\n_______________________\nWonderful! ID recorded successfully, Now enter *121 together with your residential address\n*Example* *121  14 Mopani Avenue Glen Norah, Harare",
                        recipient_id=resipient
                        )
                    )

            elif "*121" in trimmed.upper():

                addre = trimmed.upper().replace("*121", "")

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE agents SET address='%s' WHERE number = '%s'" %(addre,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*ADVERTISER*\n*REGISTRATION PROCESS*\n_______________________\nWonderful! address recorded successfully, Now enter tag *IMG to your ID image\n*Example* take a photo of your ID from this chat and add the text *IMG then press send.",
                        recipient_id=resipient
                        )

                    )

            elif "*IMG" in trimmed.upper():

                image_urli = request.values['MediaUrl0']

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE agents SET image='%s' WHERE number='%s'" %(image_urli,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*ADVERTISER*\n*REGISTRATION PROCESS*\n_______________________\nWonderful! ID image recorded successfully\nNow enter tag *IMES to your image\nTake a current picture of yourself and attach *IMES to image",
                        recipient_id=resipient)

                    )

            elif "*IMES" in trimmed.upper():

                image_urlii = request.values['MediaUrl0']

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE agents SET smage='%s' WHERE number='%s'" %(image_urlii,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*End of REGISTRATION PROCESS*\n_______________________\nYour registration is complete enter UPL1 to start uploading",
                        recipient_id=resipient
                        )
                    )

            ###########################
            ###########################
            ###########################
            ###########################
            #end of registration process
            
            elif trimmed == "SaGeNtS":
                mycursor = mysql.connection.cursor()
                mycursor.execute("SELECT name, agentcode, number, idnumber, address, image FROM agents")
                myresulto = mycursor.fetchall()
                for rowo in myresulto:
                    sre = messenger.send_message(
                            message="*Advertiser Name* : "+rowo[0] + "\n" "*Advertiser Code* : "+ rowo[1] + "\n" + "*Advertiser Number* : "+rowo[2] + "\n" + "*ID number* : "+rowo[3] + "\n" + "*Advertiser Address* : "+rowo[4],
                            recipient_id=resipient
                            )      
                return (sre)
            
            #Uploading houses for rent section
                ##########################
                ##########################
                ##########################

            elif trimmed == "*550":

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT number FROM agents")

                agn = mycursor.fetchall()

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT number FROM agents")

                ang = mycursor.fetchall()

                for bn in agn:

                    if resipient in bn:

                        n = random.randint(1,99999)
                        cur_date = datetime.datetime.now()
                        cod = "RP" + str(n)
                        num = resipient
                        link = "https://wa.me/" + str(num)
                        adcod = "S1"
                        newdate = "*Date posted* : " + cur_date.strftime("%d-%b-%Y (%H:%M:%S)")

                        sql = "INSERT INTO advert (number_id, date, whatsapp, code, adcode) VALUES (%s, %s, %s, %s, %s)"
                        val = (resipient, newdate, link, cod, adcod)
                        mycursor = mysql.connection.cursor()
                        mycursor.execute(sql, val)

                        mysql.connection.commit()

                        mycursor = mysql.connection.cursor()

                        mycursor.execute("SELECT id FROM advert WHERE code = '%s'"%cod)

                        re = mycursor.fetchall()

                        for c in re:

                            idrow = str(c[0])

                        resp=messenger.send_message(
                                message="_______________________\n*UPLOADING*\n*HOUSE TO RENT ADVERT*\n______________________\n\nIn case you will need to correct an error\n\nChoose appropriate code for your amendments\n\n155*%s*Location of property\n\n156*%s*Details of property\n\n157*%s*Rent for property\n\n158*%s*Extra facilities/amenities\n\n159*%s* upload best picture"%(idrow,idrow,idrow,idrow,idrow),
                                recipient_id=resipient
                                )

                        resp=messenger.send_message(
                                message="_______________________\n*UPLOADING*\n*HOUSE TO RENT ADVERT*\n______________________\n\nThank you, Your advert code %s\n\nNow add location\n155*%s*Location of Property\n156*%s*Details of property\n157*%s*Rent for property\n158*%s*Extra facilities/amenities\n159*%s* upload best picture" %(cod,idrow,idrow,idrow,idrow,idrow),
                                recipient_id=resipient
                                )

                        return (resp)

                res=messenger.send_message(
                        message="Inorder to upload you need to register as an advertiser first\nEnter *550*1 to start registration process",
                        recipient_id=resipient
                        )
                return (res)
            
            elif "155*" in trimmed:
                initial = 2
                the_id = trimmed.split('*')[initial-1]
                trimmed_turn10 = trimmed.split('*')[initial]
                mycursor = mysql.connection.cursor()
                mycursor.execute("UPDATE advert SET location='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn10,the_id,resipient))
                mysql.connection.commit()
                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*HOUSE TO RENT ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit details\n*Example* 156*%s*A Duplex Flat \nFirst Floor - 4 Bedrooms, Main en-suite, two bath-toilet with showers, living room. \nGround Floor - Modern fitted kitchen, lounge, dinning, and double lock-up garage"%the_id,
                        recipient_id=resipient
                        )
                    )

            elif "156*" in trimmed:

                initial = 2
                the_id = trimmed.split('*')[initial-1]
                trimmed_turn1 = trimmed.split('*')[initial]
                mycursor = mysql.connection.cursor()
                mycursor.execute("UPDATE advert SET details='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn1,the_id,resipient))
                mysql.connection.commit()
                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*HOUSE TO RENT ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit price\n*Example* 157*%s*$500USD per month"%the_id,
                        recipient_id=resipient
                        )
                    )


            elif "157*" in trimmed:

                initial = 2
                the_id = trimmed.split('*')[initial-1]
                trimmed_turn2 = trimmed.split('*')[initial]
                mycursor = mysql.connection.cursor()
                mycursor.execute("UPDATE advert SET price='%s' WHERE id='%s' AND number_id='%s'" %("*Price* : " + trimmed_turn2,the_id,resipient))
                mysql.connection.commit()
                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*HOUSE TO RENT ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit extras if any\n*Example* 158*%s*Solar power, Bolehole, swimming pool etc"%the_id,
                        recipient_id=resipient
                        )
                    )

            elif "158*" in trimmed:

                initial = 2
                the_id = trimmed.split('*')[initial-1]
                trimmed_turn3 = trimmed.split('*')[initial]
                mycursor = mysql.connection.cursor()
                mycursor.execute("UPDATE advert SET extras='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn3,the_id,resipient))
                mysql.connection.commit()
                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*HOUSE TO RENT ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nIf you wish to attach an image to you advert\nAttach 159*%s* to image and send\n*Enter SR to return to main menu* "%the_id,
                        recipient_id=resipient
                        )
                    )

            elif "159*" in trimmed:

                initial = 2
                the_id = trimmed.split('*')[initial-1]
                image_url = request.values['MediaUrl0']
                mycursor = mysql.connection.cursor()
                mycursor.execute("UPDATE advert SET img='%s' WHERE id='%s' AND number_id='%s'" %(image_url,the_id,resipient))
                mysql.connection.commit()
                mycursor = mysql.connection.cursor()
                mycursor.execute("SELECT code FROM advert WHERE id='%s' AND number_id='%s'" %(the_id,resipient))
                ge = mycursor.fetchall()
                for idef in ge:
                    thecod = idef[0]
                return (messenger.send_message(
                        message="_______________________\n*END OF UPLOAD*\n*House for rent*\n______________________\n\nThanks for the image!\nYour Advert has been successfully placed\nTo view it enter your advert code %s\n*Enter SR to return to main menu* "%thecod,
                        recipient_id=resipient
                        )
                    )
                ##########################
                ##########################
                ##########################
            #end of house for rent upload section
            
            #Uploading Commercial/Shops for rent section
                ##########################
                ##########################
                ##########################

            elif trimmed.upper() == "*560":

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT number FROM agents")

                agn = mycursor.fetchall()

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT number FROM agents")

                ang = mycursor.fetchall()

                for bn in agn:

                    if resipient in bn:

                        n = random.randint(1,99999)
                        cur_date = datetime.datetime.now()
                        cod = "RP" + str(n)
                        num = resipient
                        link = "https://wa.me/" + str(num)
                        adcod = "S2"
                        newdate = "*Date posted* : " + cur_date.strftime("%d-%b-%Y (%H:%M:%S)")

                        sql = "INSERT INTO advert (number_id, date, whatsapp, code, adcode) VALUES (%s, %s, %s, %s, %s)"
                        val = (resipient, newdate, link, cod, adcod)
                        mycursor = mysql.connection.cursor()
                        mycursor.execute(sql, val)

                        mysql.connection.commit()

                        mycursor = mysql.connection.cursor()

                        mycursor.execute("SELECT id FROM advert WHERE code = '%s'"%cod)

                        re = mycursor.fetchall()

                        for c in re:

                            the_id = str(c[0])

                        es=messenger.send_message(
                                message="_______________________\n*UPLOADING*\n*Commercial/Shops TO RENT ADVERT*\n______________________\n\nIn case you will need to correct an error\n\nChoose appropriate code for your amendments\n\n165*%s*Location of property\n\n166*%s*Details of property\n\n167*%s*Rent for property\n\n168*%s*Extra facilities/amenities\n\n169*%s upload best picture"%(the_id,the_id,the_id,the_id,the_id),
                                recipient_id=resipient
                                )

                        es=messenger.send_message(
                                message="_______________________\n*UPLOADING*\n*Commercial/Shops TO RENT ADVERT*\n______________________\n\nThank you. Information has been successful uploadedd\n\nYour advert code %s\n\nNow add location\n165*%s*Location of Property\n*Example* 165*%s*Harare, Borrowdale" %(cod,the_id,the_id),
                                recipient_id=resipient
                                )

                        return (es)


                return (messenger.send_message(
                        message="Inorder to upload you need to register as an advertiser first\nEnter *550*1 to start registration process",
                        recipient_id=resipient
                        )
                )
                
            elif "165*" in trimmed:

                initial = 2
                the_id = trimmed.split('*')[initial-1]

                trimmed_turn10 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET location='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn10,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*Commercial/Shops TO RENT ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit details\n*Example* 166*%s*To rent is a supermarket and 3 shops "%the_id,
                        recipient_id=resipient
                        )
                    )

            elif "166*" in trimmed:

                initial = 2
                the_id = trimmed.split('*')[initial-1]

                trimmed_turn1 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET details='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn1,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*Commercial/Shops TO RENT ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit price\n*Example* 167*%s*US$2 100 per Month"%the_id,
                        recipient_id=resipient
                        )
                    )


            elif "167*" in trimmed:

                initial = 2
                the_id = trimmed.split('*')[initial-1]

                trimmed_turn2 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET price='%s' WHERE id='%s' AND number_id='%s'" %("*Price* : " + trimmed_turn2,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*Commercial/Shops TO RENT ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit extras if any\n*Example* 168*%s*Delivery space, 6 parking lots….."%the_id,
                        recipient_id=resipient
                        )
                    )

            elif "168*" in trimmed:

                initial = 2
                the_id = trimmed.split('*')[initial-1]

                trimmed_turn3 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET extras='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn3,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*Commercial/Shops TO RENT ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nIf you wish to attach an image to you advert\nAttach 169*%s to image and send\n*Enter SR to return to main menu* "%the_id,
                        recipient_id=resipient
                        )
                    )

            elif "169*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                image_url = request.values['MediaUrl0']
                mycursor = mysql.connection.cursor()
                mycursor.execute("UPDATE advert SET img='%s' WHERE id='%s' AND number_id='%s'" %(image_url,the_id,resipient))
                mysql.connection.commit()

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT code FROM advert WHERE id='%s' AND number_id='%s'" %(the_id,resipient))

                ge = mycursor.fetchall()

                for idef in ge:

                    thecod = idef[0]

                return (messenger.send_message(
                        message="_______________________\n*END OF UPLOAD*\n*Commercial / Shops for rent*\n______________________\n\nThanks for the image!\nYour Advert has been successfully placed\nTo view it enter your advert code %s\n*Enter SR to return to main menu* "%thecod,
                        recipient_id=resipient
                        )
                    )

                ##########################
                ##########################
                ##########################
            #end of commercial / shops for rent upload section
            
            #Uploading Industrial for rent section
                ##########################
                ##########################
                ##########################

            elif trimmed.upper() == "*580":

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT number FROM agents")

                agn = mycursor.fetchall()

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT number FROM agents")

                ang = mycursor.fetchall()

                for bn in agn:

                    if resipient in bn:

                        n = random.randint(1,99999)
                        cur_date = datetime.datetime.now()
                        cod = "RP" + str(n)
                        num = resipient
                        link = "https://wa.me/" + str(num)
                        adcod = "S4"
                        newdate = "*Date posted* : " + cur_date.strftime("%d-%b-%Y (%H:%M:%S)")

                        sql = "INSERT INTO advert (number_id, date, whatsapp, code, adcode) VALUES (%s, %s, %s, %s, %s)"
                        val = (resipient, newdate, link, cod, adcod)
                        mycursor = mysql.connection.cursor()
                        mycursor.execute(sql, val)

                        mysql.connection.commit()

                        mycursor = mysql.connection.cursor()

                        mycursor.execute("SELECT id FROM advert WHERE code = '%s'"%cod)

                        re = mycursor.fetchall()

                        for c in re:

                            the_id = str(c[0])

                        esp=messenger.send_message(
                                message="_______________________\n*UPLOADING*\n*Industrial TO RENT ADVERT*\n______________________\n\nIn case you will need to correct an error\n\nChoose appropriate code for your amendments\n\n175*%s*Location of property\n\n176*%s*Details of property\n\n177*%s*Rent for property\n\n178*%s*Extra facilities/amenities\n\n179*%s upload best picture"%(the_id,the_id,the_id,the_id,the_id),
                                recipient_id=resipient
                                )

                        esp=messenger.send_message(
                                message="_______________________\n*UPLOADING*\n*Industrial TO RENT ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\n\nYour advert code %s\n\nNow add location\n175*%s*Location of Property\n*Example* 175*%s*Harare Willowvale" %(cod,the_id,the_id),
                                recipient_id=resipient
                                )

                        return (esp)

                return (messenger.send_message(
                        message="Inorder to upload you need to register as an advertiser first\nEnter *550*1 to start registration process",
                        recipient_id=resipient
                        )
                )
                
            elif "175*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn10 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET location='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn10,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*Industrial TO RENT ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit details\n*Example* 176*%s*Two warehouses and a block of six offices"%the_id,
                        recipient_id=resipient)


                    )

            elif "176*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn1 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET details='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn1,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*Industrial TO RENT ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit price\n*Example* 177*%s*US$2000 per month"%the_id,
                        recipient_id=resipient)
                )


            elif "177*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn2 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET price='%s' WHERE id='%s' AND number_id='%s'" %("*Price* : " + trimmed_turn2,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*Industrial TO RENT ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit extras if any\n*Example* 178*%s*Workshop, Zesa transformer….."%the_id,
                        recipient_id=resipient)
                    )

            elif "178*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn3 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET extras='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn3,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*Industrial TO RENT ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nIf you wish to attach an image to you advert\nAttach 179*%s*to image and send\n*Enter SR to return to main menu* "%the_id,
                        recipient_id=resipient)

                )

            elif "179*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                image_url = request.values['MediaUrl0']

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET img='%s' WHERE id='%s' AND number_id='%s'" %(image_url,the_id,resipient))

                mysql.connection.commit()

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT code FROM advert WHERE id='%s' AND number_id='%s'" %(the_id,resipient))

                ge = mycursor.fetchall()

                for idef in ge:

                    thecod = idef[0]

                return (messenger.send_message(
                        message="_______________________\n*END OF UPLOAD*\n*Industrial for rent*\n______________________\n\nThanks for the image!\nYour Advert has been successfully placed\nTo view it enter your advert code %s\n*Enter SR to return to main menu* "%thecod,
                        recipient_id=resipient)
                    )

                ##########################
                ##########################
                ##########################
            #end of Industrial for rent upload section
            
            #Uploading Farm for rent section
                ##########################
                ##########################
                ##########################

            elif trimmed.upper() == "*570":

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT number FROM agents")

                agn = mycursor.fetchall()

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT number FROM agents")

                ang = mycursor.fetchall()

                for bn in agn:

                    if resipient in bn:

                        n = random.randint(1,99999)
                        cur_date = datetime.datetime.now()
                        cod = "RP" + str(n)
                        num = resipient
                        link = "https://wa.me/" + str(num)
                        adcod = "S3"
                        newdate = "*Date posted* : " + cur_date.strftime("%d-%b-%Y (%H:%M:%S)")

                        sql = "INSERT INTO advert (number_id, date, whatsapp, code, adcode) VALUES (%s, %s, %s, %s, %s)"
                        val = (resipient, newdate, link, cod, adcod)
                        mycursor = mysql.connection.cursor()
                        mycursor.execute(sql, val)

                        mysql.connection.commit()

                        mycursor = mysql.connection.cursor()

                        mycursor.execute("SELECT id FROM advert WHERE code = '%s'"%cod)

                        re = mycursor.fetchall()

                        for c in re:

                            the_id = str(c[0])

                        esp=messenger.send_message(
                                message="_______________________\n*UPLOADING*\n*Farm TO RENT ADVERT*\n______________________\n\nIn case you will need to correct an error\nChoose appropriate code for your amendments\n\n185*%s*Location of property\n\n186*%s*Details of property\n\n187*%s*Rent for property\n\n188*%s*Extra facilities/amenities\n\n189*%s upload best picture"%(the_id,the_id,the_id,the_id,the_id),
                                recipient_id=resipient)

                        esp=messenger.send_message(
                                message="_______________________\n*UPLOADING*\n*Farml TO RENT ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\n\nYour advert code %s\n\nNow add location\n185*%s*Location of Property\n*Example* 185*%s*Bindura, Ballard Farm" %(cod,the_id,the_id),
                                recipient_id=resipient)

                    return str(esp)

                return (messenger.send_message(
                        message="Inorder to upload you need to register as an advertiser first\nEnter *550*1 to start registration process",
                        recipient_id=resipient
                        )
                    )
            
            elif "185*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn10 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET location='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn10,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*Farm TO RENT ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit details\n*Example* 186*%s*Seventy hectares of arable land and 45ha of grazing."%the_id,
                        recipient_id=resipient)
                    )

            elif "186*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn1 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET details='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn1,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*Farm TO RENT ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit price\n*Example* 187*%s*US$900 per Year"%the_id,
                        recipient_id=resipient)
                    )


            elif "187*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn2 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET price='%s' WHERE id='%s' AND number_id='%s'" %("*Price* : " + trimmed_turn2,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*Farm TO RENT ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit extras if any\n*Example* 188*%s*Centre Pivot installed ….."%the_id,
                        recipient_id=resipient)
                    )

            elif "188*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn3 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET extras='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn3,the_id,resipient))

                mysql.connection.commit()

                return(messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*Farm TO RENT ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nIf you wish to attach an image to you advert\nAttach 189*%s to image and send\n*Enter SR to return to main menu* "%the_id,
                        recipient_id=resipient)

                    )

            elif "189*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                image_url = request.values['MediaUrl0']

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET img='%s' WHERE id='%s' AND number_id='%s'" %(image_url,the_id,resipient))

                mysql.connection.commit()

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT code FROM advert WHERE id='%s' AND number_id='%s'" %(the_id,resipient))

                ge = mycursor.fetchall()

                for idef in ge:

                    thecod = idef[0]

                return (messenger.send_message(
                        message="_______________________\n*END OF UPLOAD*\n*Farm for rent*\n______________________\n\nThanks for the image!\nYour Advert has been successfully placed\nTo view it enter your advert code %s\n*Enter SR to return to main menu* "%thecod,
                        recipient_id=resipient) )
                ##########################
                ##########################
                ##########################
            #end of Farm for rent upload section
            
            #Uploading HOUSES FOR SALE section
                ##########################
                ##########################
                ##########################

            elif trimmed.upper() == "*650":

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT number FROM agents")

                agn = mycursor.fetchall()

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT number FROM agents")

                ang = mycursor.fetchall()

                for bn in agn:

                    if resipient in bn:

                        n = random.randint(1,99999)
                        cur_date = datetime.datetime.now()
                        cod = "RP" + str(n)
                        num = resipient
                        link = "https://wa.me/" + str(num)
                        adcod = "S5"
                        newdate = "*Date posted* : " + cur_date.strftime("%d-%b-%Y (%H:%M:%S)")

                        sql = "INSERT INTO advert (number_id, date, whatsapp, code, adcode) VALUES (%s, %s, %s, %s, %s)"
                        val = (resipient, newdate, link, cod, adcod)
                        mycursor = mysql.connection.cursor()
                        mycursor.execute(sql, val)

                        mysql.connection.commit()

                        mycursor = mysql.connection.cursor()

                        mycursor.execute("SELECT id FROM advert WHERE code = '%s'"%cod)

                        re = mycursor.fetchall()

                        for c in re:

                            the_id = str(c[0])

                        resp=messenger.send_message(
                                message="_______________________\n*UPLOADING*\n*HOUSES FOR SALE ADVERT*\n______________________\n\nIn case you will need to correct an error\nChoose appropriate code for your amendments\n\n195*%s*Location of property\n\n196*%s*Details of property\n\n197*%s*Rent for property\n\n198*%s*Extra facilities/amenities\n\n199*%s upload best picture"%(the_id,the_id,the_id,the_id,the_id),
                                recipient_id=resipient)

                        resp=messenger.send_message(
                                message="_______________________\n*UPLOADING*\n*HOUSES FOR SALE ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\n\nYour advert code %s\n\nNow add location\n195*%s*Location of Property\n*Example* 195*%s*Harare Greendale" %(cod,the_id,the_id),
                                recipient_id=resipient)

                        return (resp)

                return (messenger.send_message(
                        message="Inorder to upload you need to register as an advertiser first\nEnter *550*1 to start registration process",
                        recipient_id=resipient
                        )
                    )
                
            elif "195*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn10 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET location='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn10,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*HOUSES FOR SALE ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit details\n*Example* 196*%s*Situated 500mtrs from primary and secondary schools, 5 min walk to a shopping centre,Five beds, kitchen, dining, main en-suite, cottage."%the_id,
                        recipient_id=resipient)
                    )

            elif "196*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn1 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET details='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn1,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*HOUSES FOR SALE ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit price\n*Example* 197*%s*US$200 000 Neg"%the_id,
                        recipient_id=resipient)
                    )


            elif "197*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn2 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET price='%s' WHERE id='%s' AND number_id='%s'" %("*Price* : " + trimmed_turn2,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*HOUSES FOR SALE ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit extras if any\n*Example* 198*%s*Borehole, well, 10000ltr  water tank, tennis court, swimming pool….."%the_id,
                        recipient_id=resipient)
                    )

            elif "198*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn3 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET extras='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn3,the_id,resipient))

                mysql.connection.commit()

                return(messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*HOUSES FOR SALE ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nIf you wish to attach an image to you advert\nAttach 199*%s to image and send\n*Enter SR to return to main menu* "%the_id,
                        recipient_id=resipient)
                    )

            elif "199*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                image_url = request.values['MediaUrl0']

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET img='%s' WHERE id='%s' AND number_id='%s'" %(image_url,the_id,resipient))

                mysql.connection.commit()

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT code FROM advert WHERE id='%s' AND number_id='%s'" %(the_id,resipient))

                ge = mycursor.fetchall()

                for idef in ge:

                    thecod = idef[0]

                return (messenger.send_message(
                        message="_______________________\n*END OF UPLOAD*\n*Houses for sale*\n______________________\n\nThanks for the image!\nYour Advert has been successfully placed\nTo view it enter your advert code %s\n*Enter SR to return to main menu* "%thecod,
                        recipient_id=resipient)
                    )

                ##########################
                ##########################
                ##########################
            #end of Houses for sale upload section
            
            #Uploading COMMERCIAL/SHOPS FOR SALE section
                ##########################
                ##########################
                ##########################

            elif trimmed.upper() == "*660":

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT number FROM agents")

                agn = mycursor.fetchall()

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT number FROM agents")

                ang = mycursor.fetchall()

                for bn in agn:

                    if resipient in bn:

                        n = random.randint(1,99999)
                        cur_date = datetime.datetime.now()
                        cod = "RP" + str(n)
                        num = resipient
                        link = "https://wa.me/" + str(num)
                        adcod = "S6"
                        newdate = "*Date posted* : " + cur_date.strftime("%d-%b-%Y (%H:%M:%S)")

                        sql = "INSERT INTO advert (number_id, date, whatsapp, code, adcode) VALUES (%s, %s, %s, %s, %s)"
                        val = (resipient, newdate, link, cod, adcod)
                        mycursor = mysql.connection.cursor()
                        mycursor.execute(sql, val)

                        mysql.connection.commit()

                        mycursor = mysql.connection.cursor()

                        mycursor.execute("SELECT id FROM advert WHERE code = '%s'"%cod)

                        re = mycursor.fetchall()

                        for c in re:

                            the_id = str(c[0])

                        resp=messenger.send_message(
                                message="_______________________\n*UPLOADING*\n*COMMERCIAL/SHOPS FOR SALE ADVERT*\n______________________\n\nIn case you will need to correct an error\nChoose appropriate code for your amendments\n\n145*%s*Location of property\n\n146*%s*Details of property\n\n147*%s*Rent for property\n\n148*%s*Extra facilities/amenities\n\n149*%s upload best picture"%(the_id,the_id,the_id,the_id,the_id),
                                recipient_id=resipient)

                        resp=messenger.send_message(
                                message="_______________________\n*UPLOADING*\n*COMMERCIAL/SHOPS FOR SALE ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\n\nYour advert code %s\n\nNow add location\n145*%s*Location of Property\n*Example* 145*%s*Harare City Centre" %(cod,the_id,the_id),
                                recipient_id=resipient)

                        return (resp)

                return (messenger.send_message(
                        message="Inorder to upload you need to register as an advertiser first\nEnter *550*1 to start registration process",
                        recipient_id=resipient
                        )
                    )


            elif "145*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn10 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET location='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn10,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*COMMERCIAL/SHOPS FOR SALE ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit details\n*Example* 146*%s*On sale is a building with thirteen offices, parking for 15 cars in the CBD."%the_id,
                        recipient_id=resipient)
                    )

            elif "146*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn1 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET details='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn1,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*COMMERCIAL/SHOPS FOR SALE ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit price\n*Example* 147*%s*US$600 000 Neg"%the_id,
                        recipient_id=resipient)
                    )


            elif "147*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn2 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET price='%s' WHERE id='%s' AND number_id='%s'" %("*Price* : " + trimmed_turn2,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*COMMERCIAL/SHOPS FOR SALE ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit extras if any\n*Example* 148*%s*Borehole, well, 10000ltr  water"%the_id,
                        recipient_id=resipient)
                    )

            elif "148*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn3 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET extras='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn3,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*COMMERCIAL/SHOPS FOR SALE ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nIf you wish to attach an image to you advert\nAttach 149*%s to image and send\n*Enter SR to return to main menu* "%the_id,
                        recipient_id=resipient)
                    )

            elif "149*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                image_url = request.values['MediaUrl0']

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET img='%s' WHERE id='%s' AND number_id='%s'" %(image_url,the_id,resipient))

                mysql.connection.commit()

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT code FROM advert WHERE id='%s' AND number_id='%s'" %(the_id,resipient))

                ge = mycursor.fetchall()

                for idef in ge:

                    thecod = idef[0]

                return (messenger.send_message(
                        message="_______________________\n*END OF UPLOAD*\n*COMMERCIAL/SHOPS*\n______________________\n\nThanks for the image!\nYour Advert has been successfully placed\nTo view it enter your advert code %s\n*Enter SR to return to main menu* "%thecod,
                        recipient_id=resipient)
                    )

                ##########################
                ##########################
                ##########################
            #end of COMMERCIAL/SHOPS upload section
            
            #Uploading INDUSTRIALS FOR SALE section
                ##########################
                ##########################
                ##########################

            elif trimmed.upper() == "*680":

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT number FROM agents")

                agn = mycursor.fetchall()

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT number FROM agents")

                ang = mycursor.fetchall()

                for bn in agn:

                    if resipient in bn:

                        n = random.randint(1,99999)
                        cur_date = datetime.datetime.now()
                        cod = "RP" + str(n)
                        num = resipient
                        link = "https://wa.me/" + str(num)
                        adcod = "S7"
                        newdate = "*Date posted* : " + cur_date.strftime("%d-%b-%Y (%H:%M:%S)")
                        sql = "INSERT INTO advert (number_id, date, whatsapp, code, adcode) VALUES (%s, %s, %s, %s, %s)"
                        val = (resipient, newdate, link, cod, adcod)
                        mycursor = mysql.connection.cursor()
                        mycursor.execute(sql, val)
                        mysql.connection.commit()
                        mycursor = mysql.connection.cursor()
                        mycursor.execute("SELECT id FROM advert WHERE code = '%s'"%cod)

                        re = mycursor.fetchall()

                        for c in re:

                            the_id = str(c[0])

                        resp=messenger.send_message(
                                message="_______________________\n*UPLOADING*\n*INDUSTRIALS FOR SALE ADVERT*\n______________________\n\nIn case you will need to correct an error\nChoose appropriate code for your amendments\n\n135*%s*Location of property\n\n136*%s*Details of property\n\n137*%s*Rent for property\n\n138*%s*Extra facilities/amenities\n\n139*%s upload best picture"%(the_id,the_id,the_id,the_id,the_id),
                                recipient_id=resipient)

                        resp=messenger.send_message(
                                message="_______________________\n*UPLOADING*\n*INDUSTRIALS FOR SALE ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\n\nYour advert code %s\n\nNow add location\n135*%s*Location of Property\n*Example* 135*%s*Harare Graniteside" %(cod,the_id,the_id),
                                recipient_id=resipient)

                        return (resp)

                return (messenger.send_message(
                        message="Inorder to upload you need to register as an advertiser first\nEnter *550*1 to start registration process",
                        recipient_id=resipient
                        )
                )


            elif "135*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn10 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET location='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn10,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*INDUSTRIALS FOR SALE ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit details\n*Example* 136*%s*A block of offices, 3 warehouses, shops……."%the_id,
                        recipient_id=resipient)
                    )

            elif "136*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn1 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET details='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn1,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*INDUSTRIALS FOR SALE ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit price\n*Example* 137*%s*US$1 600 000 Neg  "%the_id,
                        recipient_id=resipient)
                )


            elif "137*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn2 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET price='%s' WHERE id='%s' AND number_id='%s'" %("*Price* : " + trimmed_turn2,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*INDUSTRIALS FOR SALE ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit extras if any\n*Example* 138*%s*Borehole, well, 10000ltr  water "%the_id,
                        recipient_id=resipient)
                    )

            elif "138*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn3 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET extras='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn3,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*INDUSTRIALS FOR SALE ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nIf you wish to attach an image to you advert\nAttach 139*%s to image and send\n*Enter SR to return to main menu* "%the_id,
                        recipient_id=resipient)
                    )

            elif "139*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                image_url = request.values['MediaUrl0']

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET img='%s' WHERE id='%s' AND number_id='%s'" %(image_url,the_id,resipient))

                mysql.connection.commit()

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT code FROM advert WHERE id='%s' AND number_id='%s'" %(the_id,resipient))

                ge = mycursor.fetchall()

                for idef in ge:

                    thecod = idef[0]

                return (messenger.send_message(
                        message="_______________________\n*END OF UPLOAD*\n*INDUSTRIALS FOR SALE*\n______________________\n\nThanks for the image!\nYour Advert has been successfully placed\nTo view it enter your advert code %s\n*Enter SR to return to main menu* "%thecod,
                        recipient_id=resipient)
                    )

                ##########################
                ##########################
                ##########################
            #end of INDUSTRIALS FOR SALE upload section
            
            #Uploading FARM FOR SALE section
                ##########################
                ##########################
                ##########################

            elif trimmed.upper() == "*670":

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT number FROM agents")

                agn = mycursor.fetchall()

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT number FROM agents")

                ang = mycursor.fetchall()

                for bn in agn:

                    if resipient in bn:

                        n = random.randint(1,99999)
                        cur_date = datetime.datetime.now()
                        cod = "RP" + str(n)
                        num = resipient
                        link = "https://wa.me/" + str(num)
                        adcod = "S8"
                        newdate = "*Date posted* : " + cur_date.strftime("%d-%b-%Y (%H:%M:%S)")

                        sql = "INSERT INTO advert (number_id, date, whatsapp, code, adcode) VALUES (%s, %s, %s, %s, %s)"
                        val = (resipient, newdate, link, cod, adcod)

                        mycursor = mysql.connection.cursor()

                        mycursor.execute(sql, val)

                        mysql.connection.commit()

                        mycursor = mysql.connection.cursor()

                        mycursor.execute("SELECT id FROM advert WHERE code = '%s'"%cod)

                        re = mycursor.fetchall()

                        for c in re:

                            the_id = str(c[0])

                        resp=messenger.send_message(
                                message="_______________________\n*UPLOADING*\n*FARM FOR SALE ADVERT*\n______________________\n\nIn case you will need to correct an error\nChoose appropriate code for your amendments\n\n125*%s*Location of property\n\n126*%s*Details of property\n\n127*%s*Rent for property\n\n128*%s*Extra facilities/amenities\n\n129*%s upload best picture"%(the_id,the_id,the_id,the_id,the_id),
                                recipient_id=resipient)

                        resp=messenger.send_message(
                                message="_______________________\n*UPLOADING*\n*FARM FOR SALE ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\n\nYour advert code %s\n\nNow add location\n125*%s*Location of Property\n*Example* 125*%s*Chegutu, Muzvezve" %(cod,the_id,the_id),
                                recipient_id=resipient)

                        return (resp)

                return (messenger.send_message(
                        message="Inorder to upload you need to register as an advertiser first\nEnter *550*1 to start registration process",
                        recipient_id=resipient
                        )
                    )


            elif "125*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn10 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET location='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn10,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*FARM FOR SALE ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit details\n*Example* 126*%s*Seventy hectares of arable land and 45ha of grazing."%the_id,
                        recipient_id=resipient)
                   )

            elif "126*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn1 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET details='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn1,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*FARM FOR SALE ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit price\n*Example* 127*%s*US$150 000 Neg"%the_id,
                        recipient_id=resipient)
                )


            elif "127*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn2 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET price='%s' WHERE id='%s' AND number_id='%s'" %("*Price* : " + trimmed_turn2,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*FARM FOR SALE ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit extras if any\n*Example* 128*%s*Perennial dam water, irrigation. "%the_id,
                        recipient_id=resipient)
                        )

            elif "128*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn3 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET extras='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn3,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*FARM FOR SALE ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nIf you wish to attach an image to you advert\nAttach 129*%s to image and send\n*Enter SR to return to main menu* "%the_id,
                        recipient_id=resipient)
                    )

            elif "129*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                image_url = request.values['MediaUrl0']

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET img='%s' WHERE id='%s' AND number_id='%s'" %(image_url,the_id,resipient))

                mysql.connection.commit()

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT code FROM advert WHERE id='%s' AND number_id='%s'" %(the_id,resipient))

                ge = mycursor.fetchall()

                for idef in ge:

                    thecod = idef[0]

                return (messenger.send_message(
                        message="_______________________\n*END OF UPLOAD*\n*FARM FOR SALE*\n______________________\n\nThanks for the image!\nYour Advert has been successfully placed\nTo view it enter your advert code %s\n*Enter SR to return to main menu* "%thecod,
                        recipient_id=resipient)
                    )

                ##########################
                ##########################
                ##########################
            #end of FARM FOR SALE upload section
            
            #Uploading STANDS FOR SALE section
                ##########################
                ##########################
                ##########################

            elif trimmed.upper() == "*540":

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT number FROM agents")

                agn = mycursor.fetchall()

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT number FROM agents")

                ang = mycursor.fetchall()

                for bn in agn:

                    if resipient in bn:

                        n = random.randint(1,99999)
                        cur_date = datetime.datetime.now()
                        cod = "RP" + str(n)
                        num = resipient
                        link = "https://wa.me/" + str(num)
                        adcod = "S9"
                        newdate = "*Date posted* : " + cur_date.strftime("%d-%b-%Y (%H:%M:%S)")

                        sql = "INSERT INTO advert (number_id, date, whatsapp, code, adcode) VALUES (%s, %s, %s, %s, %s)"
                        val = (resipient, newdate, link, cod, adcod)
                        mycursor = mysql.connection.cursor()
                        mycursor.execute(sql, val)

                        mysql.connection.commit()

                        mycursor = mysql.connection.cursor()

                        mycursor.execute("SELECT id FROM advert WHERE code = '%s'"%cod)

                        re = mycursor.fetchall()

                        for c in re:

                            the_id = str(c[0])

                        resp=messenger.send_message(
                                message="_______________________\n*UPLOADING*\n*STANDS FOR SALE ADVERT*\n______________________\n\nIn case you will need to correct an error\nChoose appropriate code for your amendments\n\n115*%s*Location of property\n\n116*%s*Details of property\n\n117*%s*Rent for property\n\n118*%s*Extra facilities/amenities\n\n119*%s upload best picture"%(the_id,the_id,the_id,the_id,the_id),
                                recipient_id=resipient)

                        resp=messenger.send_message(
                                message="_______________________\n*UPLOADING*\n*STANDS FOR SALE ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\n\nYour advert code %s\n\nNow add location\n115*%s*Location of Property\n*Example* 115*%s*Harare Ashdown Park" %(cod,the_id,the_id),
                                recipient_id=resipient)

                        return (resp)

                return (messenger.send_message(
                        message="Inorder to upload you need to register as an advertiser first\nEnter *550*1 to start registration process",
                        recipient_id=resipient
                        )
                    )



            elif "115*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn10 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET location='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn10,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*STANDS FOR SALE ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit details\n*Example* 116*%s*fully serviced stands from 540sqm to 890sqm."%the_id,
                        recipient_id=resipient)
                    )

            elif "116*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn1 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET details='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn1,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*STANDS FOR SALE ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit price\n*Example* 117*%s*US$50/sqm Neg"%the_id,
                        recipient_id=resipient)
                    )


            elif "117*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn2 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET price='%s' WHERE id='%s' AND number_id='%s'" %("*Price* : " + trimmed_turn2,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*STANDS FOR SALE ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit extras if any\n*Example* 118*%s*High-speed internet, ZESA"%the_id,
                        recipient_id=resipient)
                )

            elif "118*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn3 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET extras='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn3,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*STANDS FOR SALE ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nIf you wish to attach an image to you advert\nAttach 119*%s to image and send\n*Enter SR to return to main menu* "%the_id,
                        recipient_id=resipient)
                )

            elif "119*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                image_url = request.values['MediaUrl0']

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET img='%s' WHERE id='%s' AND number_id='%s'" %(image_url,the_id,resipient))

                mysql.connection.commit()

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT code FROM advert WHERE id='%s' AND number_id='%s'" %(the_id,resipient))

                ge = mycursor.fetchall()

                for idef in ge:

                    thecod = idef[0]

                return (messenger.send_message(
                        message="_______________________\n*END OF UPLOAD*\n*STANDS FOR SALE*\n______________________\n\nThanks for the image!\nYour Advert has been successfully placed\nTo view it enter your advert code %s\n*Enter SR to return to main menu* "%thecod,
                        recipient_id=resipient)
                    )

                ##########################
                ##########################
                ##########################
            #end of STANDS FOR SALE upload section
            
            #Uploading HOLIDAY ACCOMMODATION section
                ##########################
                ##########################
                ##########################

            elif trimmed == "*590":

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT number FROM agents")

                agn = mycursor.fetchall()

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT number FROM agents")

                ang = mycursor.fetchall()

                for bn in agn:

                    if resipient in bn:

                        n = random.randint(1,99999)
                        cur_date = datetime.datetime.now()
                        cod = "RP" + str(n)
                        num = resipient
                        link = "https://wa.me/" + str(num)
                        adcod = "S11"
                        newdate = "*Date posted* : " + cur_date.strftime("%d-%b-%Y (%H:%M:%S)")

                        sql = "INSERT INTO advert (number_id, date, whatsapp, code, adcode) VALUES (%s, %s, %s, %s, %s)"
                        val = (resipient, newdate, link, cod, adcod)
                        mycursor = mysql.connection.cursor()
                        mycursor.execute(sql, val)

                        mysql.connection.commit()

                        mycursor = mysql.connection.cursor()

                        mycursor.execute("SELECT id FROM advert WHERE code = '%s'"%cod)

                        re = mycursor.fetchall()

                        for c in re:

                            the_id = str(c[0])

                        resp=messenger.send_message(
                                message="_______________________\n*UPLOADING*\n*HOLIDAY ACCOMMODATION ADVERT*\n______________________\n\nIn case you will need to correct an error, just enter\n\n\nThen choose appropriate code for your amendments\n\n160*%s*Location of property\n\n161*%s*Details of property\n\n162*%s*Rent for property\n\n163*%s*Extra facilities/amenities\n\n164*%s upload best picture"%(the_id,the_id,the_id,the_id,the_id),
                                recipient_id=resipient)

                        resp=messenger.send_message(
                                message="_______________________\n*UPLOADING*\n*HOLIDAY ACCOMMODATION ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\n\nYour advert code %s\n\nNow add location\n160*%s*Location of Property\n*Example* 160*%s*Victoria Falls/Mazowe/Harare" %(cod,the_id,the_id),
                                recipient_id=resipient)

                        return (resp)

                return (messenger.send_message(
                        message="Inorder to upload you need to register as an advertiser first\nEnter *550*1 to start registration process",
                        recipient_id=resipient
                        )
                    )




            elif "160*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn10 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET location='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn10,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*HOLIDAY ACCOMMODATION ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit details\n*Example* 161*%s*self-catering 4 bedrooms holiday home. - Fully furnished.- Minimum booking- 4days"%the_id,
                        recipient_id=resipient)
                    )

            elif "161*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn1 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET details='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn1,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*HOLIDAY ACCOMMODATION ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit price\n*Example* 162*%s*US$60 per night  "%the_id,
                        recipient_id=resipient)
                    )


            elif "162*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn2 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET price='%s' WHERE id='%s' AND number_id='%s'" %("*Price* : " + trimmed_turn2,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*HOLIDAY ACCOMMODATION ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit extras if any\n*Example* 163*%s*Children Entertainment area….."%the_id,
                        recipient_id=resipient)
                    )

            elif "163*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn3 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET extras='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn3,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*HOLIDAY ACCOMMODATION ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nIf you wish to attach an image to you advert\nAttach 164*%s to image and send\n*Enter SR to return to main menu* "%the_id,
                        recipient_id=resipient)
                    )

            elif "164*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                image_url = request.values['MediaUrl0']

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET img='%s' WHERE id='%s' AND number_id='%s'" %(image_url,the_id,resipient))

                mysql.connection.commit()

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT code FROM advert WHERE id='%s' AND number_id='%s'" %(the_id,resipient))

                ge = mycursor.fetchall()

                for idef in ge:

                    thecod = idef[0]

                return (messenger.send_message(
                        message="_______________________\n*END OF UPLOAD*\n*HOLIDAY ACCOMMODATION ADVERT*\n______________________\n\nThanks for the image!\nYour Advert has been successfully placed\nTo view it enter your advert code %s\n*Enter SR to return to main menu* "%thecod,
                        recipient_id=resipient)
                    )

                ##########################
                ##########################
                ##########################
            #end of HOLIDAY ACCOMMODATION upload section
            
            #Uploading HOLIDAY ACCOMMODATION FOR SALE section
                ##########################
                ##########################
                ##########################

            elif trimmed.upper() == "*690":

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT number FROM agents")

                agn = mycursor.fetchall()

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT number FROM agents")

                ang = mycursor.fetchall()

                for bn in agn:

                    if resipient in bn:

                        n = random.randint(1,99999)
                        cur_date = datetime.datetime.now()
                        cod = "RP" + str(n)
                        num = resipient
                        link = "https://wa.me/" + str(num)
                        adcod = "S12"
                        newdate = "*Date posted* : " + cur_date.strftime("%d-%b-%Y (%H:%M:%S)")

                        sql = "INSERT INTO advert (number_id, date, whatsapp, code, adcode) VALUES (%s, %s, %s, %s, %s)"
                        val = (resipient, newdate, link, cod, adcod)
                        mycursor = mysql.connection.cursor()
                        mycursor.execute(sql, val)

                        mysql.connection.commit()

                        mycursor = mysql.connection.cursor()

                        mycursor.execute("SELECT id FROM advert WHERE code = '%s'"%cod)

                        re = mycursor.fetchall()

                        for c in re:

                            the_id = str(c[0])

                        resp=messenger.send_message(
                                message="_______________________\n*UPLOADING*\n*HOLIDAY ACCOMMODATION FOR SALE ADVERT*\n______________________\n\nIn case you will need to correct an error, just enter\n\n\nThen choose appropriate code for your amendments\n\n165*%s*Location of property\n\n166*%s*Details of property\n\n167*%s*Rent for property\n\n168*%s*Extra facilities/amenities\n\n169*%s upload best picture"%(the_id,the_id,the_id,the_id,the_id),
                                recipient_id=resipient)

                        resp=messenger.send_message(
                                message="_______________________\n*UPLOADING*\n*HOLIDAY ACCOMMODATION FOR SALE ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\n\nYour advert code %s\n\nNow add location\n165*%s*Location of Property\n*Example* 165*%s*Masvingo, Great Zimbabwe" %(cod,the_id,the_id),
                                recipient_id=resipient)

                        return (resp)

                return (messenger.send_message(
                        message="Inorder to upload you need to register as an advertiser first\nEnter *550*1 to start registration process",
                        recipient_id=resipient
                        )
                    )


            elif "150*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn10 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET location='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn10,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*HOLIDAY ACCOMMODATION FOR SALE ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit details\n*Example* 151*%s*Conference facility, six chalets, eight canoes, 10 double rooms, 12 single rooms, restaurant, three private dining room."%the_id,
                        recipient_id=resipient)
                    )

            elif "151*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn1 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET details='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn1,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*HOLIDAY ACCOMMODATION FOR SALE ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit price\n*Example* 152*%s*US$1 600 000 Neg"%the_id,
                        recipient_id=resipient)
                    )


            elif "152*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn2 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET price='%s' WHERE id='%s' AND number_id='%s'" %("*Price* : " + trimmed_turn2,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*HOLIDAY ACCOMMODATION FOR SALE ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nNow add/edit extras if any\n*Example* 153*%s*railway siding, 24hrs security"%the_id,
                        recipient_id=resipient)
                    )

            elif "153*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                trimmed_turn3 = trimmed.split('*')[initial]

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET extras='%s' WHERE id='%s' AND number_id='%s'" %(trimmed_turn3,the_id,resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="_______________________\n*UPLOADING*\n*HOLIDAY ACCOMMODATION FOR SALE ADVERT*\n______________________\n\nThank you. Information has been successful uploaded\nIf you wish to attach an image to you advert\nAttach 154*%s to image and send\n*Enter SR to return to main menu* "%the_id,
                        recipient_id=resipient)
                    )

            elif "154*" in trimmed:

                initial = 2

                the_id = trimmed.split('*')[initial-1]

                image_url = request.values['MediaUrl0']

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE advert SET img='%s' WHERE id='%s' AND number_id='%s'" %(image_url,the_id,resipient))

                mysql.connection.commit()

                mycursor = mysql.connection.cursor()

                mycursor.execute("SELECT code FROM advert WHERE id='%s' AND number_id='%s'" %(the_id,resipient))

                ge = mycursor.fetchall()

                for idef in ge:

                    thecod = idef[0]

                return (messenger.send_message(
                        message="_______________________\n*END OF UPLOAD*\n*HOLIDAY ACCOMMODATION FOR SALE*\n______________________\n\nThanks for the image!\nYour Advert has been successfully placed\nTo view it enter your advert code %s\n*Enter SR to return to main menu* "%thecod,
                        recipient_id=resipient)
                    )

                ##########################
                ##########################
                ##########################
            #end of HOLIDAY ACCOMMODATION FOR SALE upload section
            
            elif "*LOGOS1" in trimmed:

                img_url = request.values['MediaUrl0']
                mycursor = mysql.connection.cursor()
                mycursor.execute("UPDATE headimg SET img = '%s' WHERE id = '1'"%img_url)
                mysql.connection.commit()

                return (messenger.send_message(
                        message="DONE!",
                        recipient_id=resipient)
                    )

            elif "*BANNERS1" in trimmed:

                img_url = request.values['MediaUrl0']
                mycursor = mysql.connection.cursor()
                mycursor.execute("UPDATE headimg SET img1 = '%s' WHERE id = '1'"%img_url)
                mysql.connection.commit()

                return (messenger.send_message(
                        message="DONE!",
                        recipient_id=resipient)
                    )

            elif trimmed == "activateMenow":

                start_date = datetime.datetime.now()

                plus = start_date + timedelta(days=300)

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE subscribers SET reg_time='%s' WHERE number='%s'" %(plus,resipient))

                mysql.connection.commit()

                mycursor = mysql.connection.cursor()

                mycursor.execute("UPDATE subscribers SET status='paid' WHERE number='%s'" %(resipient))

                mysql.connection.commit()

                return (messenger.send_message(
                        message="DONE!",
                        recipient_id=resipient)
                    )
            else:
                return (messenger.send_message(
                        message="I don't know this response, send me a *hi* to see what I can respond to",
                        recipient_id=resipient)
                    )


@app.route("/response", methods=["GET", "POST"])

def response():
    
    poll_url = response.poll_url

    print("Poll Url: ", poll_url)
    
    time.sleep(5)

    status = paynow.check_transaction_status(poll_url)
    
    json_res = request.get_json(force=True)

    print(json_res)
    
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Invalid verification token"
    return jsonify({"status": "success"}, 200)
    
    
    
    


if __name__ == "__main__":
    app.run(debug=True)