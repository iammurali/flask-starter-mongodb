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

currentDate = datetime.date.today()
prevDate = currentDate
currentTimes = 1
prevTimes = 0
currentMinute = 0
prevMinute = 1
prevPercent1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
prevPercent2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
prevPercent3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
presentPercent1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
presentPercent2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
presentPercent3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
serverStart = 1
sessionRunTime = 0
goin = 1

app = Flask(__name__)


machines = db.list_collection_names()
nofmachines = len(machines)
print(nofmachines)


machinesID = machines
print(machinesID)

@app.route("/") #TESTING PART
def apiWelcome():
	return "this is api for our arduino"

@app.route("/ON/<machineID>") 
def machineOn(machineID):
	today = datetime.date.today()
	machines = db[machineID]
	currentDoc = machines.find_one({"date":today.strftime("%d/%m/%Y")})
	if currentDoc["machineStaus"] != 1:
		machines.update_one({"date":today.strftime("%d/%m/%Y")},{ "$set": {"startTime": time.time(), "machineStaus": 1}}, upsert=True)
		return("switched on")
	else:
		return("already on")

@app.route("/OFF/<machineID>") 
def machineOff(machineID):
	today = datetime.date.today()
	machines = db[machineID]
	currentDoc = machines.find_one({"date":today.strftime("%d/%m/%Y")})
	if currentDoc["machineStaus"] != 0:
		machines.update_one({"date":today.strftime("%d/%m/%Y")},{ "$set": {"stopTime": time.time(), "machineStaus": 0}}, upsert=True)
		return("switched off")
	else:
		return("already off")


@app.route("/PROBLEM/<machineID>") 
def machineProblem(machineID):
	today = datetime.date.today()
	machines = db[machineID]
	currentDoc = machines.find_one({"date":today.strftime("%d/%m/%Y")})
	if currentDoc["machineStaus"] != 3:
		machines.update_one({"date":today.strftime("%d/%m/%Y")},{ "$set": {"problemstartTime": time.time(), "machineStaus": 3}}, upsert=True)
		return("problem")
	else:
		return("already problem")


@app.route("/IDLE/<machineID>") 
def machineIdle(machineID):
	today = datetime.date.today()
	machines = db[machineID]
	currentDoc = machines.find_one({"date":today.strftime("%d/%m/%Y")})
	if currentDoc["machineStaus"] != 4:
		machines.update_one({"date":today.strftime("%d/%m/%Y")},{ "$set": {"problemstartTime": time.time(), "machineStaus": 4}}, upsert=True)
		return("Idle")
	else:
		return("already idle")

					   ##create machines from database##
@app.route("/createmachine/<machineID>")
def createmachine(machineID):
	if machineID not in db.list_collection_names():
		machines = db[machineID]
		today = datetime.date.today()
		machine = machines.insert_one({"_id":today.strftime("%d/%m/%Y") ,"machinename": machineID, "date":today.strftime("%d/%m/%Y"), "machineStaus": 0,
								 "totalTimeOn": 0, "elapsedTime": 0,"idleTime": 0,"problemtime": 0, "offtime": 0, "elapsedTimeB": 0, "problemtimeB": 0, "idleTimeB": 0, "offtimeB": 0, "elapsedTimeA": 0, "problemtimeA": 0, "idleTimeA": 0, "offtimeA": 0, "elapsedTimeC": 0, "problemtimeC": 0, "idleTimeC": 0, "offtimeC":0})
		return "machine created"
	else:
		return "machine already available"

@app.route("/mob/getmachines")
def getmachinesfn():
	data = []
	print("machine data recieved")
	for x in machines:
		machineData = db[x]
		data.append(machineData.find_one())
	return dumps(data)

