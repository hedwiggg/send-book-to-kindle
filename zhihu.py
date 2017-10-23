import urllib2
import os
import requests
import re
from selenium import webdriver
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')   
# def pinzhuang(num):
# 	if num<10:
# 		return "00"+str(num)
# 	elif num<=99:
# 		return "0"+str(num)
# 	else:
# 		return str(num)
host = "https://www.zhihu.com"
parentPath = "/media/doujinlong/my/Dunkirk/"
topic = "/topic"
dunkirk = "/20039857"
commonUrl = "/questions?page="
allQuesUrl = host+topic +dunkirk+commonUrl
headers = {'content-type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
count = 0.0
writeCount = 0.0
for i in range(1,16):
	url= host+allQuesUrl+str(i)
	res =requests.get(url,headers = headers)
	content = res.content
	matcho = re.findall("(question_link(.*?)([\u2E80-\u9FFF]*)</a>)",content)
	count += len(matcho)
print "all question size is "+str(count) 
for i in range(1,16):
	url= host+allQuesUrl+str(i)
	res =requests.get(url,headers = headers)
	content = res.content
	matcho = re.findall("(question_link(.*?)([\u2E80-\u9FFF]*)</a>)",content)
	print "start page " +str(i) +" ing..."
	print len(matcho)
	for myTuple in matcho:
		writeCount += 1.0
		per = writeCount/count
		per = round(per,2)
		print "has write "+ str(100*per) +"% ,please sleep..."
		Chrome_login=webdriver.Firefox()
		Chrome_login.set_page_load_timeout(20)
		try:
			descMatch =  re.findall(">(.*?)<",myTuple[0])
			urlMatch  = re.findall("=\"(.*?)\"",myTuple[0])
			detailUrl = host+ urlMatch[0]
			content = Chrome_login.get(detailUrl)
			needContent =  Chrome_login.page_source
			Chrome_login.quit()
			answer = re.findall("CopyrightRichText-richTex(.*?)([\u2E80-\u9FFF]*)</span>",needContent)
			os.mknod(parentPath+descMatch[0])
			fp = open(parentPath+descMatch[0],'w')
			for myTuple in answer:
				text = myTuple[0]
				answerText = text.replace("t\" itemprop=\"text\">","").replace("<p>","").replace("</p>","").replace("<br>","").replace("</br>","")
				fp.write("Answer: "+answerText)
				fp.write("\n")
				fp.write("\n")
			fp.close()
		except:
			Chrome_login.quit()
			continue
	print "end page " +str(i) +"ing..."