#Author: Nicholas Swiatecki <nicholas@swiatecki.com>
from utils import *
import requests
requests.packages.urllib3.disable_warnings() #Fix request's warnings
import reportBuilder
import settings
import os

""" Import your Modules below """
import passwordCheck
import shRunCheck
import DOFchecker
import portCheck
import versionCheck


if __name__ == "__main__":
	#Start our program
	print("Launching BPA v0.1")
	global devices 

	devices = getAllNetworkDevices()

	scans = [] # To store the results in

	# Add scans below here
	
	scans.append(passwordCheck.passwordChecker())
	scans.append(shRunCheck.shRunChecker())
	scans.append(DOFchecker.DOFchecker())
	scans.append(portCheck.portSpeedCheck())
	scans.append(versionCheck.versionChecker())
	
	
	"""Don't edit below this!  """
	#print(json.dumps(scans[0],indent=4,separators=(',', ': ')))

	#Build report, and write to a file
	
	report = reportBuilder.build(scans)
	f = open(settings.reportFileName,"w")
	f.write(report)
	f.close()

	print("****** DiCK!  Success! Report in: " + settings.reportFileName)

	# Launch a webbrowser with the newly generated report
	os.startfile(settings.reportFileName)