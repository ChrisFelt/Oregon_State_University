Communication Contract for RGBRandomizer Microservice  
CS 361  
Christopher Felt  

-----------------------------------------------------
Overview
-----------------------------------------------------

Welcome to the RGBRandomizer.py microservice README!

This microservice receives RGB data in a JSON format, randomizes the RGB values while maintaining any repeated patterns, then returns the randomized values to the client as a JSON. The following requirements must be met to successfully use the RGBRandomizer:  

1. The request and response JSON files must be in a dictionary format with a "status" key, and a "data" key.


2. The "data" key value must contain a list of dictionaries containing RGB data. 
   The exact format of the JSON is described in the 'How to REQUEST data' and 'How to RECEIVE data' sections.


3. All communication must take place via JSON file requests and responses. No other messages will be accepted or sent. 
   WARNING: if the request JSON does not match the prescribed format or contain a "status" key, the microservice will print a notification, ignore the request, and wait for the next message.


4. The microservice communicates with the client using ZeroMQ. 
   As such, it will be necessary for the client to import the 'zmq' package for Python, or other appropriate package(s) if it is written in a different language.  
   

Other notes:

The microservice communicates on the local host at port 7077.  

Once started, the RGBRandomizer will run indefinitely until the program is terminated. 
The microservice can receive and respond to any number of requests from the client while it is active.


Finally, to start the microservice, simply run RGBRandomizer.py from the command-line interface. No other files in this repository are necessary.

-----------------------------------------------------
How to REQUEST data:
-----------------------------------------------------

The client will send a JSON file to the microservice using ZeroMQ on tcp://localhost:7077.  

The JSON sent in the request must be a dictionary in the following format:
```
{
	"status":"run",
	"data":
	[
		{"r":40, "g":55, "b":70},
		{"r":40, "g":55, "b":70},
		{"r":33, "g":66, "b":120},
	]
}
```
Where the "status":"run" line tells the microservice to randomize the RGB combinations in the "data" section.  

Note: if the value of "status" is anything other than "run", the microservice will print a notification, ignore the message, and wait for the next message.


-----------------------------------------------------
How to RECEIVE data:
-----------------------------------------------------

The microservice will send a JSON to the client using ZeroMQ on the same port at tcp://localhost:7077.  

The JSON sent in the response will be a dictionary in the following format:
```
{
	"status":"done",
	"data":
	[
		{"r":155, "g":0, "b":25},
		{"r":155, "g":0, "b":25},
		{"r":197, "g":235, "b":71},
	]
}
```
Where the "status":"done" line tells the client that the "data" section has been successfully randomized.  

Note: The response message will ONLY take this format. The microservice will not send any other messages to the client.


-----------------------------------------------------
UML Sequence Diagram:
-----------------------------------------------------

![UML sketch](https://user-images.githubusercontent.com/54368648/180090719-173436d9-339d-4f3b-994a-6eab797890fb.png)
