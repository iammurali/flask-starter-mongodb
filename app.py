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
import threading

# Configure the connection to the database
client = MongoClient('localhost', 27017)
db = client.arduinoDb  # Select the database
prevDate=0

machines = db.machines  # collection for storing list of machines
machineTimings = db.machineTimingspytho
app = Flask(__name__)
app.secret_key = "mys33cret"

# modify=ObjectId()
#now = datetime.datetime.now(pytz.timezone(TIME_ZONE))
now=round(time.time(),0)
cdt =datetime.datetime

nofmachines = db.machines.count()
print(nofmachines)
#machinesID = machines.find({},{"machinename":1})
machinesID = machines.distinct("machinename")
print(machinesID)
currentDate = datetime.date.today()
prevDate = currentDate
currentTimes = 1
prevTimes = 0
currentMinute = 0
prevMinute = 1
prevPercent1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
prevPercent2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
prevPercent3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		
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
	global currentDate
	global prevPercent1
	prevPercent1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	print(machineID)	
	currentTime = datetime.datetime.now()
	currentTime = currentTime.strftime("%H")
	print(currentTime)
	orMachine = machines.find_one({"machinename": machineID})
	#print(currentDate,prevDate)
	if orMachine["machineStaus"] != 1:
		machines.update_one({"machinename": machineID}, {
							"$set": {"startTime": time.time(), "machineStaus": 1}}, upsert=True)
		return "switched on"
	else:
		return "already on"

                         #OFF REQUEST

@app.route("/OFF/<machineID>")
def machineOff(machineID):
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	#print(currentDate,prevDate)
	cursorMachine = machines.find_one({"machinename": machineID})
	if cursorMachine["machineStaus"] != 0:
		machines.update_one({"machinename": machineID}, {
							"$set": {"stopTime": time.time(), "machineStaus": 0}}, upsert=True)
		'''cursorMachine = machines.find_one({"machinename": machineID})
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
								{"$set": {"elapsedTimeB": elapsedTime/2,"elapsedTime": elapsedTime}}, upsert=True)
			elif   24>currentTime >= 16:
				elapsedTime = cursorMachine["elapsedTimeA"] + \
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": machineID},
								{"$set": {"elapsedTimeA": elapsedTime/2,"elapsedTime": elapsedTime}}, upsert=True)
			elif   8>currentTime >= 0:
				elapsedTime = cursorMachine["elapsedTimeC"] + \
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": machineID},
								{"$set": {"elapsedTimeC": elapsedTime/2,"elapsedTime": elapsedTime}}, upsert=True)					
			return str(elapsedTime)
		else:
			return "there is an error" '''
	else:
		return "machine already off IN AIDA1"



                    #PROBLEM REQUEST


@app.route("/PROBLEM/<machineID>") 
def machineProblem(machineID):
	global prevPercent2
	prevPercent2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	orMachine = machines.find_one({"machinename": machineID})
	if orMachine["machineStaus"] != 3:
	    machines.update_one({"machinename": machineID},
						{"$set": {"problemstartTime": time.time(),"machineStaus":3}}, upsert=True)
	print("machine data recieved")
	return "machine problem"


                        #PROBLEM SOLVED REQUEST


@app.route("/PROBLEMSOLVED/<machineID>") 
def machineProblemSolved(machineID):
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	#print(currentDate,prevDate)
	cursorMachine = machines.find_one({"machinename": machineID})
	if cursorMachine["machineStaus"] != 2:
		machines.update_one({"machinename": machineID}, {
                            "$set": {"problemstopTime": time.time(), "machineStaus": 2}}, upsert=True)
		'''cursorMachine = machines.find_one({"machinename": machineID})
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
								{"$set": {"problemtimeB": elapsedTime/2,"problemtime": elapsedTime}}, upsert=True)
			if   24>currentTime >= 16:
				elapsedTime = cursorMachine["problemtimeA"] + \
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": machineID},
								{"$set": {"problemtimeA": elapsedTime/2,"problemtime": elapsedTime}}, upsert=True)
			if   8>currentTime >= 0:
				elapsedTime = cursorMachine["problemtimeC"] + \
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": machineID},
								{"$set": {"problemtimeC": elapsedTime/2,"problemtime": elapsedTime}}, upsert=True)
			return str(elapsedTime)'''
	else:
		return "there is an error"



                        #IDLE REQUEST

@app.route("/IDLE/<machineID>")
def machineIdle(machineID):
	global prevPercent3
	prevPercent3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	orMachine = machines.find_one({"machinename": machineID})
	#print(currentDate,prevDate)
	if orMachine["machineStaus"] != 4:
	    machines.update_one({"machinename": machineID}, {
						"$set": {"machineStaus":4, "idleStart": time.time()}}, upsert=True)
	print("machine data recieved IN AIDA1")
	return "Machine idle"




                   ##IDLEOFF REQUEST

