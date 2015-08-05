def build(scans):
	head = '<html><head><title>BPA Report</title></head>'
	style = (
			"<style>"
			"body{background-color: rgb(245, 245, 245);}"
			"h1{font-family: Arial, Helvetica, sans-serif}"
			"</style>"
			)

	body = "<body><h1>Best Practice Analyser v. 0.1</h1>"

	for s in scans:
		#Get header and write it

		body+= "<div>\
		<div><h2>"+s["name"]+", Score: "+str(s["totalScore"])+"</h2></div>"+\
		"<table style='width:100%'><thead><tr><th>Name</th><th>Comment</th><th>Sub-Score</th></tr></thead>"

		body+="<tbody>"
		for i in s["items"]:
			body+="<tr><td>"+i["id"]+"</td><td>"+i["comment"]+"</td><td>"+str(i["score"])+"</td></tr>"


		body+="</tbody></table>"

		body+="</div>"



	end = "</body></html>"

	html = head + style + body + end
	return html