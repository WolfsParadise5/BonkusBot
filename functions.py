import os
import json
import requests
import random

#Insert Bitrue API keycode here
keycode = ""

#Bitrue
def checkBitrue(keypair):
    url = "https://www.bitrue.com/api/v1/ticker/price?symbol="
    key = {'X-MBX-APIKEY':keycode}
    url += keypair
    r = requests.get(url,params=key)
    return r.text

#Save to savefile
def pickleToFile(dictSaves):
    #Check if the save file exists
    if os.path.exists("save.txt"):
        openFile = open("save.txt", "rb")
        currentList = json.load(openFile)
        currentList.append(dictSaves)
        openFile.close()

    else:
        currentList = []
        currentList.append(dictSaves)

    pickleSave = open("save.txt", "w")
    json.dump(currentList, pickleSave)
    pickleSave.close()

    return True
