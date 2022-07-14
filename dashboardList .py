from getpass import getuser
from tkinter import Y
from typing import List
import requests
import json
import csv

tokenSfx = "AAAAAAAAAAAAAAAA"
headerSfx = "X-SF-TOKEN"
baseUrl= "https://api.us1.signalfx.com/v2"
header = ['name', 'DashboardGroup', 'creator']
data = []


def getUserList ():
    response = requests.get(baseUrl+"/organization/member",headers = {headerSfx: tokenSfx})
    list = json.loads(response.text)["results"]
    
    return list

userList = getUserList()

def getName (id):

    for user in userList:
        if user["userId"] == id:
            return user["fullName"]
        elif "AAAAAAAAAAA" == id:
            return "SignalFx Created"
    
    return "Not Find"



def getList():
    response = requests.get(baseUrl+"/dashboard",headers = {headerSfx: tokenSfx})
    answer = json.loads(response.text)
    return answer["results"]





list = getList()
print(list)
for dashboard in list:
    #print( dashboard["name"]+","+dashboard["groupName"]+","+getName(dashboard["creator"])+","+dashboard["creator"])
    print( dashboard["name"]+","+dashboard["groupName"]+","+getName(dashboard["creator"]))