from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from pymongo import MongoClient # Database connector
from bson.objectid import ObjectId # For ObjectId to work

client = MongoClient('localhost', 27017)    #Configure the connection to the database
db = client.arduinoDb    #Select the database
todos = db.todo #Select the collection
machines = db.machines #collection for storing list of machines
# machineTimings = db.machineTimings

app = Flask(__name__)
title = "TODO with Flask"
heading = "ToDo Reminder"
#modify=ObjectId()

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

@app.route("/")
def apiWelcome():
	return "this is api for our aurdino"

@app.route("/ON")
def machineOn():
	machine = machines.find_one({"machinename":"arduino123"})

	print(machine)

	return machine

@app.route("/OFF")
def machineOff():
	print("machine data recieved")
	return "hello"	

@app.route("/MACHINEPROBLEM")
def machineProblem():
	print("machine data recieved")
	return "hello"

@app.route("/IDLE")
def machineIdle():
	print("machine data recieved")
	return "hello"

@app.route("/createmachine")
def createmachine():
	print("machine data recieved")
	hello = machines.insert_one({"machinename": "arduino124", "machineStaus": 0, "totalTimeOn": 0 })
	print(hello.inserted_id)
	return "hello"


if __name__ == "__main__":
    app.run(debug=True)
# Careful with the debug mode..