@app.route("/IDLEOFF/<machineID>")
def machineIdleoff(machineID):
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	cursorMachine = machines.find_one({"machinename": machineID})
	if cursorMachine["machineStaus"] != 5:
		machines.update_one({"machinename": machineID}, {
						"$set": {"machineStaus":5, "idleStop":time.time()}}, upsert=True)
		'''cursorMachine = machines.find_one({"machinename": machineID})
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
				elapsedTime = cursorMachine["idleTimeB"] + 
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": machineID},
								{"$set": {"idleTimeB": elapsedTime/2,"idleTime": elapsedTime}}, upsert=True)
			if   24>currentTime >= 16:
				elapsedTime = cursorMachine["idleTimeA"] + 
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": machineID},
								{"$set": {"idleTimeA": elapsedTime/2,"idleTime": elapsedTime}}, upsert=True)
			if   8>currentTime >= 0:
				elapsedTime = cursorMachine["idleTimeC"] + 
				time_difference_in_percent
				elapsedTime = round(elapsedTime,2)
				print(elapsedTime)
				machines.update_one({"machinename": machineID},
								{"$set": {"idleTimeC": elapsedTime/2,"idleTime": elapsedTime}}, upsert=True)
			return "idle time" + str(elapsedTime)
		else:
			return "no data yet"
		'''


                       ##create machines from database##
@app.route("/createmachine/<machineID>")
def createmachine(machineID):
	global nofmachines
	global machinesID
	currentTime = datetime.datetime.now()
	currentTime = currentTime.strftime("%H")
	print(currentTime)
	print("machine created")
	hello = machines.insert_one({"machinename": machineID, "machineStaus": 0,
								 "totalTimeOn": 0, "elapsedTime": 0,"idleTime": 0,"problemtime": 0, "elapsedTimeB": 0, "problemtimeB": 0, "idleTimeB": 0, "elapsedTimeA": 0, "problemtimeA": 0, "idleTimeA": 0, "elapsedTimeC": 0, "problemtimeC": 0, "idleTimeC": 0})
	print(hello.inserted_id)
	time.sleep(5)
	nofmachines = nofmachines + 1
	machinesID.append(machineID)
	print(nofmachines)
	print(machinesID)
	return "machine created"

                    ##get data from app##

@app.route("/mob/getmachines")
def getmachinesfn():
	print("machine data recieved")
	machine = machines.find()
	return dumps(machine)


