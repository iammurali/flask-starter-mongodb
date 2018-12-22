# For flask implementation
from flask import Flask,session ,render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient  # Database connector
from bson.objectid import ObjectId  # For ObjectId to work
from bson import Binary, Code
from bson.json_util import dumps
import datetime
from datetime import timedelta
import pytz
from constants import TIME_ZONE
import time

# Configure the connection to the database
client = MongoClient('localhost', 27017)
db = client.arduinoDb  # Select the database
#prevDate=0

machines = db.machines  # collection for storing list of machines
machineTimings = db.machineTimings
app = Flask(__name__)
app.secret_key = "mys33cret"

# modify=ObjectId()
#now = datetime.datetime.now(pytz.timezone(TIME_ZONE))
now=round(time.time(),0)
cdt =datetime.datetime

currentDate = datetime.date.today()
prevDate=datetime.date.fromordinal(datetime.date.today().toordinal()-1).strftime("%F")
print(currentDate)
print(prevDate)
'''if(currentDate != prevDate):
		prevDate = currentDate
		machines.update_one({"machinename": "AIDA 1"},
								{"$set": {"elapsedTimeB": 0,"elapsedTime": 0,"elapsedTimeC": 0,"elapsedTimeA": 0,}}, upsert=True)
		machines.update_one({"machinename": "AIDA 1"},
								{"$set": {"idleTimeB": 0,"idleTime": 0,"idleTimeC": 0,"idleTimeA": 0,}}, upsert=True)
		machines.update_one({"machinename": "AIDA 1"},
								{"$set": {"problemTimeB": 0,"problemTime": 0,"problemTimeC": 0,"problemTimeA": 0,}}, upsert=True)'''



def redirect_url():
	return request.args.get('next') or \
		request.referrer or \
		url_for('index')


@app.route("/") #TESTING PART
def apiWelcome():
	global prevDate
	currentTime = datetime.datetime.now()
	currentTime = currentTime.strftime("%H")
	print(request.remote_addr)
	return "this is api for our aurdino"
	
                        #ON REQUEST

@app.route("/ON/<machineID>") 
def machineOn(machineID):
	print(machineID)
	temptoday = datetime.date.today()
	today = temptoday.strftime('%m/%d/%Y')
	if 'existingDate' not in session:
		print("from session loop",currentDate)
		session['existingDate']= today	
	currentTime = datetime.datetime.now()
	currentTime = currentTime.strftime("%H")
	print(currentTime)
	currentDate = today
	prevDate=session['existingDate']
	orMachine = machines.find_one({"machinename": machineID})
	print(currentDate,prevDate)
	if(currentDate != prevDate):
		session['existingDate']= currentDate
		machines.update_one({"machinename": machineID},
								{"$set": {"startTime": 0,"elapsedTimeB": 0,"elapsedTime": 0,"elapsedTimeC": 0,"elapsedTimeA": 0}}, upsert=True)
	if orMachine["machineStaus"] != 1:
		machines.update_one({"machinename": machineID}, {
							"$set": {"startTime": time.time(), "machineStaus": 1}}, upsert=True)
		return "switched on"
	else:
		return "already on"

                         #OFF REQUEST

@app.route("/OFF/<machineID>")
def machineOff(machineID):
	temptoday = datetime.date.today()
	today = temptoday.strftime('%m/%d/%Y')
	if 'existingDate' not in session:
		print("from session loop",currentDate)
		session['existingDate']= today
	currentDate = today
	prevDate=session['existingDate']
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	print(currentDate,prevDate)
	cursorMachine = machines.find_one({"machinename": machineID})
	if(currentDate != prevDate):
		session['existingDate']= currentDate
		machines.update_one({"machinename": machineID},
								{"$set": {"elapsedTimeB": 0,"elapsedTime": 0,"elapsedTimeC": 0,"elapsedTimeA": 0,"stopTime": 0}}, upsert=True)
	if cursorMachine["machineStaus"] != 0:
		machines.update_one({"machinename": machineID}, {
							"$set": {"stopTime": time.time(), "machineStaus": 0}}, upsert=True)
		cursorMachine = machines.find_one({"machinename": machineID})
		startTime = cursorMachine["startTime"]
		print(startTime)
		stopTime = cursorMachine["stopTime"]
		time_difference = stopTime - startTime
		print("hello" + str(time_difference))
		time_difference_in_minutes = time_difference / 60
		time_difference_in_minutes = round(time_difference_in_minutes,2)
		time_difference_in_percent = time_difference_in_minutes*100/450
		time_difference_in_percent = round(time_difference_in_percent,2)
		print(time_difference_in_percent)
		print("time diff in minutes" + str(time_difference_in_minutes))
		if "elapsedTime" in cursorMachine:
			if   16>currentTime >= 8:
				elapsedTime = cursorMachine["elapsedTimeB"] + \
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": machineID},
								{"$set": {"elapsedTimeB": elapsedTime,"elapsedTime": elapsedTime}}, upsert=True)
			elif   24>currentTime >= 16:
				elapsedTime = cursorMachine["elapsedTimeA"] + \
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": machineID},
								{"$set": {"elapsedTimeA": elapsedTime,"elapsedTime": elapsedTime}}, upsert=True)
			elif   8>currentTime >= 0:
				elapsedTime = cursorMachine["elapsedTimeC"] + \
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": machineID},
								{"$set": {"elapsedTimeC": elapsedTime,"elapsedTime": elapsedTime}}, upsert=True)					
			return str(elapsedTime)
		else:
			return "there is an error"
	else:
		return "machine already off IN AIDA1"



                    #PROBLEM REQUEST


