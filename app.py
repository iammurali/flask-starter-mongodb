# For flask implementation
from flask import Flask, render_template, request, redirect, url_for, jsonify
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

machines = db.machines  # collection for storing list of machines
machineTimings = db.machineTimings
app = Flask(__name__)

# modify=ObjectId()
#now = datetime.datetime.now(pytz.timezone(TIME_ZONE))
now=round(time.time(),0)
cdt =datetime.datetime
def redirect_url():
	return request.args.get('next') or \
		request.referrer or \
		url_for('index')


@app.route("/")
def apiWelcome():
	currentTime = datetime.datetime.now()
	currentTime = currentTime.strftime("%H")
	currentDate = currentTime.strftime("%D")
	if(currentDate != prevDate):
		print(currentTime)
		print(request.remote_addr)
		prevDate = currentDate
		return "this is api for our aurdino"


@app.route("/ON") #FOR MACHINE AIDA1 --ON REQUEST
def machineOn():
	currentTime = datetime.datetime.now()
	currentTime = currentTime.strftime("%H")
	print(currentTime)
	orMachine = machines.find_one({"machinename": "AIDA 1"})
	if orMachine["machineStaus"] != 1:
		machines.update_one({"machinename": "AIDA 1"}, {
							"$set": {"startTime": time.time(), "machineStaus": 1}}, upsert=True)
		return "switched on"
	else:
		return "already on"

@app.route("/ONS") #FOR MACHINE AIDA2 --ON REQUEST
def machineOns():
	currentTime = datetime.datetime.now()
	currentTime = currentTime.strftime("%H")
	print(currentTime)
	orMachine = machines.find_one({"machinename": "AIDA 2"})
	if orMachine["machineStaus"] != 1:
		machines.update_one({"machinename": "AIDA 2"}, {
							"$set": {"startTime": time.time(), "machineStaus": 1}}, upsert=True)
		return "AIDA 2 switched on"
	else:
		return "AIDA 2 already on"

@app.route("/ONT") #FOR MACHINE AIDA3 --ON REQUEST
def machineOnt():
	currentTime = datetime.datetime.now()
	currentTime = currentTime.strftime("%H")
	print(currentTime)
	orMachine = machines.find_one({"machinename": "AIDA 3"})
	if orMachine["machineStaus"] != 1:
		machines.update_one({"machinename": "AIDA 3"}, {
							"$set": {"startTime": time.time(), "machineStaus": 1}}, upsert=True)
		return "AIDA 3 switched on"
	else:
		return "AIDA 3 already on"

@app.route("/ONF") #FOR MACHINE AIDA4 --ON REQUEST
def machineOnf():
	currentTime = datetime.datetime.now()
	currentTime = currentTime.strftime("%H")
	print(currentTime)
	orMachine = machines.find_one({"machinename": "AIDA 4"})
	if orMachine["machineStaus"] != 1:
		machines.update_one({"machinename": "AIDA 3"}, {
							"$set": {"startTime": time.time(), "machineStaus": 1}}, upsert=True)
		return "AIDA 4 switched on"
	else:
		return "AIDA 4 already on"

@app.route("/ONFV") #FOR MACHINE 350SANES --ON REQUEST
def machineOnfv():
	currentTime = datetime.datetime.now()
	currentTime = currentTime.strftime("%H")
	print(currentTime)
	orMachine = machines.find_one({"machinename": "350SANES"})
	if orMachine["machineStaus"] != 1:
		machines.update_one({"machinename": "350SANES"}, {
							"$set": {"startTime": time.time(), "machineStaus": 1}}, upsert=True)
		return "350SANES switched on"
	else:
		return "350SANES already on"

@app.route("/ONSIX") #FOR MACHINE DOBBY --ON REQUEST
def machineOnsix():
	currentTime = datetime.datetime.now()
	currentTime = currentTime.strftime("%H")
	print(currentTime)
	orMachine = machines.find_one({"machinename": "DOBBY"})
	if orMachine["machineStaus"] != 1:
		machines.update_one({"machinename": "DOBBY"}, {
							"$set": {"startTime": time.time(), "machineStaus": 1}}, upsert=True)
		return "DOBBY switched on"
	else:
		return "DOBBY already on"