def checkDate():
	time.sleep(1)
	global prevPercent1, prevPercent2, prevPercent3
	while True:
		#print("hi")
		global currentMinute
		global prevMinute
		global currentTimes
		global prevTimes
		global prevDate

		currentDate = datetime.date.today()
		currentTimes = time.time()
		currentMinute = time.strftime("%S")
		currentTime = datetime.datetime.now()
		currentTime = int(currentTime.strftime("%H"))
		'''if(int(currentTimes) != int(prevTimes)):
			print(currentTimes, prevTimes)
			print("Current Date is :" , currentDate)
			print("Previous Date is :" ,prevDate)
			print(currentMinute)
			prevTimes = currentTimes'''
		if(currentDate != prevDate):
			if nofmachines > 0:
				for i in machinesID:
					print("am in")		
					machines.update_one({"machinename": i},
											{"$set": {"elapsedTimeB": 0,"elapsedTime": 0,"elapsedTimeC": 0,"elapsedTimeA": 0,}}, upsert=True)
					machines.update_one({"machinename": i},
											{"$set": {"idleTimeB": 0,"idleTime": 0,"idleTimeC": 0,"idleTimeA": 0,}}, upsert=True)
					machines.update_one({"machinename": i},
											{"$set": {"problemtimeB": 0,"problemtime": 0,"problemtimeC": 0,"problemtimeA": 0,}}, upsert=True)
			prevDate = currentDate

		if nofmachines > 0:
			#print("nofmachines : ", nofmachines)
			presentPercent1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
			presentPercent2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
			presentPercent3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
			y = 0
			
			for i in machinesID:
				y = y + 1
				cursorMachine = machines.find_one({"machinename": i})
				
				if cursorMachine["machineStaus"] == 1:
					runningTime = int(time.time() - cursorMachine["startTime"])
					time_difference_in_minutes = runningTime*1.0 / 60
					time_difference_in_minutes = round(time_difference_in_minutes,2)
					time_difference_in_percent1 = time_difference_in_minutes*100/450
					time_difference_in_percent1 = round(time_difference_in_percent1,2)
					presentPercent1[y] = time_difference_in_percent1
					if(currentMinute != prevMinute):
						print("time diff in minutes" + str(time_difference_in_minutes))
						print("time diff in percent" , time_difference_in_percent1)
						print(cursorMachine)
						print(cursorMachine["startTime"])
						print("runningTime ", runningTime)
						prevMinute = currentMinute
					if(presentPercent1[y] != prevPercent1[y]):
						if "elapsedTime" in cursorMachine:
							if   16>currentTime >= 8:
								elapsedTime = cursorMachine["elapsedTimeB"] - prevPercent1[y] +\
								time_difference_in_percent1
								elapsedTime = round(elapsedTime,2)
								print(elapsedTime)
								machines.update_one({"machinename": i},
												{"$set": {"elapsedTimeB": elapsedTime,"elapsedTime": elapsedTime}}, upsert=True)
							elif   24>currentTime >= 16:
								print("elapsedTimeA :", cursorMachine["elapsedTimeA"] )
								elapsedTime = cursorMachine["elapsedTimeA"]  - prevPercent1[y] + \
								time_difference_in_percent1
								elapsedTime = round(elapsedTime,2)
								print("elapsedtime:", elapsedTime)
								machines.update_one({"machinename": i},
												{"$set": {"elapsedTimeA": elapsedTime,"elapsedTime": elapsedTime}}, upsert=True)
							elif   8>currentTime >= 0:
								elapsedTime = cursorMachine["elapsedTimeC"]  - prevPercent1[y] + \
								time_difference_in_percent1
								elapsedTime = round(elapsedTime,2)
								print(elapsedTime)
								machines.update_one({"machinename": i},
												{"$set": {"elapsedTimeC": elapsedTime,"elapsedTime": elapsedTime}}, upsert=True)
						prevPercent1[y] = time_difference_in_percent1
				
				if cursorMachine["machineStaus"] == 3:
					runningTime = time.time() - cursorMachine["problemstartTime"]
					time_difference_in_minutes = runningTime / 60
					time_difference_in_minutes = round(time_difference_in_minutes,2)
					time_difference_in_percent2 = time_difference_in_minutes*100/450
					time_difference_in_percent2 = round(time_difference_in_percent2,2)
					print(time_difference_in_percent2)
					presentPercent2[y] = time_difference_in_percent2
					if(presentPercent2[y] != prevPercent2[y]):
						if "problemtime" in cursorMachine:
							if   16>currentTime >= 8:
								elapsedTime = cursorMachine["problemtimeB"] - prevPercent2[y] + \
								time_difference_in_percent2
								elapsedTime = round(elapsedTime,2)
								print(elapsedTime)
								machines.update_one({"machinename": i},
												{"$set": {"problemtimeB": elapsedTime,"problemtime": elapsedTime}}, upsert=True)
							if   24>currentTime >= 16:
								elapsedTime = cursorMachine["problemtimeA"] - prevPercent2[y] + \
								time_difference_in_percent2
								elapsedTime = round(elapsedTime,2)
								print(elapsedTime)
								machines.update_one({"machinename": i},
												{"$set": {"problemtimeA": elapsedTime,"problemtime": elapsedTime}}, upsert=True)
							if   8>currentTime >= 0:
								elapsedTime = cursorMachine["problemtimeC"] - prevPercent2[y] + \
								time_difference_in_percent2
								elapsedTime = round(elapsedTime,2)
								print(elapsedTime)
								machines.update_one({"machinename": i},
												{"$set": {"problemtimeC": elapsedTime,"problemtime": elapsedTime}}, upsert=True)
					prevPercent2[y] = time_difference_in_percent2

				if cursorMachine["machineStaus"] == 4:
					runningTime = time.time() - cursorMachine["idleStart"]
					time_difference_in_minutes = runningTime / 60
					time_difference_in_minutes = round(time_difference_in_minutes,2)
					time_difference_in_percent3 = time_difference_in_minutes*100/450
					time_difference_in_percent3 = round(time_difference_in_percent3,2)
					print(time_difference_in_percent3)
					presentPercent3[y] = time_difference_in_percent3
					if(presentPercent3[y] != prevPercent3[y]):
						if "idleTime" in cursorMachine:
							if   16>currentTime >= 8:
								elapsedTime = cursorMachine["idleTimeB"] - prevPercent3[y] + \
								time_difference_in_percent3
								elapsedTime = round(elapsedTime,2)
								print(elapsedTime)
								machines.update_one({"machinename": i},
												{"$set": {"idleTimeB": elapsedTime,"idleTime": elapsedTime}}, upsert=True)
							if   24>currentTime >= 16:
								elapsedTime = cursorMachine["idleTimeA"] - prevPercent3[y] + \
								time_difference_in_percent3
								elapsedTime = round(elapsedTime,2)
								print(elapsedTime)
								machines.update_one({"machinename": i},
												{"$set": {"idleTimeA": elapsedTime,"idleTime": elapsedTime}}, upsert=True)
							if   8>currentTime >= 0:
								elapsedTime = cursorMachine["idleTimeC"] - prevPercent3[y] + \
								time_difference_in_percent3
								elapsedTime = round(elapsedTime,2)
								print(elapsedTime)
								machines.update_one({"machinename": i},
												{"$set": {"idleTimeC": elapsedTime,"idleTime": elapsedTime}}, upsert=True)
					prevPercent3[y] = time_difference_in_percent3



threadOne = threading.Thread(target=checkDate)
threadOne.start()

app.run(host='0.0.0.0', port=8081)
	
# Careful with the debug mode..
