import settings
from utils import *
import json
import base64
import requests
from bpa import *
import re


#Author: Nicholas Swiatecki <nicholas@swiatecki.com>

def passwordChecker():
	# CALLS: reachability-info
	# Takes a list of switches as input for lookup

	url = settings.baseURL + "reachability-info"
	response = requests.get(url, verify=False)

	#Create a JSON object
	host_json = response.json()
	reach =  host_json["response"]


	items = []

	for d in reach:
		# Only analyze passwords which actually could login
		if d["reachabilityStatus"].lower() == "success":

			hostname = getDeviceByIDOnline(d["id"])["hostname"]
			if not hostname:
				# No hostname available, break
				continue

			decode = str(base64.b64decode(d["password"]))
			#Empty item
			item ={"id":"","comment":"","score":0}

			item["id"] = hostname

			item["comment"] = "Username:"+ d["userName"] +"(Password: " + decode + ")"

			# Lets look at the password first
			# We want a password that has: 2 uppercase, one special, 2 numbers, minimum 8 i total
			# Regex is magic
			if(re.match(r'^(?=.*[A-Z].*[A-Z])(?=.*[!@#$&*])(?=.*[0-9].*[0-9])(?=.*[a-z].*[a-z].*[a-z]).{8,}$',decode)):
				item["comment"]+= "# Strength: Good"
				item["core"] = 10
			else:
				item["comment"]+= "# Strength: Sucks"
				item["score"] = 4


			#If the enable password exsists analyze this
			
			if "enablePassword" in d:
				decodeEn = str(base64.b64decode(d["enablePassword"]))
				#print ("(Enable password: " + decodeEn + ")" )

				if(re.match(r'^(?=.*[A-Z].*[A-Z])(?=.*[!@#$&*])(?=.*[0-9].*[0-9])(?=.*[a-z].*[a-z].*[a-z]).{8,}$',decode)):
					item["comment"]+= "# Enable Strength: Good"
					item["score"]+= 6
				else:
					item["comment"]+= "# Enable Strength: Sucks"
					item["score"]+=-3 #Note this is -= as it is negative
			


			items.append(item)		
		else:
			pass 
			# Not reachable
	return items