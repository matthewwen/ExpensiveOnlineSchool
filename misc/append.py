import json
import sqlite3
import sys

sys.path.append("../ext")

from algo import *
from stralgo import *

class TEMP():
    test:json=None
    request:list=None

def get_json():
    if TEMP.test == None:
        test = None
        with open('../collegeName.txt') as json_file:
            test = json.load(json_file)
        TEMP.test = test

def get_request(id=None):
    if TEMP.request == None:
        requestlist = []
        conn = sqlite3.connect('request.db')
        c = conn.cursor()
        i = 0
        for row in c.execute("SELECT * FROM REQUEST"):
            id = int(row[0])
            name = row[1]
            href = row[2]
            online = int(row[3]) == 1
            requestlist.append({"id": i, "collegeid": id, \
                    "msg": name, "href": href, "online": online})
            i+=1
        conn.close()
        print("hello")
        TEMP.request = requestlist

    if id != None:
        for item in TEMP.request:
            if item["id"] == id:
                return item

def save_json():
    get_json()
    for item in TEMP.request:
        obj = get_obj(TEMP.test["data"], item["collegeid"])
        obj["href"].append({"msg": item["msg"], \
                "href": item["href"]})
        obj["pop"] = 100
        obj["online"] = item["online"] 

    with open('collegeName.txt', "w") as json_file:
        json.dump(TEMP.test, json_file)

def read_request():
    get_request()
    for item in TEMP.request:
        print(item)

def edit_request(id, msg=None, href=None):
    obj = get_request(id=id)
    if obj != None and msg != None:
        obj["msg"] = msg
    if obj != None and href != None:
        obj["href"] = href

def remove_request(id):
    newList = []
    for item in TEMP.request:
        if item["id"] != id:
            newList.append(item)
    TEMP.request = newList

def remove_requests(idList):
    for i in idList:
        remove_request(i)
