from settings import *
import requests
import json
import traceback

def getDeviceByIDOffline(id):
	deviceURL = baseUrl + "network-device"
	url = deviceURL + "/"+id
	response = requests.get(url, verify=False)
	if response.status_code == requests.codes.ok:
		hjson = response.json()
		parent =  hjson["response"]
		return parent
	else:
		return None

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