@app.route("/OFF")
def machineOff():
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	orMachine = machines.find_one({"machinename": "AIDA 1"})
	if orMachine["machineStaus"] != 0:
		machines.update_one({"machinename": "AIDA 1"}, {
							"$set": {"stopTime": time.time(), "machineStaus": 0}}, upsert=True)
		cursorMachine = machines.find_one({"machinename": "AIDA 1"})
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
				machines.update_one({"machinename": "AIDA 1"},
								{"$set": {"elapsedTimeB": elapsedTime,"elapsedTime": elapsedTime}}, upsert=True)
			elif   24>currentTime >= 16:
				elapsedTime = cursorMachine["elapsedTimeA"] + \
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": "AIDA 1"},
								{"$set": {"elapsedTimeA": elapsedTime,"elapsedTime": elapsedTime}}, upsert=True)
			elif   8>currentTime >= 0:
				elapsedTime = cursorMachine["elapsedTimeC"] + \
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": "AIDA 1"},
								{"$set": {"elapsedTimeC": elapsedTime,"elapsedTime": elapsedTime}}, upsert=True)					
			return str(elapsedTime)
		else:
			return "there is an error"
	else:
		return "machine already off"

@app.route("/OFFS")
def machineOffs():
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	orMachine = machines.find_one({"machinename": "AIDA 2"})
	if orMachine["machineStaus"] != 0:
		machines.update_one({"machinename": "AIDA 2"}, {
							"$set": {"stopTime": time.time(), "machineStaus": 0}}, upsert=True)
		cursorMachine = machines.find_one({"machinename": "AIDA 2"})
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
				machines.update_one({"machinename": "AIDA 2"},
								{"$set": {"elapsedTimeB": elapsedTime,"elapsedTime": elapsedTime}}, upsert=True)
			elif   24>currentTime >= 16:
				elapsedTime = cursorMachine["elapsedTimeA"] + \
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": "AIDA 2"},
								{"$set": {"elapsedTimeA": elapsedTime,"elapsedTime": elapsedTime}}, upsert=True)
			elif   8>currentTime >= 0:
				elapsedTime = cursorMachine["elapsedTimeC"] + \
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": "AIDA 2"},
								{"$set": {"elapsedTimeC": elapsedTime,"elapsedTime": elapsedTime}}, upsert=True)					
			return str(elapsedTime)
		else:
			return "there is an error IN AIDA2"
	else:
		return "machine already off IN AIDA2"

@app.route("/OFFT")
def machineOffs():
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	orMachine = machines.find_one({"machinename": "AIDA 3"})
	if orMachine["machineStaus"] != 0:
		machines.update_one({"machinename": "AIDA 3"}, {
							"$set": {"stopTime": time.time(), "machineStaus": 0}}, upsert=True)
		cursorMachine = machines.find_one({"machinename": "AIDA 3"})
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
				machines.update_one({"machinename": "AIDA 3"},
								{"$set": {"elapsedTimeB": elapsedTime,"elapsedTime": elapsedTime}}, upsert=True)
			elif   24>currentTime >= 16:
				elapsedTime = cursorMachine["elapsedTimeA"] + \
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": "AIDA 3"},
								{"$set": {"elapsedTimeA": elapsedTime,"elapsedTime": elapsedTime}}, upsert=True)
			elif   8>currentTime >= 0:
				elapsedTime = cursorMachine["elapsedTimeC"] + \
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": "AIDA 3"},
								{"$set": {"elapsedTimeC": elapsedTime,"elapsedTime": elapsedTime}}, upsert=True)					
			return str(elapsedTime)
		else:
			return "there is an error IN AIDA3"
	else:
		return "machine already off IN AIDA3"

