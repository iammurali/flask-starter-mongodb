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


@app.route("/") #TESTING PART
def apiWelcome():
	currentTime = datetime.datetime.now()
	currentTime = currentTime.strftime("%H")
	currentDate = currentTime.strftime("%D")
	if(currentDate != prevDate):
		print(currentTime)
		print(request.remote_addr)
		prevDate = currentDate
		return "this is api for our aurdino"

                        #ON REQUEST

@app.route("/ON") #FOR MACHINE AIDA1 --ON REQUEST(FIRST MACHINE)
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

@app.route("/ONS") #FOR MACHINE AIDA2 --ON REQUEST(S-SECOND MACHINE)
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

@app.route("/ONT") #FOR MACHINE AIDA3 --ON REQUEST(T-THIRD MACHINE)
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

@app.route("/ONF") #FOR MACHINE AIDA4 --ON REQUEST(F-FOURTH MACHINE)
def machineOnf():
	currentTime = datetime.datetime.now()
	currentTime = currentTime.strftime("%H")
	print(currentTime)
	orMachine = machines.find_one({"machinename": "AIDA 4"})
	if orMachine["machineStaus"] != 1:
		machines.update_one({"machinename": "AIDA 4"}, {
							"$set": {"startTime": time.time(), "machineStaus": 1}}, upsert=True)
		return "AIDA 4 switched on"
	else:
		return "AIDA 4 already on"

@app.route("/ONFV") #FOR MACHINE 350SANES --ON REQUEST(FV - FIFTH MACHINE)
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

@app.route("/ONSIX") #FOR MACHINE DOBBY --ON REQUEST(SIX - SIXth MACHINE)
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

@app.route("/ONSV") #FOR MACHINE  250SANES --ON REQUEST(SV-SEVENth MACHINE)
def machineOnsv():
	currentTime = datetime.datetime.now()
	currentTime = currentTime.strftime("%H")
	print(currentTime)
	orMachine = machines.find_one({"machinename": "250SANES"})
	if orMachine["machineStaus"] != 1:
		machines.update_one({"machinename": "250SANES"}, {
							"$set": {"startTime": time.time(), "machineStaus": 1}}, upsert=True)
		return "250SANES switched on"
	else:
		return "250SANES already on"


                          #OFF REQUEST

@app.route("/OFF") #FOR MACHINE AIDA1 --OFF REQUEST(FIRST MACHINE)
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
		return "machine already off IN AIDA1"

@app.route("/OFFS") #FOR MACHINE AIDA2 --OFF REQUEST(S-SECOND MACHINE)
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

@app.route("/OFFT") #FOR MACHINE AIDA3 --OFF REQUEST(T-THIRD MACHINE)
def machineOfft():
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

@app.route("/OFFF") #FOR MACHINE AIDA4 --OFF REQUEST(F-FOURTH MACHINE)
def machineOfff():
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

@app.route("/OFFFV") #FOR MACHINE 350SANES --OFF REQUEST(FV-FIFTH MACHINE)
def machineOfffv():
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	orMachine = machines.find_one({"machinename": "350SANES"})
	if orMachine["machineStaus"] != 0:
		machines.update_one({"machinename": "350SANES"}, {
							"$set": {"stopTime": time.time(), "machineStaus": 0}}, upsert=True)
		cursorMachine = machines.find_one({"machinename": "350SANES"})
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
				machines.update_one({"machinename": "350SANES"},
								{"$set": {"elapsedTimeB": elapsedTime,"elapsedTime": elapsedTime}}, upsert=True)
			elif   24>currentTime >= 16:
				elapsedTime = cursorMachine["elapsedTimeA"] + \
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": "350SANES"},
								{"$set": {"elapsedTimeA": elapsedTime,"elapsedTime": elapsedTime}}, upsert=True)
			elif   8>currentTime >= 0:
				elapsedTime = cursorMachine["elapsedTimeC"] + \
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": "350SANES"},
								{"$set": {"elapsedTimeC": elapsedTime,"elapsedTime": elapsedTime}}, upsert=True)					
			return str(elapsedTime)
		else:
			return "there is an error IN 350SANES"
	else:
		return "machine already off IN 350SANES"

