import requests 
import json
import base64
requests.packages.urllib3.disable_warnings()


baseUrl = "https://173.38.218.144/api/v0/"

url = baseUrl + "reachability-info"
#url = baseUrl + "device-credential"

# this statement performs a GET on the specified url
# the verify varibale is to ignore SSL errors
response = requests.get(url, verify=False)


def getDeviceByID(id):
	deviceURL = baseUrl + "network-device"
	url = deviceURL + "/"+id
	response = requests.get(url, verify=False)
	if response.status_code == requests.codes.ok:
		hjson = response.json()
		p =  hjson["response"]
		#print(p)
		return p["hostname"]
	else:
		print("error")


#Create a JSON object
host_json = response.json()

# print the json that is returned
#print(response.text)
#print(json.dumps(host_json,indent=4,separators=(',', ': ')))

# set our parent as the top level response object
parent =  host_json["response"]

for d in parent:
	#print("ID is: " + d["id"] + ", and type is: " + d["type"] + "(S/N:" + d["serialNumber"] + ")" )
	hostname = getDeviceByID(d["id"])
	if not hostname:
		continue

	decode = str(base64.b64decode(d["password"]))

	print("Hostname:" + hostname,end="")
	print(" #" + d["id"] + \
		" # mgmtIp: " + d["mgmtIp"] + \
		" # discoveryId: " + d["discoveryId"] + \
		" # reachabilityStatus: " + d["reachabilityStatus"] + \
		" # protocolUsed: " + d["protocolUsed"] + \
		" # protocolList: " + d["protocolList"] + \
		" # discoveryStartTime: " + d["discoveryStartTime"] + \
		" #  Username:"+ d["userName"] + \
		" # Password: " + decode \
		,end="")
	if "enablePassword" in d:
		decodeEn = str(base64.b64decode(d["enablePassword"]))
		print (" # Enable password: " + decodeEn )

	"""print(hostname,end="")
	print(";"+d["id"] + \
		";" + d["discoveryId"] + \
		";" + d["reachabilityStatus"] + \
		";" + d["protocolUsed"] + \
		";" + d["protocolList"] + \
		";" + d["discoveryStartTime"] + \
		";"+ d["userName"] + \
		";" + decode \
		)
	if "enablePassword" in d:
		decodeEn = str(base64.b64decode(d["enablePassword"]))
		print ("," + decodeEn )	"""


print("*********")
print("Total of " + str(len(parent)) + " devices") 
