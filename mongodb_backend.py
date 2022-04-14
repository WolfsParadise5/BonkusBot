from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

#Test database connection
try:
    toPasstoDB = "mongodb+srv://" + str(os.getenv("USERNAME_DB"))  + ":" + str(os.getenv("USERNAME_PSWD")) + "@cluster0.efk8g.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    cluster = MongoClient(toPasstoDB)
    db = cluster["BonkusDB"]
    collection = db["Reminder"]
    print("Database connected successfully!")
except:
    print("Database could not be connected, functions may be limited")

def getAllReminders():
    return collection.find({})


def getIDFromReminders() :
    #Get the latest ID
    result = getAllReminders()
    id = "R000R"
    for i in result:
        id = i["_id"]
    
    #Add by 1 and return
    return str(int(id[3:4])+1)


def postNewPost(username, cryptoOfChoice, price):
    print(username)
    #Build post
    post = {"_id": "R00" + getIDFromReminders() + "R", "username":username, "reminder":cryptoOfChoice, "price":price}   
    #Post to database
    collection.insert_one(post)

def deletePost(id) :
    collection.delete_one({"_id": id})