@app.route("/OFFSIX") #FOR MACHINE DOBBY --OFF REQUEST(SIX-SIXTH MACHINE)
def machineOffsix():
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	orMachine = machines.find_one({"machinename": "DOBBY"})
	if orMachine["machineStaus"] != 0:
		machines.update_one({"machinename": "DOBBY"}, {
							"$set": {"stopTime": time.time(), "machineStaus": 0}}, upsert=True)
		cursorMachine = machines.find_one({"machinename": "DOBBY"})
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
				machines.update_one({"machinename": "DOBBY"},
								{"$set": {"elapsedTimeB": elapsedTime,"elapsedTime": elapsedTime}}, upsert=True)
			elif   24>currentTime >= 16:
				elapsedTime = cursorMachine["elapsedTimeA"] + \
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": "DOBBY"},
								{"$set": {"elapsedTimeA": elapsedTime,"elapsedTime": elapsedTime}}, upsert=True)
			elif   8>currentTime >= 0:
				elapsedTime = cursorMachine["elapsedTimeC"] + \
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": "DOBBY"},
								{"$set": {"elapsedTimeC": elapsedTime,"elapsedTime": elapsedTime}}, upsert=True)					
			return str(elapsedTime)
		else:
			return "there is an error IN DOBBY"
	else:
		return "machine already off IN DOBBY"

@app.route("/OFFSV") #FOR MACHINE 250SANES --OFF REQUEST(SV-SEVENTH MACHINE)
def machineOffsv():
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	orMachine = machines.find_one({"machinename": "250SANES"})
	if orMachine["machineStaus"] != 0:
		machines.update_one({"machinename": "250SANES"}, {
							"$set": {"stopTime": time.time(), "machineStaus": 0}}, upsert=True)
		cursorMachine = machines.find_one({"machinename": "250SANES"})
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
				machines.update_one({"machinename": "250SANES"},
								{"$set": {"elapsedTimeB": elapsedTime,"elapsedTime": elapsedTime}}, upsert=True)
			elif   24>currentTime >= 16:
				elapsedTime = cursorMachine["elapsedTimeA"] + \
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": "250SANES"},
								{"$set": {"elapsedTimeA": elapsedTime,"elapsedTime": elapsedTime}}, upsert=True)
			elif   8>currentTime >= 0:
				elapsedTime = cursorMachine["elapsedTimeC"] + \
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": "250SANES"},
								{"$set": {"elapsedTimeC": elapsedTime,"elapsedTime": elapsedTime}}, upsert=True)					
			return str(elapsedTime)
		else:
			return "there is an error IN 250SANES"
	else:
		return "machine already off IN 250SANES"

                    #PROBLEM REQUEST


@app.route("/PROBLEM") ##FOR MACHINE AIDA1 --PROBLEM REQUEST(FIRST MACHINE)
def machineProblem():
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	machines.update_one({"machinename": "AIDA 1"},
						{"$set": {"problemstartTime": time.time(),"machineStaus":3}}, upsert=True)
	print("machine data recieved")
	return "machine problem"

@app.route("/PROBLEMS") ##FOR MACHINE AIDA2 --PROBLEM REQUEST(S-SECOND MACHINE)
def machineProblems():
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	machines.update_one({"machinename": "AIDA 2"},
						{"$set": {"problemstartTime": time.time(),"machineStaus":3}}, upsert=True)
	print(" AIDA 2 machine data recieved")
	return "AIDA 2 machine problem"

@app.route("/PROBLEMT") ##FOR MACHINE AIDA3 --PROBLEM REQUEST(T-THIRD MACHINE)
def machineProblemt():
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	machines.update_one({"machinename": "AIDA 3"},
						{"$set": {"problemstartTime": time.time(),"machineStaus":3}}, upsert=True)
	print(" AIDA 3 machine data recieved")
	return "AIDA 3 machine problem"

@app.route("/PROBLEMF") ##FOR MACHINE AIDA4 --PROBLEM REQUEST(F-FOURTH MACHINE)
def machineProblemf():
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	machines.update_one({"machinename": "AIDA 4"},
						{"$set": {"problemstartTime": time.time(),"machineStaus":3}}, upsert=True)
	print(" AIDA 4 machine data recieved")
	return "AIDA 4 machine problem"

@app.route("/PROBLEMFV") ##FOR MACHINE 350SANES --PROBLEM REQUEST(FV-FIFTH MACHINE)
def machineProblemfv():
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	machines.update_one({"machinename": "350SANES"},
						{"$set": {"problemstartTime": time.time(),"machineStaus":3}}, upsert=True)
	print(" 350SANES machine data recieved")
	return "350SANES machine problem"

