# -*- coding: utf-8 -*-
#!/usr/bin/python
import sys,os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import time,random,hashlib
import urllib,urllib2
import json

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

Project_Name = None
Directory_Name = None
Configuration = None
Fir_Token = None
emailFromUser = None
emailPassword = None
emailToUser = None
Message_AppKey = None
Message_AppSecret = None
Message_Mobiles = None
Message_TemplateID = None

def readJson():
	with open('./config.json') as json_file:
		dict = json.load(json_file)
		global Project_Name 
		global Directory_Name 
		global Configuration 
		global emailFromUser 
		global emailPassword 
		global emailToUser 
		global Message_AppKey 
		global Message_AppSecret 
		global Message_Mobiles 
		global Message_TemplateID 
		global Fir_Token

		Project_Name = dict["BaseConfig"]["Project_Name"]
		Directory_Name = dict["BaseConfig"]["Directory_Name"]
		Configuration = dict["BaseConfig"]["Configuration"]
		emailFromUser = dict["BaseConfig"]["emailFromUser"]
		emailPassword = dict["BaseConfig"]["emailPassword"]
		emailToUser = dict["BaseConfig"]["emailToUser"]
		Message_AppKey = dict["MessageConfig"]["AppKey"]
		Message_AppSecret = dict["MessageConfig"]["AppSecret"]
		Message_Mobiles = dict["MessageConfig"]["Mobiles"]
		Message_TemplateID = dict["MessageConfig"]["TemplateID"]
		Fir_Token = dict["Fir_Token"]

def showParam():
	print "Project_Name----------"+Project_Name
	print "Directory_Name--------"+Directory_Name
	print "Configuration---------"+Configuration
	print "emailFromUser---------"+emailFromUser
	print "emailPassword---------"+emailPassword
	print "emailToUser-----------"+emailToUser
	print "Message_AppKey--------"+Message_AppKey
	print "Message_AppSecret-----"+Message_AppSecret
	print "Message_Mobiles-------%s"%Message_Mobiles
	print "Message_TemplateID----"+Message_TemplateID
	print "Fir_Token-------------"+Fir_Token

def sendEmail(text, changlog):
	if not os.path.exists("./build/%s-adhoc/%s.ipa"%(Project_Name,Project_Name)):
		print "没有找到ipa文件"
		return

	html = '<html><h2>地址：<a href="%s">屠龙宝刀，点击就送</a></h2><br><h3>更新内容：%s</h3></html>' % (text, changlog)
	msg = MIMEText(text,'html','utf-8')
	# msg = MIMEText('地址：%s'%text,'html','utf-8')
	msg['to'] = emailToUser
	msg['from'] = emailFromUser
	msg['subject'] = '新的测试包已经上传'
	try:
		server = smtplib.SMTP()
		server.connect("smtp.mxhichina.com")
		server.login(emailFromUser,emailPassword)
		server.sendmail(msg['from'], msg['to'],msg.as_string())
		server.quit()
		print '发送成功'
	except Exception, e:  
		print str(e)
	return

#网易云信
def sendMessage(changlog):
	url = 'https://api.netease.im/sms/sendtemplate.action'
	CurTime = int(time.time()*1000)
	Nonce = random.randint(0,CurTime)
	#sha1校验
	CheckSum = hashlib.sha1(Message_AppSecret+'%s%s'%(Nonce,CurTime)).hexdigest()
	headers = {
		'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
		'AppKey': Message_AppKey,
		'Nonce': str(Nonce),
		'CurTime': str(CurTime),
		'CheckSum': CheckSum
	}
	data = {
		'templateid':Message_TemplateID,
		'mobiles':json.dumps(Message_Mobiles),
		'params':json.dumps([Project_Name,changlog])
	}
	request = urllib2.Request(url,headers=headers, data=urllib.urlencode(data))
	print urllib2.urlopen(request).read()
	
def uploadToFir(changlog):
	httpAddress = None
	if os.path.exists("./build/%s-adhoc/%s.ipa"%(Project_Name,Project_Name)):
		ret = os.popen("fir publish ./build/%s-adhoc/%s.ipa -T %s --changelog=%s"%(Project_Name,Project_Name,Fir_Token,changlog))
		for info in ret.readlines():
			if "Published succeed" in info:
				# httpAddress = '<html><h2>地址：<a href="%s">屠龙宝刀，点击就送</a></h2><br><h3>更新内容：%s</h3></html>' % (info[info.find("http://"):], changlog)
				# httpAddress = info[info.find("Published succeed"):] + "\n更新内容：" + changlog
				httpAddress = info[info.find("http://"):]
				print httpAddress
				break
	else:
		print "没有找到ipa文件"
	return httpAddress
	
#clean工程   
def cleanPro():
	os.system('xcodebuild clean -project ./%s/%s.xcodeproj -configuration %s -alltargets' % (Directory_Name,Project_Name,Configuration))
	return

#pull工程
def gitPull():
	os.system("cd %s;git reset --hard;git pull"%Directory_Name)
	return
	
#build工程
def build():
	os.system("xcodebuild -project ./%s/%s.xcodeproj -scheme %s -configuration %s -archivePath ./build/%s-adhoc.xcarchive clean archive build" % (Directory_Name, Project_Name, Project_Name, Configuration, Project_Name))
	os.system("xcodebuild -exportArchive -archivePath ./build/%s-adhoc.xcarchive -exportOptionsPlist ./ADHOCExportOptionsPlist.plist -exportPath ./build/%s-adhoc" % (Project_Name, Project_Name))

print("-------Please define Build Configuration Mode:-----------\n1.Debug(Upload Fir)\n2.Release(Upload Fir)\n3.Release(Not Upload Fir)")
input = raw_input("Configuration:")

if input == "1":
	Configuration = "Debug"
elif input == "2":
	Configuration = "Release"
elif input == "3":
	configuration = "Release"
else:
	print("undefined key!!!!")
	sys.exit()

readJson()
showParam()
cleanPro()
gitPull()
build()
# if input != "3":
# 	print "-----------请输入版本log----------"
# 	changlog = raw_input("changlog:")
# 	httpAddress = uploadToFir(changlog)
# 	sendEmail(httpAddress, changlog)
# 	sendMessage(changlog)