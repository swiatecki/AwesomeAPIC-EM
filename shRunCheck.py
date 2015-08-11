
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

def shRunChecker():
	# CALLS: reachability-info
	# Takes a list of switches as input for lookup

	url = settings.baseURL + "network-device/config"
	response = requests.get(url, verify=False)

	#Create a JSON object
	host_json = response.json()
	configs =  host_json["response"]


	result = {"name":"Config Checker","totalScore":0,"items":[],"description":"Analyses the output of the /network-device/config API and checks for running telnet, HTTP and HTTPS servers"}
	sumScore=[] # for calculating the total score
	hostsChecked=[]# temp for storing the hosts already in the list

	for d in configs:
		# Only analyze passwords which actually could login

			hostname = getDeviceByIDOnline(d["id"])["hostname"]
			#hostname = getDeviceByIDOffline(d["id"])["hostname"]
			if not hostname or hostname in hostsChecked:
				# No hostname available, break
				continue

			hostsChecked.append(hostname)	
			#Empty item
			item ={"id":"","comment":"","score":0}

			item["id"] = hostname


			#Parse the config (oh god!!)

			#Look for telnet! 

			item["score"]=5

			if "transport input telnet" in d["runningConfig"]:
				item["comment"] = "Telnet <span style='color:red'>found</span>."
				item["score"]+= -2
			else:
				if "transport input" in d["runningConfig"]:
					item["score"]+= -2
					item["comment"] = "<span style='color:red'>'<pre style='display:inline'>transport input</pre>'' not specified</span>"

			# !!! TODO: Add scoring



			# Look for non ssl htto

			if "ip http server" in d["runningConfig"] and "no ip http server" not in d["runningConfig"]:
				# Damn, there is a HTTP server running!
				item["comment"]+= " <span style='color:red'>HTTP server found</span>"
				item["score"]+= -1
			else:
				item["comment"]+= " <span style='color:green'>no HTTP server found</span>"
				item["score"]+= 0

			if "ip http secure-server" in d["runningConfig"] and "no ip http secure-server" not in d["runningConfig"]:
				item["comment"]+= " <span style='color:green'>HTTPS server found</span>"
				item["score"]+= 5
				# HTTPS <3 



			sumScore.append(item["score"])
			result["items"].append(item)	


	
		# calculate the avg. of the scores
	result["totalScore"] = round(sum(sumScore)/float(len(sumScore)),1)
	#result["totalScore"] =4
	return result