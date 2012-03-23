#!/usr/bin/python
import os,sys,time
sys.path.append("/opt/swara/libs")
from database import *
from utilities import *
import datetime, xmlrpclib
import ConfigParser
import ftplib
import PyRSS2Gen
config=ConfigParser.ConfigParser()

db = Database()	 

def getLastPushedPostID():
		post=os.popen("cat lastrssedpost").read().strip()
		return post

def rss_item(post):
		title = db.getTitleforPost('12345',post)
		content = db.getContentforPost('12345',post) + "\n http://nbsvr1/audio/"+str(post)+".mp3"
		#content = "<pre>[mp3-jplayer tracks='7355.mp3, url, FEED:http://10.16.16.14/swara/index.php?id=7355']"
		link = "http://nbsvr1/swara/index.php?"+str(post)
		time=db.getPostedTime('12345',post)
		item="<item><title>"+title+"</title><description>"+content+"</description><link>"+link+"</link></item>"
		return item
if __name__=="__main__":
		#Create Database object
		postid=getLastPushedPostID()
		posts=db.getUnpushedPostsInChannel(12345,postid)
		if len(posts) == 0:
				print "No unpushed posts"
				exit()
		os.system("cp /opt/swara/web/pyrss2gen.xml /opt/swara/web/swararss.xml")
		xml = open("/opt/swara/web/swararss.xml","a")
		for post in posts:
				try:
					xml.write("\n")
					xml.write(rss_item(post))
					xml.write("\n")
				except:
						print "Could not create RSS item %s" %post
						continue
		debugPrint("Final post = " + str(post))
		os.system("echo %s > lastrssedpost" %(str(post)))
		xml.write("</channel></rss>")
		xml.close()
		






