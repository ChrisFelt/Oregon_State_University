# Title: Flash Card User
# Class: CS 361 - Software Engineering I
# Author: Christopher Felt
# Description: Defines the User class used in the Flash Card app.

import json
from pathlib import Path
import os
import zmq

# prepare socket for search microservice communication
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:7077")


def data_open(name):
    """open and read user's json file if it exists"""
    data_file = Path(name + ".json")
    if data_file.is_file():
        # open file and load into data
        with open(name + '.json', 'r') as in_file:
            return json.load(in_file)

    # dictionary defaults to empty
    else:
        return {}


class User:
    """Represents a user, with credentials and flash cards."""

    def __init__(self, name, pwd):
        """initialize data members"""
        # get user data
        self._data = data_open(name)

        # save user details
        self._name = name
        self._pwd = pwd
        self._cred = {name: pwd}

        # create credential file if it does not exist
        cred_file = Path(name + ".txt")
        if cred_file.is_file() is False:
            with open(name + ".txt", 'w') as file:
                file.write(json.dumps(self._cred))

    def valid_index(self, pos):
        """check if the given index falls within the dictionary"""
        pos = int(pos) - 1
        if 0 <= pos < len(self._data):
            return True
        else:
            return False

    def add_card(self, pos, front, back):
        """adds a flash card entry to given collection in user._data"""
        pos = int(pos) - 1

        # create dictionary if no cards
        if self._data == {}:
            self._data = {list(self._data.keys())[pos]: {front: back}}

        # add card to dictionary
        else:
            self._data[list(self._data.keys())[pos]][front] = back

    def add_coll(self, coll):
        """"adds an empty collection to self._data"""
        self._data[coll] = {}

    def show_coll(self):
        """prints a numbered list of all collections"""
        i = 1
        # print list
        for front, back in self._data.items():
            print(str(i) + ". " + front)

            # screen break every 10 cards
            if i % 10 == 0:
                input("\nPress any key to continue...\n")

            i += 1

    def show_cards(self, pos):
        """shows cards in a given collection"""
        pos = int(pos) - 1
        # print front and back of card in order sorted by front
        i = 1
        print("Cards (front | back):")
        for front, back in self._data[list(self._data.keys())[pos]].items():
            print("    " + str(i) + ". " + front + "  |  " + back)

            # screen break every 10 cards
            if i % 10 == 0:
                input("\nPress any key to continue...\n")

            i += 1

    def show_all(self):
        """given the index of a collection, prints a numbered list of all flash cards"""

        # print collection
        for j in range(len(self._data)):
            print(str(j + 1) + ". " + list(self._data.keys())[j])
            i = 1
            # print list
            for front, back in self._data[list(self._data.keys())[j]].items():
                print("    " + front)

                # screen break every 10 cards
                if i % 10 == 0:
                    input("\nPress any key to continue...\n")

                i += 1

    def study_cards(self, pos):
        """given the index of a collection, prints flash cards in self._data in front -> back order"""
        pos = int(pos) - 1

        # print front and back of card in order sorted by front
        i = 1
        for front, back in self._data[list(self._data.keys())[pos]].items():
            print("\nShowing flash card #" + str(i) + ".")
            print("Front: " + front)
            input("----------------")
            print("Back: " + back)
            input("Press any key to see next card...")
            i += 1

    def edit_card(self, coll, key, key_str, value):
        """edit a card in the given collection at the given position"""

        # retype indices and save collection and card keys to a list
        coll = int(coll) - 1
        key = int(key) - 1
        coll_list = list(self._data)
        card_list = list(self._data[coll_list[coll]])

        # swap old key with new, then update value
        self._data[coll_list[coll]][key_str] = self._data[coll_list[coll]].pop(card_list[key])
        self._data[coll_list[coll]][key_str] = value

    def save_cards(self):
        """saves self.data contents as a json to same directory"""
        with open(self._name + '.json', 'w') as out_file:
            out_file.write(json.dumps(self._data))

    def delete_card(self, coll, key):
        """delete a card in the given collection at the given position"""

        # retype indices
        coll = int(coll) - 1
        key = int(key) - 1

        coll_list = list(self._data)
        card_list = list(self._data[coll_list[coll]])

        del self._data[coll_list[coll]][card_list[key]]

    def delete_all(self):
        """deletes cards from self._data and from hard drive"""
        # delete data
        self._data = {}
        # delete file if it exists
        data_file = Path(self._name + ".json")
        if data_file.is_file():
            os.remove(self._name + '.json')

    def no_cards(self):
        """returns true if user has no cards, otherwise false"""
        if self._data == {}:
            return True
        else:
            return False

    def print_result(self, result):
        """print the results of a search"""
        print("\nFound the following matches: ")

        # print collection
        for coll, data in result.items():
            print("Collection name: " + coll)
            print("Cards (front | back):")

            # print cards
            i = 1
            for front, back in result[coll].items():
                print("    " + str(i) + ". " + front + "  |  " + back)

                # screen break every 10 cards
                if i % 10 == 0:
                    input("\nPress any key to continue...\n")
                i += 1

    def search_comms(self, term):
        """handles communication with the search microservice"""
        # generate and send request
        request = {
            "status": "run",
            "search term": term,
            "data": self._data
        }
        socket.send_json(request)

        response = socket.recv_json()
        return response

    def search(self, term):
        """search self._data for cards that match term"""
        # send flash card JSON to search microservice
        response = self.search_comms(term)

        # check if search was successful
        if response["status"] != "done":
            print("\nSearch failed. Please try again.")

        # get search results from response
        else:
            result = response["data"]

            if result == {}:
                print("\nNo matches found for " + term + ".")

            else:
                self.print_result(result)
