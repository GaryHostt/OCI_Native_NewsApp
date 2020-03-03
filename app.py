import requests
import csv
import json
from csv import reader
import datetime
from datetime import datetime
import flask
import logging
from flask import Flask, jsonify
from flask import render_template
from flask import request
import fromFile
import os
import subprocess
from subprocess import call
import glob
import time

# one day separte different functions like fromFile & hello()
#handle api key in getNews() & getSources() with variable

app = Flask(__name__)
@app.route("/")

@app.route('/api/version', methods=['GET'])
def version():
	return jsonify(status='success', api_version='1.0')

@app.route('/api/sources/csv', methods=['GET'])
def getInfo():
	if request.method =='GET':
		writeSourceCSV()
		uploadSources()
		deleteSourceFiles()
		return jsonify(status='success')
#/api/xxx/csv
# these endpoints are meant to be called by chron to create csv, upload it, and delete it
#it should take care of everything
@app.route('/api/news/csv', methods=['GET'])
def getInfo2():
	if request.method =='GET':
		writeNewsCSV()
		uploadNews()
		deleteNewsFiles()
		return jsonify(status='success')

@app.route('/api/sources', methods=['GET'])
def getInfo3():
	if request.method =='GET':
		getSources()
		sources = getSources()
		return jsonify(sources)

@app.route('/api/news', methods=['GET'])
def getInfo4():
	if request.method =='GET':
		getNews()
		news = getNews()
		return jsonify(news)

def credentials(filename):
    """ Given a filename,
        return the contents of that file
    """
    try:
        with open(filename, 'r') as f:
            # It's assumed our file contains a single line,
            # with our API key
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)

def deleteSourceFiles():
	os.chdir("/Users/aamacdon/Desktop/n3ws/3flask")
	print(os.getcwd())
	print(os.listdir())
	cat1=(os.getcwd())
	cat2=os.listdir()
	SourceFileList=glob.glob('Source*.csv')
	print('here1')
	for filePath in SourceFileList:
		try:
			os.remove(filePath)
			print('here2')
		except:
			print("Error while deleting file : ", filePath)
			print('here')
	cat5=os.listdir()
	print('here3')

def deleteNewsFiles():
	os.chdir("/Users/aamacdon/Desktop/n3ws/3flask")
	print(os.getcwd())
	print(os.listdir())
	cat1=(os.getcwd())
	cat2=os.listdir()
	newsFileList=glob.glob('News*.csv')
	print('here1')
	for filePath in newsFileList:
		try:
			os.remove(filePath)
			print('here2')
		except:
			print("Error while deleting file : ", filePath)
			print('here')
	cat5=os.listdir()
	print('here3')

def getSources():
	filename = 'apikey'
	credentials(filename)
	api_key = credentials(filename)
	#print("Our API key is: %s" % (api_key))
	url = "https://newsapi.org/v2/sources?language=en"
	headers = {
	  'X-Api-Key': api_key,
	  'Content-Type': 'multipart/form-data; boundary=--------------------------593272731598089745485801'
	}
	r = requests.request("GET", url, headers=headers)
	#print(r)
	json_data = json.loads(r.text)
	response = json_data['sources']
	sources = []
	i = 0
	for source in response:
		i += 1
		sources.append(source)
	return sources
def writeSourceCSV():
	getSources()
	sources = getSources()
	print(sources)
	myData = sources
	i=0
	localtime = datetime.now()
	filename = 'Sourceslogs-'+str(localtime)+'.csv'
	with open(filename,'a', newline='') as csvfile:
		newslist = csv.writer(csvfile, delimiter=' ')
		newslist.writerow([sources[i]])
		for row in myData:
			newslist.writerow(myData)
			print(row)
	print('order66')
	logging.basicConfig(filename='error.log',level=logging.DEBUG)
	logging.debug('This message should go to the log file')
	print(localtime)
	hello()

def uploadSources():
	os.chdir("/Users/aamacdon/Desktop/n3ws/3flask")
	print(os.getcwd())
	#modifyPermissions = os.system("chmod a+x newsupload.sh")
	#for running shell scripts if getting denied
	lol2=(os.listdir())
	rc = subprocess.call("./sourceupload.sh", shell=True)
	lol=(os.getcwd())

def getNews():
	filename = 'apikey'
	credentials(filename)
	api_key = credentials(filename)
	print("Our API key is: %s" % (api_key))
	url = "https://newsapi.org/v2/top-headlines?language=en"
	headers = {
	  'X-Api-Key': api_key,
	  'Content-Type': 'multipart/form-data; boundary=--------------------------994416873992670733558445'
	}
	r = requests.request("GET", url, headers=headers)
	json_data = json.loads(r.text)
	response = json_data['articles']
	articles = []
	print('got news')
	i = 0
	for article in response:
		i += 1
		articles.append(article)
	return articles
def writeNewsCSV():
	getNews()
	articles = getNews()
	print(articles)
	myData = articles
	i=0
	localtime = datetime.now()
	filename = 'Newslogs-'+str(localtime)+'.csv'
	with open(filename,'a', newline='') as csvfile:
		newsCSV = csv.writer(csvfile, delimiter=' ')
		newsCSV.writerow([articles[i]])
		for row in myData:
			newsCSV.writerow(myData)
			print(row)
	logging.basicConfig(filename='error.log',level=logging.DEBUG)
	logging.debug('This message should go to the log file')
	#print(localtime)
	#hello()
		# hello for practicing with "from fromFile import hello"

def uploadNews():
	os.chdir("/Users/aamacdon/Desktop/n3ws/3flask")
	print(os.getcwd())
	lol2=(os.listdir())
	rc = subprocess.call("./newsupload.sh", shell=True)
	lol=(os.getcwd())

if __name__=='__main__':
	app.run(host='0.0.0.0', port=80, debug=True)    





