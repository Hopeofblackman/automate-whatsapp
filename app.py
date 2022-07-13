from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime

cluster = MongoClient("mongodb+srv://Aaron7210:Aaron7210@cluster0.xrxjowf.mongodb.net/?retryWrites=true&w=majority")
db = cluster["MyCityDeliverydemo"]
users = db["users"]
orders = db["orders"]

app = Flask(__name__)


@app.route("/", methods=["get", "post"])
def reply():
    text = request.form.get("Body")
    number = request.form.get("From")
    number = number.replace("whatsapp:", "")
    res = MessagingResponse()
    user = users.find_one({"number": number})

    if bool(user) == False:
        res.message("Hi welcome to *MyCityDelivery* please choose an option : \n 1 Food delivery \n 2 Liqour Delivery \n 3 Track my order \n 4 Partner with us")
        users.insert_one({"number": number, "status": "main", "messages": []})

    elif user["status"] == "main":
        try:
            option = int(text)
        except:
            res.message("please choose option 1 - 4 : \n 1 Food delivery \n 2 Liqour Delivery \n 3 Track my order \n 4 Partner with us")
            return str(res)

        if option == 1:
            res.message(" you've entered Food Delivery Mode")
            users.update_one({"number": number}, {"$set": {"status": "FoodDelivery"}})
            res.message(" please pick your restaraunt: \n 1 KFC \n 2 PEDROS \n 3 CHILLAX \n 4 Vaal Fisheries \n 0 back to menu \n 00 view menu")
        elif option == 2:
            res.message("you have entered liquorDelivery (18+)")
            users.update_one({"number": number}, {"$set": {"status": "LiqourDelivery"}})
            res.message(" please choose a liqour shop  \n 1 Blue bottles \n 2 overland \n 3 ultraliquor \n  00 view mne, \n 0 back to menu")
        elif option == 3:
            res.message("youve enter ordering mode ")
            res.message(" please enter your order number and proof of payment")
        elif option == 4:
            res.message("i am a *creation of mutsvanga_industries")
        else:
            res.message("please choose option 1 - 4 : \n 1 Food delivery \n 2 Liqour Delivery \n 3 Track my order \n 4 Partner with us")



    elif user["status"] == "FoodDelivery":
        try:
            option = int(text)
        except:
            res.message("please choose option 1 - 4 : \n 1 KFC \n 2 PEDROS \n 3 CHILLAX \n 5 Vaal Fisheries \n 0 back to  menu")
            return str(res)
        if option == 0:
            users.update_one({"number": number}, {"$set": {"status": "main"}})
            res.message("please choose option 1 - 4 : \n 1 Food delivery \n 2 Liqour Delivery \n 3 Track my order \n 4 Partner with us")

        elif 1 <= option <= 4:
            food = ["kfc", "pedros", "chillax", "vaalfisheries"]
            selected = food[option - 1]
            users.update_one({"number": number}, {"$set": {"status": "address"}})
            users.update_one({"number": number}, {"$set": {"item": selected}})
            res.message(" please enter your address to continue ordering ")
        else:
            res.message("please choose a restaraunt")


    elif user["status"] == "LiqourDelivery":
        try:
            option = int(text)
        except:
            res.message(" please choose a liqour store: \n 1 ultraliqours \n 2 vison meat \n 3 bluebootles, \n 0 back to menu")
            return str(res)
        if option == 0:
            users.update_one({"number": number}, {"$set": {"status": "main"}})
            res.message("please choose option 1 - 4 : \n 1 Food delivery \n 2 Liqour Delivery \n 3 Track my order \n 4 Partner with us")
        elif 1 <= option <= 3:
            stores = ["ultraliqou", "vision meat", "bluebootles"]
            selected = stores[option - 1]
            users.update_one({"number": number}, {"$set": {"status": "address"}})
            users.update_one({"number": number}, {"$set": {"item": selected}})
            res.message("please enter your address to continue ordering")
            res.message("an id picture will be required upon delivery")
        else:
            res.message("please choose a liquor store")

    elif user["status"] == "address":
        selected = user["item"]
        res.message(f"lets continue ordring {selected}")
        res.message("please type in your the meal of choose")
        orders.insert_one({"number": number, "item": selected, "address": text, "order_time": datetime.now()})
        users.update_one({"number": number}, {"$set": {"status": "ordered"}})

    elif user["status"] == "ordered":
        res.message(f"great your {text}  will be confirmed in 1 - 3 mins")
        users.update_one({"number": number}, {"$set": {"status": "main"}})
    users.update_one({"number": number}, {"$push": {"messages": {"text": text, "date": datetime.now()}}})
   # msg = res.message(f"okay '{text}' number is {number}")
    #msg.media("https://robocrop.realpython.net/?url=https%3A//files.realpython.com/media/Conditional-Statements-in-Python_Watermarked.b6b7d30ff62b.jpg&w=960&sig=2bc1ba6f83d3338105a6c31fbe3ae8e9be51e0b3")
    return str(res)

if __name__ == "__main__":
    app.run()
