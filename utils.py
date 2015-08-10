from settings import *
import requests
import json
import traceback
import time

devices = []

def getDeviceByIDOffline(id):
	#todo
	pass

def getDeviceByIDOnline(id):
	deviceURL = baseURL + "network-device"
	url = deviceURL + "/"+id
	response = requests.get(url, verify=False)
	if response.status_code == requests.codes.ok:
		hjson = response.json()
		parent =  hjson["response"]
		return parent
	else:
		return None		

def getAllNetworkDevices():
	deviceURL = baseURL + "network-device"
	url = deviceURL + "/"
	try:
		response = requests.get(url, verify=False)
		if response.status_code == requests.codes.ok:
			hjson = response.json()

			parent =  hjson["response"]
			#print(json.dumps(parent,indent=4,separators=(',', ': ')))
			return parent
		else:
			print("fuck")
			raise Exception('My error!')
	except:
		print("Get getAllNetworkDevices failed!")
		print(traceback.format_exc())


def testUtils():
	print("Util works")

def tic():
	#Homemade version of matlab tic and toc functions
	global startTime_for_tictoc
	startTime_for_tictoc = time.time()

def toc():
    import time
    if 'startTime_for_tictoc' in globals():
        print ("Elapsed time is " + str(time.time() - startTime_for_tictoc) + " seconds.")
    else:
        print ("Toc: start time not set")