#!/usr/bin/python

# Requires tweepy,simplejson and oauth0
# further requires a config file (tweetrswara.conf) with the access token for the swara user

import os,sys,time
sys.path.append("/opt/swara/libs")
from database import *
from utilities import *
import ConfigParser
import oauth2 as oauth
import os,sys
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

config=ConfigParser.ConfigParser()
gmail_user = ""
gmail_pwd = ""



def mail(post,to):
	title=db.getTitleforPost(12345,post)[0][:120]
	title=title.replace("&#039;","'")
	subject="[Swara Training]" + title 
	content=str(db.getMessageforPost(12345,post)[0])
	content=content.replace("&#039;","'")
	authorname=str(db.getMessageforPost(12345,post)[0])
	if '_' in authorname:
		authorname=authorname.split('_')[0]
	text="Dear friends,\n \n"+content+"\n \nhttp://10.0.0.25/swara/index.php?id="+str(post)+"\n\nYou can also listen to this post after leaving a missed call on 080 4113 7280.\nYou can also record your own messages/songs the same way using your phone as this user has done\nRegards\nCGnet Swara moderators team" 	
	attach='/opt/swara/sounds/web/'+str(post)+'.mp3'
	#debugPrint("Tweeted post %s" %post)
	msg = MIMEMultipart()
	msg['From'] = "CGnet Swara"
	msg['To'] = to
	msg['Subject'] = subject
	msg.attach(MIMEText(text))
	if attach != "":
		part = MIMEBase('application', 'octet-stream')
		part.set_payload(open(attach, 'rb').read())
		Encoders.encode_base64(part)
		part.add_header('Content-Disposition',
			  'attachment; filename="%s"' % os.path.basename(attach))
		msg.attach(part)
	mailServer = smtplib.SMTP("smtp.gmail.com", 587)
	mailServer.ehlo()
	mailServer.starttls()
	mailServer.ehlo()
	mailServer.login(gmail_user, gmail_pwd)
	mailServer.sendmail(gmail_user, to, msg.as_string())
	# Should be mailServer.quit(), but that crashes...
	mailServer.close()

if __name__=="__main__":
	#Create Database object
	db=Database()
	postid=sys.argv[1] 
	print postid
	posts=db.getUnpushedPostsInChannel(12345,postid)
	for post in posts:
		mail(post,"")
	print "Final post = " + str(post)
