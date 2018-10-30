from flask import Flask, render_template,request,redirect,url_for, jsonify # For flask implementation
from pymongo import MongoClient # Database connector
from bson.objectid import ObjectId # For ObjectId to work
from bson import Binary, Code
from bson.json_util import dumps
import datetime
from datetime import timedelta
import pytz
from constants import TIME_ZONE

client = MongoClient('localhost', 27017)    #Configure the connection to the database
db = client.arduinoDb    #Select the database

machines = db.machines #collection for storing list of machines
machineTimings = db.machineTimings
app = Flask(__name__)

#modify=ObjectId()
now = datetime.datetime.now(pytz.timezone(TIME_ZONE))

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

@app.route("/")
def apiWelcome():
	print(request.remote_addr)
	return "this is api for our aurdino"

@app.route("/ON")
def machineOn():
	machines.update_one({"machinename":"arduino123"}, {"$set": {"startTime":now, "machineStaus": 1}}, upsert=True)
	return "switched on"

@app.route("/OFF")
def machineOff():
	cursorMachine = machines.find_one({"machinename":"arduino123"})	
	if cursorMachine["machineStaus"] != 0:
		machines.update_one({"machinename":"arduino123"}, {"$set": {"stopTime":now,"machineStatus":0}}, upsert=True)
		startTime = cursorMachine["startTime"]
		print(startTime)
		stopTime = cursorMachine["stopTime"]
		time_difference = stopTime - startTime
		time_difference_in_minutes = time_difference / timedelta(minutes=1)
		print(time_difference_in_minutes)
		if "elapsedTime" in cursorMachine:
			elapsedTime = cursorMachine["elapsedTime"] + time_difference_in_minutes
			print(elapsedTime)
			machines.update_one({"machinename":"arduino123"},
			 {"$set": {"elapsedTime":elapsedTime}}, upsert=True)
		return str(time_difference_in_minutes)	

@app.route("/MACHINEPROBLEM")
def machineProblem():
	machines.update_one({"machinename":"arduino123"},
	 {"$set": {"machineStatus":3}}, upsert=True)
	print("machine data recieved")
	return "hello"

@app.route("/MACHINEPROBLEMSOLVED")
def machineProblemSolved():
	cursorMachine = machines.find_one({"machinename":"arduino123"})
	if cursorMachine["machineStatus"] == 4 or cursorMachine["machineStatus"] == 1:		
		machines.update_one({"machinename":"arduino123"}, 
		{"$set": {"machineStatus":3}}, upsert=True)
		print("machine data recieved")
		return "Problem"


@app.route("/IDLE")
def machineIdle():
	machines.update_one({"machinename":"arduino123"}, {"$set": {"machineStatus":4}}, upsert=True)
	print("machine data recieved")
	return "Machine idle"

@app.route("/IDLEOFF")
def machineIdleoff():
	machines.update_one({"machinename":"arduino123"}, {"$set": {"machineStatus":4}}, upsert=True)
	print("machine data recieved")
	return "Machine idle"


@app.route("/createmachine")
def createmachine():
	print("machine data recieved")
	hello = machines.insert_one({"machinename": "arduino124", "machineStaus": 0, "totalTimeOn": 0,"elapsedTime": 0 })
	print(hello.inserted_id)
	return "hello"

@app.route("/mob/getmachines")
def getmachinesfn():
	print("machine data recieved")
	machine = machines.find()	
	return dumps(machine)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8081)
# Careful with the debug mode..


