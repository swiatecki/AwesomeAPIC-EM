from utils import *
import requests
import passwordCheck
import reportBuilder
import EOLchecker
import settings
import os
requests.packages.urllib3.disable_warnings() #Fix request's warnings

#Author: Nicholas Swiatecki <nicholas@swiatecki.com>


if __name__ == "__main__":
	#Start our program
	print("Launching BPA v0.1")
	global devices 
	devices = getAllNetworkDevices()
	#print(devices)

	scans = [] # To store the results in

	# Add scans below here
	scans.append(passwordCheck.passwordChecker())
	scans.append(EOLchecker.DOFchecker())
	# Don't edit below this! 
	#print(json.dumps(scans[0],indent=4,separators=(',', ': ')))

	#Build report, and write to a file
	report = reportBuilder.build(scans)
	f = open(settings.reportFileName,"w")
	f.write(report)
	f.close()

	print("****** DiCK!  Success! Report in: " + settings.reportFileName)

	os.startfile(settings.reportFileName)