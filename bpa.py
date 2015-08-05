from utils import *
import requests
import passwordCheck
import reportBuilder
requests.packages.urllib3.disable_warnings() #Fix request's warnings




if __name__ == "__main__":
	#Start our program
	print("Launching BPA v0.1")
	global devices 
	devices = getAllNetworkDevices()
	#print(devices)

	scans = []

	# Add scans below here
	scans.append(passwordCheck.passwordChecker())
	scans.append(passwordCheck.passwordChecker())
	# Don't edit below this! 
	print(json.dumps(scans[0],indent=4,separators=(',', ': ')))
	report = reportBuilder.build(scans)

	f = open("report.html","w")
	f.write(report)
	f.close()

