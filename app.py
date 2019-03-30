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

goin = 1

# modify=ObjectId()
#now = datetime.datetime.now(pytz.timezone(TIME_ZONE))
now=round(time.time(),0)
cdt =datetime.datetime

nofmachines = db.machines.count()
print(nofmachines)
#machinesID = machines.find({},{"machinename":1})
machinesID = machines.distinct("machinename")
print(machinesID)
if nofmachines > 0:
		for i in machinesID:
				print("am in")		
				machines.update_one({"machinename": i},
								{"$set": {"machineStaus": 0,}}, upsert=True)

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
fh = open("records.txt", "a")
		
def redirect_url():
	return request.args.get('next') or \
		request.referrer or \
		url_for('index')


@app.route("/") #TESTING PART
def apiWelcome():
	global goin
	goin = 0
	#threadOne.join()
	global prevDate
	currentTime = datetime.datetime.now()
	currentTime = currentTime.strftime("%H")
	print(request.remote_addr)
	fh = open("records.txt", "a")
	fh.writelines(str(datetime.datetime.now()) +  "Just an empty request" + "\n")
	goin = 1
	return "this is api for our aurdino"
	
	
                        #ON REQUEST

@app.route("/ON/<machineID>") 
def machineOn(machineID):
	global goin
	goin = 0
	#threadOne.join()
	global currentDate
	global prevPercent1
	#prevPercent1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	#presentPercent1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	print(machineID)	
	print(prevPercent1)
	currentTime = datetime.datetime.now()
	currentTime = currentTime.strftime("%H")
	#print(currentTime)
	orMachine = machines.find_one({"machinename": machineID})
	fh = open("records.txt", "a")
	fh.writelines(str(datetime.datetime.now()) + "ON " + machineID + "\n")
	#print(currentDate,prevDate)
	if orMachine["machineStaus"] != 1:
		machines.update_one({"machinename": machineID}, {
							"$set": {"startTime": time.time(), "machineStaus": 1}}, upsert=True)
		goin = 1
		return "switched on"
	else:
		goin = 1
		return "already on"
	

                         #OFF REQUEST

@app.route("/OFF/<machineID>")
def machineOff(machineID):
	global goin
	global prevPercent1
	goin = 0
	#threadOne.join()
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	#print(currentTime)
	#print(currentDate,prevDate)
	cursorMachine = machines.find_one({"machinename": machineID})
	fh = open("records.txt", "a")
	fh.writelines(str(datetime.datetime.now()) + "OFF " + machineID + "\n")
	if cursorMachine["machineStaus"] != 0:
		machines.update_one({"machinename": machineID}, {
							"$set": {"stopTime": time.time(), "machineStaus": 0}}, upsert=True)
		print(machinesID.index(machineID))
		prevPercent1[machinesID.index(machineID) + 1] = 0
		print(prevPercent1)
	
	
		goin = 1
	else:
		goin = 1
		return "machine already off "
	goin = 1



                    #PROBLEM REQUEST


@app.route("/PROBLEM/<machineID>") 
def machineProblem(machineID):
	global goin
	goin = 0
	#threadOne.join()
	global prevPercent2
	#prevPercent2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	orMachine = machines.find_one({"machinename": machineID})
	fh = open("records.txt", "a")
	fh.writelines(str(datetime.datetime.now()) + "PROBLEM " + machineID + "\n")
	if orMachine["machineStaus"] != 3:
	    machines.update_one({"machinename": machineID},
						{"$set": {"problemstartTime": time.time(),"machineStaus":3}}, upsert=True)
	print("machine data recieved")
	goin = 1
	return "machine problem"
	


                        #PROBLEM SOLVED REQUEST


@app.route("/PROBLEMSOLVED/<machineID>") 
def machineProblemSolved(machineID):
	global goin
	global prevPercent2
	goin = 0
	#threadOne.join()
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	#print(currentDate,prevDate)
	cursorMachine = machines.find_one({"machinename": machineID})
	fh = open("records.txt", "a")
	fh.writelines(str(datetime.datetime.now()) + "PROBLEMOFF " + machineID + "\n")
	if cursorMachine["machineStaus"] != 2:
		machines.update_one({"machinename": machineID}, {
                            "$set": {"problemstopTime": time.time(), "machineStaus": 2}}, upsert=True)
		print(machinesID.index(machineID))
		prevPercent2[machinesID.index(machineID) + 1] = 0
		print(prevPercent2)
		
		goin = 1	
	else:
		goin = 1
		return "there is an error"
	



                        #IDLE REQUEST

@app.route("/IDLE/<machineID>")
def machineIdle(machineID):
	global goin
	goin = 0
	#threadOne.join()
	global prevPercent3
	#prevPercent3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	orMachine = machines.find_one({"machinename": machineID})
	fh = open("records.txt", "a")
	fh.writelines(str(datetime.datetime.now()) + "IDLE " + machineID + "\n")
	#print(currentDate,prevDate)
	if orMachine["machineStaus"] != 4:
	    machines.update_one({"machinename": machineID}, {
						"$set": {"machineStaus":4, "idleStart": time.time()}}, upsert=True)
	print("machine data recieved IN AIDA1")
	goin = 1
	return "Machine idle"
	




                   ##IDLEOFF REQUEST

