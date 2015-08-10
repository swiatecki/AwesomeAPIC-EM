import settings
import requests

# import the json library.  This provides many handy features for formatting, displaying
# and manipulating json.  https://docs.python.org/2/library/json.html
import json

def versionChecker():
	# All of our REST calls will use the url for the APIC EM Controller as the base URL
	# So lets define a variable for the controller IP or DNS so we don't have to keep typing it
	controller_url = settings.baseURL
	# Get Devices
	# This function allows you to view a list of all the devices in the network(routers and switches).
	get_devices_url = controller_url + 'network-device'

	#Perform GET on get_devices_url
	get_devices_response = requests.get(get_devices_url, verify=False)

	# The json method of the response object returned by requests.get returns the request body in json format
	get_devices_json = get_devices_response.json()

	# Now let's read and display some specific information from the json

	# set our parent as the top level response object
	parent =  get_devices_json["response"]

	# for each device returned, print the networkDeviceId
	familyswitch = []
	familyrouter = []
	for item in parent:
		#print ("Family = " + item["family"] + " type = " + item["type"] + " software = " + item["softwareVersion"])
		if item["type"] == "ROUTER":
			familyrouter.append(item["family"])
		if item["type"] == "SWITCH":
			familyswitch.append(item["family"])

	switches = []
	routers = []
	for item in parent:
		item["family_duplicates"] = 0
		item["software_duplicates_equal"] = 0 #Number of equal versions to me.
		item["software_duplicates_newer"] = 0 #Number newer versions than me.
		item["software_duplicates_older"] = 0 #Number older versions than me.
		item["newer_software"] = 0 # Newest software version
		item["newer_hostname"] = 0 # Device with newer software
		if item["type"] == "ROUTER":
			routers.append(item)
		if item["type"] == "SWITCH":
			switches.append(item)

	#Let's count the number of duplicates for each family of routers.
	for i in range(0,len(routers)):
		for j in range(i+1,len(routers)):
			if(routers[i]["family"]==routers[j]["family"]):
				routers[i]["family_duplicates"]=routers[i]["family_duplicates"]+1
				routers[j]["family_duplicates"]=routers[j]["family_duplicates"]+1
				if(routers[i]["softwareVersion"]==routers[j]["softwareVersion"]):
					routers[i]["software_duplicates_equal"]=routers[i]["software_duplicates_equal"]+1
					routers[j]["software_duplicates_equal"]=routers[j]["software_duplicates_equal"]+1
				if(routers[i]["softwareVersion"]<routers[j]["softwareVersion"]):
					routers[i]["newer_software"] = routers[j]["softwareVersion"]
					routers[i]["newer_hostname"] = routers[j]["hostname"]
					routers[i]["software_duplicates_newer"]=routers[i]["software_duplicates_newer"]+1
					routers[j]["software_duplicates_older"]=routers[j]["software_duplicates_older"]+1
				if(routers[i]["softwareVersion"]>routers[j]["softwareVersion"]):
					routers[i]["software_duplicates_older"]=routers[i]["software_duplicates_older"]+1
					routers[j]["software_duplicates_newer"]=routers[j]["software_duplicates_newer"]+1

	#Let's count the number of duplicates for each family of switches.
	for i in range(0,len(switches)):
		for j in range(i+1,len(switches)):
			if(switches[i]["family"]==switches[j]["family"]):
				switches[i]["family_duplicates"]=switches[i]["family_duplicates"]+1
				switches[j]["family_duplicates"]=switches[j]["family_duplicates"]+1
				if(switches[i]["softwareVersion"]==switches[j]["softwareVersion"]):
					switches[i]["software_duplicates_equal"]=switches[i]["software_duplicates_equal"]+1
					switches[j]["software_duplicates_equal"]=switches[j]["software_duplicates_equal"]+1
				if(switches[i]["softwareVersion"]<switches[j]["softwareVersion"]):
					switches[i]["newer_software"] = switches[j]["softwareVersion"]
					switches[i]["newer_hostname"] = switches[j]["hostname"]
					switches[i]["software_duplicates_newer"]=switches[i]["software_duplicates_newer"]+1
					switches[j]["software_duplicates_older"]=switches[j]["software_duplicates_older"]+1
				if(switches[i]["softwareVersion"]>switches[j]["softwareVersion"]):
					switches[i]["software_duplicates_older"]=switches[i]["software_duplicates_older"]+1
					switches[j]["software_duplicates_newer"]=switches[j]["software_duplicates_newer"]+1

	result = {"name":"Software Version Checker","totalScore":0,"items":[]}


	#print("\n\nSWITCHES:")
	badscore = 0
	for item in switches:
		line ={"id":"","comment":"","score":0}
		#print ("Family = " + item["family"] + " software = " + item["softwareVersion"]+" Family Duplicates = %d\nDuplicate Software = %d Newer Software = %d Older Software = %d\n" % (item["family_duplicates"], item["software_duplicates_equal"], item["software_duplicates_newer"], item["software_duplicates_older"]))
		line["id"] = item["hostname"]
		result["items"].append(line)
		if item["software_duplicates_newer"] > 0:
			badscore = badscore +1
			line["score"] = 1
			line["comment"] = " Current software = " + item["softwareVersion"] + ", Newest software (device) = " + item["newer_software"] + " (" + item["newer_hostname"] + ")"
		else:
			line["score"] = 10
			line["comment"] = " Current software = " + item["softwareVersion"]
	#print("\n\nROUTERS:")
	for item in routers:
		line ={"id":"","comment":"","score":0}
		line["id"] = item["hostname"]	
		result["items"].append(line)
		if item["software_duplicates_newer"] > 0:
			badscore = badscore +1
			line["score"] = 1
			line["comment"] = " Current software = " + item["softwareVersion"] + ", Newest software (device) = " + item["newer_software"] + " (" + item["newer_hostname"] + ")"
		else:
			line["score"] = 10
			line["comment"] = " Current software = " + item["softwareVersion"]
		#print ("Family = " + item["family"] + " software = " + item["softwareVersion"]+" Family Duplicates = %d\nDuplicate Software = %d Newer Software = %d Older Software = %d\n" % (item["family_duplicates"], item["software_duplicates_equal"], item["software_duplicates_newer"], item["software_duplicates_older"]))
	result["totalScore"] = round(((len(switches)+len(routers))-badscore)/(len(switches)+len(routers))*10,0)
	#print(json.dumps(result,indent=4,separators=(',', ': ')))
#versionChecker()
	return result