# Title: RGB Randomizer Microservice
# Class: CS 361 - Software Engineering I
# Author: Christopher Felt
# Description: Microservice that uses ZeroMQ to communicate with a client.
# The microservice:
# 1. Waits for a json request from the client.
# 2. When a json request is received, runs a randomizer function on the RGB values it contains.
# 3. Returns the randomized RGB values as a json to the client.

import zmq
import random

# ZeroMQ socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:7077")


def randomize(request):
    """
    Randomizes the RGB values of a list of embroidery layers.
    :param request: A list of dictionaries with RGB key value pairs
    :return: A list of dictionaries with new, randomized RGB key value pairs
    """
    # create dictionary to track repeat colors
    repeat = {}

    # create set to track unique colors in request
    req_unique = set()

    # create set to track unique colors in response
    res_unique = set()

    response = []

    # iterate through RGB list
    for i in range(len(request)):

        rgb = request[i]["r"], request[i]["g"], request[i]["b"]

        if rgb not in req_unique:

            req_unique.add(rgb)

            # create randomized RGB tuple
            rand_rgb = rgb

            # generate new RGB combinations
            while rand_rgb == rgb or rand_rgb in res_unique:
                rand_rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            res_unique.add(rand_rgb)

            # add RGB value to response list and repeat dictionary
            response.append({"r": rand_rgb[0], "g": rand_rgb[1], "b": rand_rgb[2]})
            repeat[rgb] = rand_rgb

        # if RGB value is a duplicate in the original list, new value is also a duplicate
        else:
            res_duplicate = repeat[rgb]

            # add duplicate RGB value to response list
            response.append({"r": res_duplicate[0], "g": res_duplicate[1], "b": res_duplicate[2]})

    return response


if __name__ == '__main__':

    # wait for request...
    while True:
        request = socket.recv_json()

        print("\nReceived request:  \n%s " % request)

        # reject message if format is unexpected
        if type(request) is not dict:
            print("Invalid message format. Waiting for next message.")
            continue

        # reject message of no status key present
        elif "status" not in request:
            print("Invalid message format. Waiting for next message.")
            continue

        # check status
        status = request["status"]

        if status == "run":
            print("\nReceived request from client, generating randomized RGB values...")

            data = request["data"]

            res_rand = randomize(data)

            # respond to client
            response = request

            response["status"] = "done"
            response["data"] = res_rand

            print("\nSuccess! Waiting to send response JSON...")

            socket.send_json(response)

            print("\nResponse sent to client!")

        # if status is not run, wait for next message
        else:
            print("Invalid status. Waiting for next message.")