@app.route("/PROBLEM/<machineID>") 
def machineProblem(machineID):
	temptoday = datetime.date.today()
	today = temptoday.strftime('%m/%d/%Y')
	currentDate = today
	if 'existingDate' not in session:
		print("from session loop",currentDate)
		session['existingDate']= today	
	prevDate=session['existingDate']
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	orMachine = machines.find_one({"machinename": machineID})
	if(currentDate != prevDate):
		session['existingDate']= currentDate
		machines.update_one({"machinename": machineID},
								{"$set": {"problemtimeB":0,"problemtime": 0,"problemtimeA":0,"problemtimeC":0,"problemstartTime": 0}}, upsert=True)
	if orMachine["machineStaus"] != 3:
	    machines.update_one({"machinename": machineID},
						{"$set": {"problemstartTime": time.time(),"machineStaus":3}}, upsert=True)
	print("machine data recieved")
	return "machine problem"


                        #PROBLEM SOLVED REQUEST


@app.route("/PROBLEMSOLVED/<machineID>") 
def machineProblemSolved(machineID):
	temptoday = datetime.date.today()
	today = temptoday.strftime('%m/%d/%Y')
	if 'existingDate' not in session:
		print("from session loop",currentDate)
		session['existingDate']= today
	currentDate = today
	prevDate=session['existingDate']
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	print(currentDate,prevDate)
	cursorMachine = machines.find_one({"machinename": machineID})
	if(currentDate != prevDate):
		session['existingDate']= currentDate
		machines.update_one({"machinename": machineID},
								{"$set": {"problemstopTime":0,"problemtimeB": 0,"problemtime": 0,"problemtimeA": 0,"problemtimeC": 0}}, upsert=True)
	if cursorMachine["machineStaus"] != 2:
		machines.update_one({"machinename": machineID}, {
                            "$set": {"problemstopTime": time.time(), "machineStaus": 2}}, upsert=True)
		cursorMachine = machines.find_one({"machinename": machineID})
		startTime = cursorMachine["problemstartTime"]
		print(startTime)
		stopTime = cursorMachine["problemstopTime"]
		time_difference = stopTime - startTime
		print("hello" + str(time_difference))
		time_difference_in_minutes = time_difference / 60
		print("time diff in minutes" + str(time_difference_in_minutes))
		time_difference_in_minutes = round(time_difference_in_minutes,2)
		time_difference_in_percent = time_difference_in_minutes*100/450
		time_difference_in_percent = round(time_difference_in_percent,2)
		print(time_difference_in_percent)
		if "problemtime" in cursorMachine:
			if   16>currentTime >= 8:
				elapsedTime = cursorMachine["problemtimeB"] + \
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": machineID},
								{"$set": {"problemtimeB": elapsedTime,"problemtime": elapsedTime}}, upsert=True)
			if   24>currentTime >= 16:
				elapsedTime = cursorMachine["problemtimeA"] + \
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": machineID},
								{"$set": {"problemtimeA": elapsedTime,"problemtime": elapsedTime}}, upsert=True)
			if   8>currentTime >= 0:
				elapsedTime = cursorMachine["problemtimeC"] + \
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": machineID},
								{"$set": {"problemtimeC": elapsedTime,"problemtime": elapsedTime}}, upsert=True)
			return str(elapsedTime)
		else:
			return "there is an error"





                        #IDLE REQUEST