@app.route("/OFFF")
def machineOffs():
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	orMachine = machines.find_one({"machinename": "AIDA 4"})
	if orMachine["machineStaus"] != 0:
		machines.update_one({"machinename": "AIDA 4"}, {
							"$set": {"stopTime": time.time(), "machineStaus": 0}}, upsert=True)
		cursorMachine = machines.find_one({"machinename": "AIDA 4"})
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
				machines.update_one({"machinename": "AIDA 4"},
								{"$set": {"elapsedTimeB": elapsedTime,"elapsedTime": elapsedTime}}, upsert=True)
			elif   24>currentTime >= 16:
				elapsedTime = cursorMachine["elapsedTimeA"] + \
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": "AIDA 4"},
								{"$set": {"elapsedTimeA": elapsedTime,"elapsedTime": elapsedTime}}, upsert=True)
			elif   8>currentTime >= 0:
				elapsedTime = cursorMachine["elapsedTimeC"] + \
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": "AIDA 4"},
								{"$set": {"elapsedTimeC": elapsedTime,"elapsedTime": elapsedTime}}, upsert=True)					
			return str(elapsedTime)
		else:
			return "there is an error IN AIDA4"
	else:
		return "machine already off IN AIDA4"

@app.route("/PROBLEM")
def machineProblem():
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	machines.update_one({"machinename": "AIDA 1"},
						{"$set": {"problemstartTime": time.time(),"machineStaus":3}}, upsert=True)
	print("machine data recieved")
	return "machine problem"

@app.route("/PROBLEMS")
def machineProblems():
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	machines.update_one({"machinename": "AIDA 2"},
						{"$set": {"problemstartTime": time.time(),"machineStaus":3}}, upsert=True)
	print(" AIDA 2 machine data recieved")
	return "AIDA 2 machine problem"


@app.route("/PROBLEMSOLVED")
def machineProblemSolved():
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	cursorMachine = machines.find_one({"machinename": "AIDA 1"})
	if cursorMachine["machineStaus"] != 2:
		machines.update_one({"machinename": "AIDA 1"}, {
                            "$set": {"problemstopTime": time.time(), "machineStaus": 2}}, upsert=True)
		cursorMachine = machines.find_one({"machinename": "AIDA 1"})
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
				machines.update_one({"machinename": "AIDA 1"},
								{"$set": {"problemtimeB": elapsedTime,"problemtime": elapsedTime}}, upsert=True)
			if   24>currentTime >= 16:
				elapsedTime = cursorMachine["problemtimeA"] + \
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": "AIDA 1"},
								{"$set": {"problemtimeA": elapsedTime,"problemtime": elapsedTime}}, upsert=True)
			if   8>currentTime >= 0:
				elapsedTime = cursorMachine["problemtimeC"] + \
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": "AIDA 1"},
								{"$set": {"problemtimeC": elapsedTime,"problemtime": elapsedTime}}, upsert=True)
			return str(elapsedTime)
		else:
			return "there is an error"
@app.route("/PROBLEMSOLVEDS")
def machineProblemSolveds():
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	cursorMachine = machines.find_one({"machinename": "AIDA 2"})
	if cursorMachine["machineStaus"] != 2:
		machines.update_one({"machinename": "AIDA 2"}, {
                            "$set": {"problemstopTime": time.time(), "machineStaus": 2}}, upsert=True)
		cursorMachine = machines.find_one({"machinename": "AIDA 2"})
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
				machines.update_one({"machinename": "AIDA 2"},
								{"$set": {"problemtimeB": elapsedTime,"problemtime": elapsedTime}}, upsert=True)
			if   24>currentTime >= 16:
				elapsedTime = cursorMachine["problemtimeA"] + \
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": "AIDA 2"},
								{"$set": {"problemtimeA": elapsedTime,"problemtime": elapsedTime}}, upsert=True)
			if   8>currentTime >= 0:
				elapsedTime = cursorMachine["problemtimeC"] + \
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": "AIDA 2"},
								{"$set": {"problemtimeC": elapsedTime,"problemtime": elapsedTime}}, upsert=True)
			return str(elapsedTime)
		else:
			return "there is an error IN AIDA 2"

