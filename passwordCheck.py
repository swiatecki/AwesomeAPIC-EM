
import settings
from utils import *
import json
import base64
import requests
from bpa import *
import re


#Author: Nicholas Swiatecki <nicholas@swiatecki.com>

# TODO
# 1) Change online lookups of ID -> hostname from "online" to "offline" 
#	Would optimize runtime a lot

def passwordChecker():
	# CALLS: reachability-info
	# Takes a list of switches as input for lookup

	url = settings.baseURL + "reachability-info"
	response = requests.get(url, verify=False)

	#Create a JSON object
	host_json = response.json()
	reach =  host_json["response"]


	result = {"name":"Password Complexity Check","totalScore":0,"items":[]}
	sumScore=[] # for calculating the total score
	hostsChecked=[]# temp for storing the hosts already in the list
	for d in reach:
		# Only analyze passwords which actually could login
		if d["reachabilityStatus"].lower() == "success":

			hostname = getDeviceByIDOnline(d["id"])["hostname"]
			#hostname = getDeviceByIDOffline(d["id"])["hostname"]
			if not hostname or hostname in hostsChecked:
				# No hostname available, break
				continue

			hostsChecked.append(hostname)	
			decoded = base64.b64decode(d["password"]).decode()
			#Empty item
			item ={"id":"","comment":"","score":0}

			item["id"] = hostname + " (Protocol: " + d["protocolUsed"] + ")"

			item["comment"] = "Username: "+ d["userName"] +" (Password: " + decoded + ")"

			# Lets look at the password first
			# We want a password that has: 2 uppercase, one special, 2 numbers, minimum 8 i total
			# Regex is magic
			if(re.match(r'^(?=.*[A-Z].*[A-Z])(?=.*[!@#$&*])(?=.*[0-9].*[0-9])(?=.*[a-z].*[a-z].*[a-z]).{8,}$',decoded)):
				item["comment"]+= ", Strength: <span style='color:green;'>Good</span>"
				item["score"] = 10
			else:
				item["comment"]+= ", Strength: <span style='color:red;'>Sucks</span>"
				item["score"] = 4


			#If the enable password exsists analyze this
			
			if "enablePassword" in d:
				decodeEn = base64.b64decode(d["enablePassword"]).decode()
				

				if(re.match(r'^(?=.*[A-Z].*[A-Z])(?=.*[!@#$&*])(?=.*[0-9].*[0-9])(?=.*[a-z].*[a-z].*[a-z]).{8,}$',decodeEn)):
					item["comment"]+= ", Enable PW: "+decodeEn+" Strength: <span style='color:green;'>Good</span>"
					item["score"]+= 6
				else:
					item["comment"]+= ", Enable PW: "+decodeEn+" Strength: <span style='color:red;'>Sucks</span>"
					item["score"]+=-3 #Note this is -= as it is negative
			else:
				print("Hmm, the enablePassword hash is:" + d["enablePassword"])
			sumScore.append(item["score"])
			result["items"].append(item)		

			

			
		else:
			pass 
			# Non-reachable discovery results not included
	# calculate the avg. of the scores
	result["totalScore"] = sum(sumScore)/float(len(sumScore))		
	return result