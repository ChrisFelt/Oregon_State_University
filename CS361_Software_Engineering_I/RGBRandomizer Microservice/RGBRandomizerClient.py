# Title: RGB Randomizer Microservice Test Client
# Class: CS 361 - Software Engineering I
# Author: Christopher Felt
# Description: Test client that uses ZeroMQ to send and receive JSON files from RGBRandomizer


import zmq

context = zmq.Context()

# connect to server with socket
print("Connecting to server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:7077")

# send some requests to the server
while True:
    # prompt user to send request JSON
    user_input = input("\nSend a request to the RGBRandomizer microservice? Y/N: ")

    if user_input.lower() == 'y':

        # generate sample request JSON
        request = {
            "status":"run",
            "data":
                [
                    {"r": 180, "g": 180, "b": 180},
                    {"r": 0, "g": 255, "b": 50},
                    {"r": 180, "g": 180, "b": 180},
                    {"r": 30, "g": 55, "b": 0},
                    {"r": 71, "g": 235, "b": 50},
                    {"r": 180, "g": 180, "b": 180},
                    {"r": 30, "g": 55, "b": 0},
                ]
        }

        # send request to server
        print("\nSending request...")
        socket.send_json(request)

        # get and print response
        response = socket.recv_json()
        print("\nReceived reply:  \n%s " % response)

    else:
        break
