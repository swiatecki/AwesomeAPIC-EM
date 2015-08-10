# Port speed vs. used speed
# July 2015, Juulia Santala

import requests
import json
from settings import *
from utils import*

requests.packages.urllib3.disable_warnings() #Fix request's warnings


def portSpeedCheck():
    interfaceURL = baseURL + "interface"
    interfaceResponse = requests.get(interfaceURL, verify=False).json()
    parent = interfaceResponse["response"]
    
    noMatch = []
    noMatchName = []
    total = 0
    totaldown = 0
    
    for item in parent:
        try:
            name = item["portName"]
            speed = item["speed"]
            itype = item["interfaceType"]
            ID = item["deviceId"]

            #Making sure, that the ports are physical
            if itype[0:4] == "Virt":
                continue
            #Checking, that the port status is up
            elif item["status"] == "down":
                totaldown += 1
                continue

            #Checking the speed
            if name[0:4] == "Ethe" and speed != 10000: #ethernet
                noMatch.append(ID)
                noMatchName.append(item["portName"])
            elif name[0:4] == "Fast" and speed != 100000: #fast ethernet
                noMatch.append(ID)
                noMatchName.append(item["portName"])
            elif name[0:4] == "Giga" and speed != 1000000: #gigabit ethernet
                noMatch.append(ID)
                noMatchName.append(item["portName"])
            elif name[0:4] == "TenG" and speed != 10000000: #tengigabit ethernet
                noMatch.append(ID)
                noMatchName.append(item["portName"])
            total = total + 1
        except:
            continue
        
    #Calculating usagerate
    usagerate = round(total/(total+totaldown), 3)
    usage = "The usagerate is <b>" + str(round((usagerate*100),1)) + " %</b>"
    scoreUsage = round(usagerate * 10)

    #creating comments for match-analysis
    matchlen = total-len(noMatch)
    match = "The amount of matches in the network: <b>" + str(matchlen) + "</b>"
    nomatch = "The amount of mismatches in the network: <b>" + str(len(noMatch)) + "</b>\n"

    #Calculating the scores
    scoreMatch = round(((total-len(noMatch))*10/total),2)
    scoreMisM = round((len(noMatch)*1/total),2)
    scoreMatchMisM = round(((total-len(noMatch))*10+len(noMatch)*1)/(total),2)
    totalS = 0.8 * scoreMatchMisM + 0.2 * scoreUsage

    items = [{'id':'Usage rate', 'comment':usage, 'score':scoreUsage},
             {'id':'Match', 'comment':match, 'score':round(scoreMatch)},
             {'id':'Mismatch', 'comment':nomatch, 'score':round(scoreMisM)}
             ]
    #If there is mismatches:
    if len(noMatch) != 0:
        listOfNoMatch = ""
        j = 0
        for i in noMatch:
            hostname = getDeviceByIDOnline(i)["hostname"]
            listOfNoMatch += hostname + ", port: " + noMatchName[j] + "<br>"
            j += 1
        listOfNoMatch = "<br><u>List of mismatching devices</u> <br>" + listOfNoMatch
        noMatchLine = {'id':'', 'comment': listOfNoMatch, 'score':''}
        items.append(noMatchLine)
        
    #Final format:
    d = {'name': 'Port Speed Check', 'totalScore': round(totalS, 1), 'items': items}

    return d