def checkDate():
	global serverStart
	#time.sleep(1)
	global prevPercent1, prevPercent2, prevPercent3
	global presentPercent1, presentPercent2, presentPercent3
	sessionStartTime = time.time()
	shiftChangeA = 1
	shiftChangeB = 1
	shiftChangeC = 1
	while True:

		
		
		if goin == 1:
			#print("hi")
			global currentMinute
			global prevMinute
			global currentTimes
			global prevTimes
			global prevDate
			sessionRunTime = int(time.time() - sessionStartTime)
			sessionRunMins = sessionRunTime / 60
			sessionRunPercent = round(sessionRunMins * 100 / 450,2)

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
						machines = db[i]
						print("am in")
						today = datetime.date.today()
						machine = machines.insert_one({"_id":today.strftime("%d/%m/%Y") ,"machinename": i, "date":today.strftime("%d/%m/%Y"), "machineStaus": 0,
								 "totalTimeOn": 0, "elapsedTime": 0,"idleTime": 0,"problemtime": 0, "offtime": 0, "elapsedTimeB": 0, "problemtimeB": 0, "idleTimeB": 0, "offtimeB": 0, "elapsedTimeA": 0, "problemtimeA": 0, "idleTimeA": 0, "offtimeA": 0, "elapsedTimeC": 0, "problemtimeC": 0, "idleTimeC": 0, "offtimeC":0})
		
				sessionStartTime = time.time()
				prevDate = currentDate

			if nofmachines > 0:
				#print("nofmachines : ", nofmachines)
				presentPercent1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
				presentPercent2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
				presentPercent3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
				y = 0
				
				for i in machinesID:
					y = y + 1
					today = datetime.date.today()
					machines = db[i]
					#print(machines)
					cursorMachine = machines.find_one({"_id":today.strftime("%d/%m/%Y")})
					#print("current cursor machine is :", cursorMachine)
					if   16>currentTime >= 8:
					 	shiftChangeA = 1
					 	shiftChangeC = 1
					 	if shiftChangeB == 1:
					 		sessionStartTime = time.time()
					 		shiftChangeB = 0
					 	offtimeB = round(sessionRunPercent - (cursorMachine["elapsedTimeB"] + cursorMachine["idleTimeB"] + cursorMachine["problemtimeB"]),2 )
					 	machines.update_one({"_id":today.strftime("%d/%m/%Y")},
					 								{"$set": {"offtimeB": offtimeB,"offtime": offtimeB }}, upsert=True)
					if   24>currentTime >= 16:
					 	shiftChangeB = 1
					 	shiftChangeC = 1
					 	if shiftChangeA == 1:
					 		sessionStartTime = time.time()
					 		shiftChangeA = 0
					 	offtimeA = round(sessionRunPercent - (cursorMachine["elapsedTimeA"] + cursorMachine["idleTimeA"] + cursorMachine["problemtimeA"]),2) 
					 	machines.update_one({"_id":today.strftime("%d/%m/%Y")},
					 								{"$set": {"offtimeA": offtimeA,"offtime": offtimeA }}, upsert=True)
					if   8>currentTime >= 0:
					 	shiftChangeA = 1
					 	shiftChangeB = 1
					 	if shiftChangeC == 1:
					 		sessionStartTime = time.time()
					 		shiftChangeC = 0
					 	offtimeC = round(sessionRunPercent - (cursorMachine["elapsedTimeC"] + cursorMachine["idleTimeC"] + cursorMachine["problemtimeC"]),2 )
					 	machines.update_one({"_id":today.strftime("%d/%m/%Y")},
					 								{"$set": {"offtimeC": offtimeC,"offtime": offtimeC }}, upsert=True)

					if cursorMachine["machineStaus"] == 1:
						#starttime =  cursorMachine["startTime"]
						#if starttime == 0:
						#	machines.update_one({"machinename": cursorMachine}, {
						#	"$set": {"startTime": time.time(), "machineStaus": 1}}, upsert=True)
							
						runningTime = int(time.time() - cursorMachine["startTime"])
						#print(runningTime)
						time_difference_in_minutes = runningTime / 60
						time_difference_in_minutes = round(time_difference_in_minutes,2)
						#print(time_difference_in_minutes)
						time_difference_in_percent1 = time_difference_in_minutes*100/450
						time_difference_in_percent1 = round(time_difference_in_percent1,2)
						presentPercent1[y] = time_difference_in_percent1
						if(currentMinute != prevMinute):
							#print("time diff in minutes" + str(time_difference_in_minutes))
							#print("time diff in percent" , time_difference_in_percent1)
							#print(cursorMachine)
							#print(cursorMachine["startTime"])
							#print("runningTime ", runningTime)
							prevMinute = currentMinute
						if(presentPercent1[y] != prevPercent1[y]):
							print("Session Run Percent" , sessionRunTime)
							print("Session Run minutes" , sessionRunPercent)
							print(time_difference_in_minutes)
							if "elapsedTime" in cursorMachine:
								if   16>currentTime >= 8:
									#print("elapsedTimeB :", cursorMachine["elapsedTimeB"] )
									if serverStart:
										elapsedTime = presentPercent1[y]
									else:
										elapsedTime = cursorMachine["elapsedTimeB"] - prevPercent1[y] +\
														time_difference_in_percent1
									elapsedTime = round(elapsedTime,2)
									if elapsedTime > 99.5:
										elapsedTime = 100
									if elapsedTime < 0:
										elapsedTime = 0
									#print(elapsedTime)
									machines.update_one({"_id":today.strftime("%d/%m/%Y")},
													{"$set": {"elapsedTimeB": elapsedTime,"elapsedTime": elapsedTime}}, upsert=True)
								elif   24>currentTime >= 16:
									#print("elapsedTimeA :", cursorMachine["elapsedTimeA"] )
									if serverStart:
										elapsedTime = presentPercent1[y]
									else:
										elapsedTime = cursorMachine["elapsedTimeA"]  - prevPercent1[y] + \
													time_difference_in_percent1
									elapsedTime = round(elapsedTime,2)
									if elapsedTime > 99.5:
										elapsedTime = 100
									if elapsedTime < 0:
										elapsedTime = 0
									#print("elapsedtime:", elapsedTime)
									machines.update_one({"_id":today.strftime("%d/%m/%Y")},
													{"$set": {"elapsedTimeA": elapsedTime,"elapsedTime": elapsedTime}}, upsert=True)
								elif   8>currentTime >= 0:
									#print("elapsedTimeC :", cursorMachine["elapsedTimeC"] )
									if serverStart:
										elapsedTime = presentPercent1[y]
									else:
										elapsedTime = cursorMachine["elapsedTimeC"]  - prevPercent1[y] + \
													time_difference_in_percent1
									elapsedTime = round(elapsedTime,2)
									if elapsedTime > 99.5:
										elapsedTime = 100
									if elapsedTime < 0:
										elapsedTime = 0
									#print(elapsedTime)
									machines.update_one({"_id":today.strftime("%d/%m/%Y")},
													{"$set": {"elapsedTimeC": elapsedTime,"elapsedTime": elapsedTime}}, upsert=True)
							#print(elapsedTime , presentPercent1[y], prevPercent1[y], "hello" ,  time_difference_in_percent1 )
							prevPercent1[y] = time_difference_in_percent1
							
					
					if cursorMachine["machineStaus"] == 3:
						#starttime =  cursorMachine["problemstartTime"]
						#if starttime == 0:
						#	machines.update_one({"machinename": cursorMachine}, {
						#	"$set": {"problemstartTime": time.time(), "machineStaus": 3}}, upsert=True)
						runningTime = time.time() - cursorMachine["problemstartTime"]
						time_difference_in_minutes = runningTime / 60
						time_difference_in_minutes = round(time_difference_in_minutes,2)
						time_difference_in_percent2 = time_difference_in_minutes*100/450
						time_difference_in_percent2 = round(time_difference_in_percent2,2)
						#print(time_difference_in_percent2)
						presentPercent2[y] = time_difference_in_percent2
						if(presentPercent2[y] != prevPercent2[y]):
							if "problemtime" in cursorMachine:
								if   16>currentTime >= 8:
									if serverStart:
										elapsedTime = presentPercent2[y]
									else:
										elapsedTime = cursorMachine["problemtimeB"] - prevPercent2[y] + \
														time_difference_in_percent2
									elapsedTime = round(elapsedTime,2)
									if elapsedTime > 99.5:
										elapsedTime = 100
									if elapsedTime < 0:
										elapsedTime = 0
									#print(elapsedTime)
									machines.update_one({"_id":today.strftime("%d/%m/%Y")},
													{"$set": {"problemtimeB": elapsedTime,"problemtime": elapsedTime}}, upsert=True)
								if   24>currentTime >= 16:
									if serverStart:
										elapsedTime = presentPercent2[y]
									else:
										elapsedTime = cursorMachine["problemtimeA"] - prevPercent2[y] + \
														time_difference_in_percent2
									elapsedTime = round(elapsedTime,2)
									if elapsedTime > 99.5:
										elapsedTime = 100
									if elapsedTime < 0:
										elapsedTime = 0
									#print(elapsedTime)
									machines.update_one({"_id":today.strftime("%d/%m/%Y")},
													{"$set": {"problemtimeA": elapsedTime,"problemtime": elapsedTime}}, upsert=True)
								if   8>currentTime >= 0:
									if serverStart:
										elapsedTime = presentPercent2[y]
									else:
										elapsedTime = cursorMachine["problemtimeC"] - prevPercent2[y] + \
														time_difference_in_percent2
									elapsedTime = round(elapsedTime,2)
									if elapsedTime > 99.5:
										elapsedTime = 100
									if elapsedTime < 0:
										elapsedTime = 0
									#print(elapsedTime)
									machines.update_one({"_id":today.strftime("%d/%m/%Y")},
													{"$set": {"problemtimeC": elapsedTime,"problemtime": elapsedTime}}, upsert=True)
						prevPercent2[y] = time_difference_in_percent2

					if cursorMachine["machineStaus"] == 4:
						#starttime =  cursorMachine["idleStart"]
						#if starttime == 0:
						#	machines.update_one({"machinename": cursorMachine}, {
						#	"$set": {"idleStart": time.time(), "machineStaus": 3}}, upsert=True)
						runningTime = time.time() - cursorMachine["idleStart"]
						time_difference_in_minutes = runningTime / 60
						time_difference_in_minutes = round(time_difference_in_minutes,2)
						time_difference_in_percent3 = time_difference_in_minutes*100/450
						time_difference_in_percent3 = round(time_difference_in_percent3,2)
						#print(time_difference_in_percent3)
						presentPercent3[y] = time_difference_in_percent3
						if(presentPercent3[y] != prevPercent3[y]):
							if "idleTime" in cursorMachine:
								if   16>currentTime >= 8:
									if serverStart:
										elapsedTime = presentPercent3[y]
									else:
										elapsedTime = cursorMachine["idleTimeB"] - prevPercent3[y] + \
													time_difference_in_percent3
									elapsedTime = round(elapsedTime,2)
									if elapsedTime > 99.5:
										elapsedTime = 100
									if elapsedTime < 0:
										elapsedTime = 0
									#print(elapsedTime)
									machines.update_one({"_id":today.strftime("%d/%m/%Y")},
													{"$set": {"idleTimeB": elapsedTime,"idleTime": elapsedTime}}, upsert=True)
								if   24>currentTime >= 16:
									if serverStart:
										elapsedTime = presentPercent3[y]
									else:
										elapsedTime = cursorMachine["idleTimeA"] - prevPercent3[y] + \
														time_difference_in_percent3
									elapsedTime = round(elapsedTime,2)
									if elapsedTime > 99.5:
										elapsedTime = 100
									if elapsedTime < 0:
										elapsedTime = 0
									#print(elapsedTime)
									machines.update_one({"_id":today.strftime("%d/%m/%Y")},
													{"$set": {"idleTimeA": elapsedTime,"idleTime": elapsedTime}}, upsert=True)
								if   8>currentTime >= 0:
									if serverStart:
										elapsedTime = presentPercent3[y]
									else:
										elapsedTime = cursorMachine["idleTimeC"] - prevPercent3[y] + \
													time_difference_in_percent3
									elapsedTime = round(elapsedTime,2)
									if elapsedTime > 99.5:
										elapsedTime = 100
									if elapsedTime < 0:
										elapsedTime = 0
									#print(elapsedTime)
									machines.update_one({"_id":today.strftime("%d/%m/%Y")},
													{"$set": {"idleTimeC": elapsedTime,"idleTime": elapsedTime}}, upsert=True)
						prevPercent3[y] = time_difference_in_percent3
				serverStart = 0

threadOne = threading.Thread(target=checkDate)
threadOne.start()

app.run(host='0.0.0.0', port=5000)


