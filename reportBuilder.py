from statistics import mean
import mattstev
#Author: Nicholas Swiatecki <nicholas@swiatecki.com>, Juulia Santala
def build(scans):
	finalScore = extractFinalScore(scans)

	head = '<html><head><title>BPA Report</title></head>'
	style = (
			"<style>"
                        "body{background-color: #EEEEEE; text-align:center;}"
                        "div.h1 {width:100%; height:300px; background-color:#2B2B2B; position:absolute; left:0px; top:0px;}"
                        "h1{color:#28CDC1;text-transform: uppercase;font-family: Arial, Helvetica, sans-serif}"
                        "h2{text-transform: uppercase;font-family: Arial, Helvetica, sans-serif}"
                        "table{font-family: Arial, Helvetica, sans-serif; background-color:#ffffff; border:0px; border-spacing:0px; width:100%;}"
                        "th {text-align:left;background-color:#2B2B2B; border-bottom:2px solid #28CDC1; color:#e9e9e9;"
                        "font-size:14px; text-transform: uppercase; font-weight:normal; padding:5px;}"
                        "td {padding:7px;} td.item {width:30%;} td.comment {width:60%;} td.score {width:10%;}"
                        "tr:nth-of-type(even){background-color:  #e9e9e9}"
                        "div.main{text-align:left; width:80%; position:relative; top:350px; left:10%;}"
                        ".description{color:#26999E; font-style:italic; font-weight:bold; font-family:arial, Helvetica, sans-serif; font-size: 16px;"
                        "border-left:1px solid #26999E; padding:5px; width:70%; position:relative; left:30px;}"
                        ".total{font-family:arial, Helvetica, sans-serif;width:80%; height:200px;text-align:center;color:#26999E;"
                        "font-size: 15px; border-left:#A75700; background-color:#EEEEEE; position:relative; left:10%; top:20px;"
                        "border-radius: 25px 25px 0px 0px; padding-left:20px; padding-top:10px;}"
                        ".matt{display:block; width:auto; height:180px; float:right; margin:10px; margin-right:70px;}"
                        "h3{font-size: 60px;text-transform: uppercase;font-family: Arial, Helvetica, sans-serif}"
                        ".master{width:50%; float:left;}"
                        ".improve{float:left;}"
                        ".summary{border:2px solid #2B2B2B; padding:10px; text-align:center; border-radius: 25px;}"
                        ".summary table{width:90%; position:relative; left:5%; font-family:arial, Helvetica, sans-serif;}"
                        "a:link, a:visited, a:active {color: #26999E; text-decoration:underline;} a:hover {color: #26999E; text-decoration:none;}"
                        "</style>"
			)

	body = "<div class=\"h1\"><h1 id=\"top\">Best Practice Analyser v. 0.1</h1><div class=\"total\">" +\
               renderMatt(finalScore) + "<div class=\"master\"><h2>Master score:</h2> <h3>" + str(finalScore) + "</h3></div>" +\
               "</div></div><div class=\"main\"><div class=\"summary\"><h2>Summary</h2>" +\
               "<table><thead><tr><th>Title</th><th>Total Score</th><th>Description</th></tr>"

        #Creating the summary table
	for s in scans:
                body+= "<tr><td><b><a href=\"#" + s["name"] + "\">"+s["name"]+"</a></b></td><td>"+str(s["totalScore"])+\
                        "</td><td>"
                if s["totalScore"] <= 4:
                        body+="<span style=\"color:red\">Bad</span>"
                elif s["totalScore"] <= 7:
                        body+="<span style=\"color:black\">Ok</a>"
                elif s["totalScore"] > 7:
                        body+="<span style=\"color:green\">Good</a>"
                body+= "</td></tr>"

	body +="</table><br/><br/></div><br/><br/>"

	for s in scans:
		#Get header and write it
        
                body+= "<div><h2 id=\""+s["name"] + "\">"+s["name"]+", Score: "+str(s["totalScore"]) + "</h2>"

                if "description" in s:
                        body+="<p class=\"description\">" + s["description"] + "</p>"
                body+="</div> <table><thead><tr><th>Item</th><th>Comment</th><th>Sub-Score</th></tr></thead>"
                body+="<tbody>"

                for i in s["items"]:
                        body+="<tr><td class=\"item\">"+i["id"]+"</td><td class=\"comment\">"+i["comment"]+\
                               "</td><td class=\"score\">"+str(i["score"])+"</td></tr>"

                body+="</tbody></table><br/><br/><center><b><a href=\"#top\">Back to the top</a></b></center><br/><br/>"

		

##	body += mattstev.happy()
##	body += mattstev.meh()
##	body += mattstev.mad()

	end = "<br/><br/></div></body></html>"

	html = head + style + body + end
	
	return html

def extractFinalScore(scans):
	#List comprehension <3 
	l = [s["totalScore"] for s in scans]
	#return round(mean(l),1)
	return round(2)



def renderMatt(score):
	if score <= 4:
		return mattstev.mad()
	elif score > 4 and score <= 7:
		return mattstev.meh()
	elif score > 7:
		return mattstev.happy()


	
