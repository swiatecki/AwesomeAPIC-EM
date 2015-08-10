from statistics import mean
import mattstev
#Author: Nicholas Swiatecki <nicholas@swiatecki.com>
def build(scans):
	head = '<html><head><title>BPA Report</title></head>'
	style = (
			"<style>"
			"body{background-color: rgb(245, 245, 245);}"
			"h1{font-family: Arial, Helvetica, sans-serif}"
			"</style>"
			)

	body = "<body><h1>Best Practice Analyser v. 0.1</h1>"
	body += "<h2 style='color: orange;text-decoration:underline;'>Total Score "+str(extractFinalScore(scans))+"</h2>"

	for s in scans:
		#Get header and write it

		body+= "<div>\
		<div><h2>"+s["name"]+", Score: "+str(s["totalScore"])+"</h2></div>"+\
		"<table style='width:100%'><thead><tr><th>Item</th><th>Comment</th><th>Sub-Score</th></tr></thead>"

		body+="<tbody>"
		for i in s["items"]:
			body+="<tr><td>"+i["id"]+"</td><td>"+i["comment"]+"</td><td>"+str(i["score"])+"</td></tr>"


		body+="</tbody></table>"

		body+="</div>"

		

	body += mattstev.happy()
	body += mattstev.meh()
	body += mattstev.mad()

	end = "</body></html>"

	html = head + style + body + end
	
	return html

def extractFinalScore(scans):
	#List comprehension <3 
	l = [s["totalScore"] for s in scans]
	return round(mean(l),1)
	