@app.route("/IDLEOFF/<machineID>")
def machineIdleoff(machineID):
	global goin
	global prevPercent3
	goin = 0
	#threadOne.join()
	currentTime = datetime.datetime.now()
	currentTime = int(currentTime.strftime("%H"))
	print(currentTime)
	cursorMachine = machines.find_one({"machinename": machineID})
	fh = open("records.txt", "a")
	fh.writelines(str(datetime.datetime.now()) + "IDLEOFF " + machineID + "\n")
	if cursorMachine["machineStaus"] != 5:
		machines.update_one({"machinename": machineID}, {
						"$set": {"machineStaus":5, "idleStop":time.time()}}, upsert=True)
		print(machinesID.index(machineID))
		prevPercent3[machinesID.index(machineID) + 1] = 0
		print(prevPercent3)
		
	goin = 1


                       ##create machines from database##
@app.route("/createmachine/<machineID>")
def createmachine(machineID):
	global goin
	goin = 0
	#threadOne.join()
	global nofmachines
	global machinesID
	currentTime = datetime.datetime.now()
	currentTime = currentTime.strftime("%H")
	fh = open("records.txt", "a")
	fh.writelines(str(datetime.datetime.now()) + "machine created " + machineID + "\n")
	print(currentTime)
	print("machine created")
	hello = machines.insert_one({"machinename": machineID, "machineStaus": 0,
								 "totalTimeOn": 0, "elapsedTime": 0,"idleTime": 0,"problemtime": 0, "offtime": 0, "elapsedTimeB": 0, "problemtimeB": 0, "idleTimeB": 0, "offtimeB": 0, "elapsedTimeA": 0, "problemtimeA": 0, "idleTimeA": 0, "offtimeA": 0, "elapsedTimeC": 0, "problemtimeC": 0, "idleTimeC": 0, "offtimeC":0})
	print(hello.inserted_id)
	time.sleep(5)
	nofmachines = nofmachines + 1
	machinesID.append(machineID)
	print(nofmachines)
	print(machinesID)
	goin = 1
	return "machine created"
	

                    ##get data from app##

@app.route("/mob/getmachines")
def getmachinesfn():
	print("machine data recieved")
	fh = open("records.txt", "a")
	fh.writelines(str(datetime.datetime.now()) + " got machine data in mobile" + "\n")
	machine = machines.find()
	return dumps(machine)


def checkDate():
	global goin
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
			sessionRunMins = sessionRunTime/60
			sessionRunPercent = round(sessionRunMins *100 / 450)

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
						machines.update_one({"machinename": i},
												{"$set": {"offtimeB": 0,"offtime": 0,"offtimeC": 0,"offtimeA": 0,}}, upsert=True)
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
					cursorMachine = machines.find_one({"machinename": i})
					#print("current cursor machine is :", cursorMachine)
					if   16>currentTime >= 8:
					 	shiftChangeA = 1
					 	shiftChangeC = 1
					 	if shiftChangeB == 1:
					 		sessionStartTime = time.time()
					 		shiftChangeB = 0
					 	offtimeB = sessionRunPercent - (cursorMachine["elapsedTimeB"] + cursorMachine["idleTimeB"] + cursorMachine["problemtimeB"]) 
					 	machines.update_one({"machinename": i},
					 								{"$set": {"offtimeB": offtimeB}}, upsert=True)
					if   24>currentTime >= 16:
					 	shiftChangeB = 1
					 	shiftChangeC = 1
					 	if shiftChangeA == 1:
					 		sessionStartTime = time.time()
					 		shiftChangeA = 0
					 	offtimeA = sessionRunPercent - (cursorMachine["elapsedTimeA"] + cursorMachine["idleTimeA"] + cursorMachine["problemtimeA"]) 
					 	machines.update_one({"machinename": i},
					 								{"$set": {"offtimeA": offtimeA}}, upsert=True)
					if   8>currentTime >= 0:
					 	shiftChangeA = 1
					 	shiftChangeB = 1
					 	if shiftChangeC == 1:
					 		sessionStartTime = time.time()
					 		shiftChangeC = 0
					 	offtimeC = sessionRunPercent - (cursorMachine["elapsedTimeC"] + cursorMachine["idleTimeC"] + cursorMachine["problemtimeC"]) 
					 	machines.update_one({"machinename": i},
					 								{"$set": {"offtimeC": offtimeC}}, upsert=True)

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
							print(runningTime)
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
									machines.update_one({"machinename": i},
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
									machines.update_one({"machinename": i},
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
									machines.update_one({"machinename": i},
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
									machines.update_one({"machinename": i},
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
									machines.update_one({"machinename": i},
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
									machines.update_one({"machinename": i},
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
									machines.update_one({"machinename": i},
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
									machines.update_one({"machinename": i},
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
									machines.update_one({"machinename": i},
													{"$set": {"idleTimeC": elapsedTime,"idleTime": elapsedTime}}, upsert=True)
						prevPercent3[y] = time_difference_in_percent3
				serverStart = 0


threadOne = threading.Thread(target=checkDate)
threadOne.start()

app.run(host='0.0.0.0', port=8081)
	
# Careful with the debug mode..

