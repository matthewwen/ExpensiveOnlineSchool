from fastapi import FastAPI
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import sys
import sqlite3
import re
import copy
import numpy as np
sys.path.append('ext')

from algo import *
from stralgo import *

class PROGRAM_LIST:
    REF_LIST:json
    SORTED_LIST:list
    POP_LIST:json
    MAX_WORD:int

def update_helper(limit=False):
    REF_LIST = None
    try:
        with open('collegeName.txt') as json_file:
            REF_LIST = json.load(json_file)

        MAX_WORD = 0
        for item in REF_LIST["data"]:
            word = re.split(r'\s|-', item["name"])
            MAX_WORD = MAX_WORD if len(word) < MAX_WORD else len(word)

        SORTED_LIST = []
        
        num_query = MAX_WORD
        for i in range(num_query):
            temp = copy.deepcopy(REF_LIST)
            temp["data"] = change_list(i, temp["data"])
            temp["data"] = sort_function(temp["data"], "name")
            SORTED_LIST.append(temp)

        POP_LIST = copy.deepcopy(REF_LIST)
        POP_LIST["data"] = sort_function(POP_LIST["data"], "pop", dist=1)

        return [REF_LIST, SORTED_LIST, POP_LIST, MAX_WORD]
    except:
        return [None, None, None, 0]

app = FastAPI(docs_url=None, redoc_url=None)
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        )

QUERY_LIMIT = 100
[PROGRAM_LIST.REF_LIST, PROGRAM_LIST.SORTED_LIST, PROGRAM_LIST.POP_LIST, PROGRAM_LIST.MAX_WORD] = update_helper()

@app.get("/")
async def root():
    return {"active": True, "queryList": True, "search": False}

@app.get("/college")
async def get_college():
    if PROGRAM_LIST.POP_LIST == None:
        return {"error", "Database Failure"}
    returnResult = []
    for index, item in zip(range(QUERY_LIMIT), PROGRAM_LIST.POP_LIST["data"]):
        returnResult.append({"id": item["id"], "name": item["name"], "online": item["online"]})
    return returnResult

@app.get("/detail")
async def get_detail(collegeid: int):
    if PROGRAM_LIST.REF_LIST == None:
        return {"error", "Database Failure"}
    return get_obj(PROGRAM_LIST.REF_LIST["data"], collegeid)

class hrefContent(BaseModel):
    collegeid: int = 1
    msg: str = ""
    href: str = ""
    online: bool = True

@app.post("/addhref/")
async def process_post(college: hrefContent):
    try:
        conn = sqlite3.connect("request.db")
        c    = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS REQUEST (id INTEGER, msg TEXT, href TEXT, online INTEGER)")
        insertStr = "INSERT INTO REQUEST(id, msg, href, online) VALUES({},\"{}\",\"{}\",{});".format(college.collegeid, college.msg, college.href, 1 if college.online else 0)
        c.execute(insertStr)
        conn.commit()
        conn.close()
        return {"success":True} 
    except:
        return {"success":False} 

@app.get("/search")
async def search_query(query: str):
    try:
        query = query.lower()
        queryList = []
        for i, listItem in zip(range(len(PROGRAM_LIST.SORTED_LIST)), PROGRAM_LIST.SORTED_LIST):
            tempList = []
            binary_search(listItem["data"], query, tempList, index=i)

            for temp in tempList:
                inQuery = False
                for queryItem in queryList:
                    inQuery = inQuery or queryItem["id"] == temp["id"]
                if not inQuery: 
                    parentObj = get_obj(PROGRAM_LIST.REF_LIST["data"], temp["id"])
                    if parentObj != None:
                        queryList.append(parentObj)


        return sort_function(queryList, "pop", dist=1)
    except:
        return {"success": False} 

@app.get("/update")
async def update_memory(temp: str):
    if temp == "mwen-kushal":
        [PROGRAM_LIST.REF_LIST, PROGRAM_LIST.SORTED_LIST, PROGRAM_LIST.POP_LIST, PROGRAM_LIST.MAX_WORD] = update_helper(limit=True)
        return {"updated":True}
    return {"updated":False}
