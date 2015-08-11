# import the requests library so we can use it to make REST calls (http://docs.python-requests.org/en/latest/index.html)
import requests

# import the json library.  This library gives us many handy features for formatting, displaying 
# and manipulating json.
import json
import utils
#from utils import*
from settings import*
requests.packages.urllib3.disable_warnings() #Fix request's warnings

def DOFchecker():
	result = {"name":"Date of Fabrication","totalScore":0,"items":[],"description":"Calls the /network-device API and extracts the fabrication date of devices on the network from their serial number."}

	interfaceURL = baseURL + "network-device"
	interfaceResponse = requests.get(interfaceURL, verify=False).json()
	parent = interfaceResponse["response"]


	itemlist = [] #list of serial Numbers
	idlist = [] 
	year = [] #list of 2 numbers representing the year
	yr = [] #list of years of fabrication
	month = [] #list of 2 numbers representing the month (string)
	mth = [] #list of 2 numbers representing the month (int)
	MonthsABC = [] #list of months of fabrication
	z = 0
	y = 0

	for item in parent:
		idlist.append(item["id"])

	for item in parent:
		itemlist.append(item["serialNumber"])

	for i in range(len(itemlist)):
		year.append(itemlist[i][3:5])
		month.append(itemlist[i][5:7])

	for j in range(len(year)):
		yr.append(int(year[j])+1996)
		mth.append(int(month[j]))

	for k in mth:
		if k < 6:
			MonthsABC.append("Jan")
		elif k < 10:
			MonthsABC.append("Feb")
		elif k < 14:
			MonthsABC.append("Mar")
		elif k < 19:
			MonthsABC.append("Apr")
		elif k < 23:
			MonthsABC.append("May")
		elif k < 27:
			MonthsABC.append("Jun")
		elif k < 32:
			MonthsABC.append("Jul")
		elif k < 36:
			MonthsABC.append("Aug")
		elif k < 41:
			MonthsABC.append("Sep")
		elif k < 45:
			MonthsABC.append("Oct")
		elif k < 49:
			MonthsABC.append("Nov")
		elif k < 53:
			MonthsABC.append("Dec")
			
	"""print("Serial Numbers = ")
	print(itemlist)

	print("Year of Fabrication = ")
	print(yr)
	#print(mth)

	print("Month of Fabrication = ")
	print (MonthsABC)	"""

	StrYear = []
	for l in range(len(year)):
		StrYear.append(str(yr[l]))

	score = []
	for n in yr:
		if n > 2012:
			score.append(str(10))
		elif 2000 < n < 2013:
			score.append(str(5))
		elif n < 2000:
			score.append(str(1))

	for m in range(len(itemlist)):
		line ={"id":"","comment":"","score":0}

		line["id"] = utils.getDeviceByIDOnline(idlist[m])["hostname"]
		line["comment"] = StrYear[m] + ", " + MonthsABC[m] 	
		line ["score"] = score[m]	#+ "/10"														

		result["items"].append(line)
		y += int(score[m])
		z = round(y/11 , 3)
		result["totalScore"] = round(z,1)


		#("ID = " + item["id"] + ", Serial Number = " + itemlist[m] + ", Date of Fabrication = " + StrYear[m] + ", " + MonthsABC[m])
	return result


a = DOFchecker()
#print(json.dumps(a,indent=4,separators=(',', ': ')))