@app.route("/IDLE/<machineID>")
def machineIdle(machineID):
	temptoday = datetime.date.today()
	today = temptoday.strftime('%m/%d/%Y')
	if 'existingDate' not in session:
		print("from session loop",currentDate)
		session['existingDate']= today	
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	currentDate = today
	prevDate=session['existingDate']
	orMachine = machines.find_one({"machinename": machineID})
	print(currentDate,prevDate)
	if(currentDate != prevDate):
		session['existingDate']= currentDate
		machines.update_one({"machinename": machineID}, {
						"$set": {"idleStart": 0,"idleStop":0,"idleTimeB": 0,"idleTimeA": 0,"idleTimeC": 0}}, upsert=True)
	if orMachine["machineStaus"] != 4:
	    machines.update_one({"machinename": machineID}, {
						"$set": {"machineStaus":4, "idleStart": time.time()}}, upsert=True)
	print("machine data recieved IN AIDA1")
	return "Machine idle"




                   ##IDLEOFF REQUEST

@app.route("/IDLEOFF/<machineID>")
def machineIdleoff(machineID):
	temptoday = datetime.date.today()
	today = temptoday.strftime('%m/%d/%Y')
	if 'existingDate' not in session:
		print("from session loop",currentDate)
		session['existingDate']= today	
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	currentDate = today
	prevDate=session['existingDate']
	cursorMachine = machines.find_one({"machinename": machineID})
	if(currentDate != prevDate):
		session['existingDate']= currentDate
		machines.update_one({"machinename": machineID}, {
						"$set": {"idleStop": 0,"idleTimeB": 0,"idleTimeA": 0,"idleTimeC": 0,"idleStart":0}}, upsert=True)
	if cursorMachine["machineStaus"] != 5:
		machines.update_one({"machinename": machineID}, {
						"$set": {"machineStaus":5, "idleStop":time.time()}}, upsert=True)
	cursorMachine = machines.find_one({"machinename": machineID})
	startTime = cursorMachine["idleStart"]
	print(startTime)
	stopTime = cursorMachine["idleStop"]
	time_difference = stopTime - startTime
	time_difference_in_minutes = time_difference / 60
	print(time_difference_in_minutes)
	time_difference_in_minutes = round(time_difference_in_minutes,2)
	time_difference_in_percent = time_difference_in_minutes*100/450
	time_difference_in_percent = round(time_difference_in_percent,2)
	print(time_difference_in_percent)
	if "idleTime" in cursorMachine:
		if   16>currentTime >= 8:
			elapsedTime = cursorMachine["idleTimeB"] + \
			time_difference_in_percent
			elapsedTime = round(elapsedTime,2)
			print(elapsedTime)
			machines.update_one({"machinename": machineID},
							{"$set": {"idleTimeB": elapsedTime,"idleTime": elapsedTime}}, upsert=True)
		if   24>currentTime >= 16:
			elapsedTime = cursorMachine["idleTimeA"] + \
			time_difference_in_percent
			elapsedTime = round(elapsedTime,2)
			print(elapsedTime)
			machines.update_one({"machinename": machineID},
							{"$set": {"idleTimeA": elapsedTime,"idleTime": elapsedTime}}, upsert=True)
		if   8>currentTime >= 0:
			elapsedTime = cursorMachine["idleTimeC"] + \
			time_difference_in_percent
			elapsedTime = round(elapsedTime,2)
			print(elapsedTime)
			machines.update_one({"machinename": machineID},
							{"$set": {"idleTimeC": elapsedTime,"idleTime": elapsedTime}}, upsert=True)
		return "idle time" + str(elapsedTime)
	else:
		return "no data yet"


                       ##create machines from database##
@app.route("/createmachine/<machineID>")
def createmachine(machineID):
	currentTime = datetime.datetime.now()
	currentTime = currentTime.strftime("%H")
	print(currentTime)
	print("machine data recieved")
	hello = machines.insert_one({"machinename": machineID, "machineStaus": 0,
								 "totalTimeOn": 0, "elapsedTime": 0,"idleTime": 0,"problemtime": 0, "elapsedTimeB": 0, "problemtimeB": 0, "idleTimeB": 0, "elapsedTimeA": 0, "problemtimeA": 0, "idleTimeA": 0, "elapsedTimeC": 0, "problemtimeC": 0, "idleTimeC": 0})
	print(hello.inserted_id)
	return "machine created"

                    ##get data from app##

@app.route("/mob/getmachines")
def getmachinesfn():
	print("machine data recieved")
	machine = machines.find()
	return dumps(machine)


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=8081)
# Careful with the debug mode..