@app.route("/IDLE")
def machineIdle():
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	machines.update_one({"machinename": "AIDA 1"}, {
						"$set": {"machineStaus":4, "idleStart": time.time()}}, upsert=True)
	print("machine data recieved")
	return "Machine idle"

@app.route("/IDLES")
def machineIdles():
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	machines.update_one({"machinename": "AIDA 2"}, {
						"$set": {"machineStaus":4, "idleStart": time.time()}}, upsert=True)
	print("machine data recieved IN AIDA2")
	return "Machine idle IN AIDA 2"


@app.route("/IDLEOFF")
def machineIdleoff():
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	machines.update_one({"machinename": "AIDA 1"}, {
						"$set": {"machineStaus":5, "idleStop":time.time()}}, upsert=True)
	cursorMachine = machines.find_one({"machinename": "AIDA 1"})
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
			machines.update_one({"machinename": "AIDA 1"},
							{"$set": {"idleTimeB": elapsedTime,"idleTime": elapsedTime}}, upsert=True)
		if   24>currentTime >= 16:
			elapsedTime = cursorMachine["idleTimeA"] + \
			time_difference_in_percent
			elapsedTime = round(elapsedTime,2)
			print(elapsedTime)
			machines.update_one({"machinename": "AIDA 1"},
							{"$set": {"idleTimeA": elapsedTime,"idleTime": elapsedTime}}, upsert=True)
		if   8>currentTime >= 0:
			elapsedTime = cursorMachine["idleTimeC"] + \
			time_difference_in_percent
			elapsedTime = round(elapsedTime,2)
			print(elapsedTime)
			machines.update_one({"machinename": "AIDA 1"},
							{"$set": {"idleTimeC": elapsedTime,"idleTime": elapsedTime}}, upsert=True)
		return "idle time" + str(elapsedTime)
	else:
		return "no data yet"

@app.route("/IDLEOFFS")
def machineIdleoffs():
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	machines.update_one({"machinename": "AIDA 2"}, {
						"$set": {"machineStaus":5, "idleStop":time.time()}}, upsert=True)
	cursorMachine = machines.find_one({"machinename": "AIDA 2"})
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
			machines.update_one({"machinename": "AIDA 2"},
							{"$set": {"idleTimeB": elapsedTime,"idleTime": elapsedTime}}, upsert=True)
		if   24>currentTime >= 16:
			elapsedTime = cursorMachine["idleTimeA"] + \
			time_difference_in_percent
			elapsedTime = round(elapsedTime,2)
			print(elapsedTime)
			machines.update_one({"machinename": "AIDA 2"},
							{"$set": {"idleTimeA": elapsedTime,"idleTime": elapsedTime}}, upsert=True)
		if   8>currentTime >= 0:
			elapsedTime = cursorMachine["idleTimeC"] + \
			time_difference_in_percent
			elapsedTime = round(elapsedTime,2)
			print(elapsedTime)
			machines.update_one({"machinename": "AIDA 2"},
							{"$set": {"idleTimeC": elapsedTime,"idleTime": elapsedTime}}, upsert=True)
		return "idle time" + str(elapsedTime)
	else:
		return "no data yet"


@app.route("/createmachine")
def createmachine():
	currentTime = datetime.datetime.now()
	currentTime = currentTime.strftime("%H")
	print(currentTime)
	print("machine data recieved")
	hello = machines.insert_one({"machinename": "AIDA 1", "machineStaus": 0,
								 "totalTimeOn": 0, "elapsedTime": 0,"idleTime": 0,"problemtime": 0, "elapsedTimeB": 0, "problemtimeB": 0, "idleTimeB": 0, "elapsedTimeA": 0, "problemtimeA": 0, "idleTimeA": 0, "elapsedTimeC": 0, "problemtimeC": 0, "idleTimeC": 0})
	print(hello.inserted_id)
	return "machine created"


@app.route("/mob/getmachines")
def getmachinesfn():
	print("machine data recieved")
	machine = machines.find()
	return dumps(machine)


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=8081)
# Careful with the debug mode..
