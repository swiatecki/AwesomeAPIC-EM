from utils import *
import requests
import passwordCheck
requests.packages.urllib3.disable_warnings() #Fix request's warnings


global devices


if __name__ == "__main__":
	#Start our program
	print("Launching BPA v0.1")
	devices = getAllNetworkDevices()

	passwordItems = passwordCheck.passwordChecker()
	#print(passwordItems)