@app.route("/PROBLEMSIX") ##FOR MACHINE DOBBY --PROBLEM REQUEST(SIX-SIXTH MACHINE)
def machineProblemsix():
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	machines.update_one({"machinename": "DOBBY"},
						{"$set": {"problemstartTime": time.time(),"machineStaus":3}}, upsert=True)
	print(" DOBBY machine data recieved")
	return "DOBBY machine problem"

@app.route("/PROBLEMSV") ##FOR MACHINE 250SANES --PROBLEM REQUEST(SV-SEVENTH MACHINE)
def machineProblemsv():
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	machines.update_one({"machinename": "250SANES"},
						{"$set": {"problemstartTime": time.time(),"machineStaus":3}}, upsert=True)
	print(" 250SANES machine data recieved")
	return "250SANES machine problem"

                        #PROBLEM SOLVED REQUEST


@app.route("/PROBLEMSOLVED") ##FOR MACHINE AIDA1 --PROBLEMSOLVED REQUEST(FIRST MACHINE)
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


@app.route("/PROBLEMSOLVEDS")##FOR MACHINE AIDA2 --PROBLEMSOLVED REQUEST(SECOND MACHINE)
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


                        #IDLE REQUEST

@app.route("/IDLE") ##FOR MACHINE AIDA1 --IDLE REQUEST(FIRST MACHINE)
def machineIdle():
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	machines.update_one({"machinename": "AIDA 1"}, {
						"$set": {"machineStaus":4, "idleStart": time.time()}}, upsert=True)
	print("machine data recieved IN AIDA1")
	return "Machine idle"

@app.route("/IDLES") ##FOR MACHINE AIDA2 --IDLE REQUEST(S-SECOND MACHINE)
def machineIdles():
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	machines.update_one({"machinename": "AIDA 2"}, {
						"$set": {"machineStaus":4, "idleStart": time.time()}}, upsert=True)
	print("machine data recieved IN AIDA2")
	return "Machine idle IN AIDA 2"

@app.route("/IDLET") ##FOR MACHINE AIDA3 --IDLE REQUEST(T-THIRD MACHINE)
def machineIdlet():
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	machines.update_one({"machinename": "AIDA 3"}, {
						"$set": {"machineStaus":4, "idleStart": time.time()}}, upsert=True)
	print("machine data recieved IN AIDA3")
	return "Machine idle"

@app.route("/IDLEF") ##FOR MACHINE AIDA4 --IDLE REQUEST(F-FOURTH MACHINE)
def machineIdlef():
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	machines.update_one({"machinename": "AIDA 4"}, {
						"$set": {"machineStaus":4, "idleStart": time.time()}}, upsert=True)
	print("machine data recieved IN AIDA4")
	return "Machine idle IN AIDA4"

@app.route("/IDLEFV") ##FOR MACHINE 350SANES--IDLE REQUEST(FV - FIFTH MACHINE)
def machineIdlefv():
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	machines.update_one({"machinename": "350SANES"}, {
						"$set": {"machineStaus":4, "idleStart": time.time()}}, upsert=True)
	print("machine data recieved IN 350SANES")
	return "Machine idle IN 350SANES"

@app.route("/IDLESIX") ##FOR MACHINE DOBBY --IDLE REQUEST(SIX-SIXTH MACHINE)
def machineIdlesix():
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	machines.update_one({"machinename": "DOBBY"}, {
						"$set": {"machineStaus":4, "idleStart": time.time()}}, upsert=True)
	print("machine data recieved IN DOBBY")
	return "Machine idle IN DOBBY"

@app.route("/IDLESV") ##FOR MACHINE 250SANES --IDLE REQUEST(SV-SEVENTH MACHINE)
def machineIdlesv():
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	machines.update_one({"machinename": "250SANES"}, {
						"$set": {"machineStaus":4, "idleStart": time.time()}}, upsert=True)
	print("machine data recieved IN 250SANES")
	return "Machine idle IN 250SANES"


                   ##IDLEOFF REQUEST

@app.route("/IDLEOFF") ##FOR MACHINE AIDA1 --IDLEOFF REQUEST(FIRST MACHINE)
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

@app.route("/IDLEOFFS")##FOR MACHINE AIDA2 --IDLEOFF REQUEST(FIRST MACHINE)
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

                       ##create machines from database##
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

                    ##get data from app##

@app.route("/mob/getmachines")
def getmachinesfn():
	print("machine data recieved")
	machine = machines.find()
	return dumps(machine)


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=8081)
# Careful with the debug mode..
