from utils import *
import requests
import passwordCheck
requests.packages.urllib3.disable_warnings() #Fix request's warnings




if __name__ == "__main__":
	#Start our program
	print("Launching BPA v0.1")
	global devices 
	devices = getAllNetworkDevices()
	#print(devices)

	passwordItems = passwordCheck.passwordChecker()
	print(json.dumps(passwordItems,indent=4,separators=(',', ': ')))


