# Title: Flash Card App
# Class: CS 361 - Software Engineering I
# Author: Christopher Felt
# Description: A flash card app that runs via a command prompt interface.

import json
from pathlib import Path
from FlashCardUser import User


# ---------------------------------------------------------------------------
#
# General use functionality
#
# ---------------------------------------------------------------------------

def print_divide():
    """prints a screen divide"""
    print("\n---------------------------------------------"
          "\n")


# ---------------------------------------------------------------------------
#
# Login page functionality
#
# ---------------------------------------------------------------------------

def authenticate(name, pwd):
    """checks user name/pwd against existing credentials"""
    # check if user credential txt file exists
    file = Path(name + ".txt")
    if file.is_file():
        # open and read file
        with open(name + '.txt', 'r') as in_file:
            credential = json.load(in_file)

        # check if pwd matches file contents
        if str(credential[name]) == pwd:
            return True

    return False


def credential_input():
    """receives login input and logs user in"""
    name = input("\nUsername -> ")
    pwd = input("Password -> ")

    # authenticate input and access account
    if authenticate(name, pwd) is True:
        print("\nSuccess! Opening your account, " + name + ".")
        account(name, pwd)

    else:
        print("\nLogin failed. Please enter a valid Username and password.")
        return


def login():
    """login screen routine"""
    while True:
        print_divide()
        # prompt user
        login_input = input("Please select an option: "
                            "\n1. Enter Username"
                            "\n2. Return to previous screen"
                            "\n-> ")

        # attempt login
        if login_input == "1":
            credential_input()

            # if return from successful account login, exit login loop
            break

        # return to previous screen
        if login_input == "2":
            print("\nReturning to previous screen.")
            return

        # invalid entry
        else:
            print("Error! Please enter a valid input.")
            continue


# ---------------------------------------------------------------------------
#
# Account page functionality
#
# ---------------------------------------------------------------------------

def add_coll(user):
    """add collection for create card"""
    coll_name = input("\nEnter collection name: ")

    # confirm collection
    print("\nYou have entered: " + coll_name)
    finalize = input("\nSave this collection? Y/N: ")

    # save collection
    if finalize.lower() == "y":
        user.add_coll(coll_name)
        input("Collection added! Press any key to return...")

    # do nothing
    elif finalize.lower() == "n":
        print("Collection not saved.")
        return


def add_card_confirmation(user, pos):
    """gets and confirms card data for add card"""
    front = input("\nEdit front of card: ")
    back = input("Edit back of card: ")

    # confirm card
    print("\nYou have entered front: " + front + "\nAnd back: " + back)
    finalize = input("\nSave this card? Y/N: ")

    # save card
    if finalize.lower() == "y":
        user.add_card(pos, front, back)
        print("Card saved!")

    elif finalize.lower() == "n":
        print("Card not saved.")
        return

    else:
        input("Invalid entry. Press any key to return to account...")


def add_card(user):
    """add a new card to a collection for create card"""
    if user.no_cards():
        print("\nYou have no collections! Make a collection first.")
        return

    else:
        print("\nYour collections: ")
        user.show_coll()
        pos = input("\nSelect a collection to add the card to: ")

        # if user entry is valid, proceed to card creation
        if pos.isdigit() and user.valid_index(pos):
            add_card_confirmation(user, pos)

        # invalid pos input
        else:
            input("Invalid entry. Press any key to return to account...")


def create_card(user):
    """card creation routine: prompts user to create and add cards to collections."""
    print_divide()
    # create flash card routine
    while True:
        card_input = input("\nWelcome to card creation! Please select an option: "
                           "\n1. Create new collection - start here!"
                           "\n2. Add card to collection"
                           "\n3. Return to previous screen"
                           "\n-> ")
        # new collection
        if card_input == "1":
            add_coll(user)

        # new card
        elif card_input == "2":
            add_card(user)

        # return to previous screen
        elif card_input == "3":
            break

        else:
            input("\nInvalid input! Press any key to return...")
            continue


def display_cards_study(user):
    """card studying function for display cards"""
    print("\nShowing a list of all of your collections and their cards: ")
    user.show_all()

    pos = input("\nEnter the number of the collection you wish to browse: ")

    # if valid entry, browse cards for the given collection
    if pos.isdigit() and user.valid_index(pos):
        user.study_cards(pos)

    # otherwise return to account
    else:
        input("Invalid entry! Press any key to return to account...")
        return


def display_cards(user):
    """display cards from edit/delete menu"""
    # check for cards
    if user.no_cards():
        print("\nYou currently have no cards to view! Please make a new card from your account menu.")
        input("Press any key to return to the previous screen...")

    # show user's flash cards
    else:
        display_cards_study(user)

        input("\nNo more cards to show. Press any key to return to account...")


def search_cards(user):
    """search card option from edit/delete menu"""
    search_term = input("\nPlease enter a search phrase: ")
    
    user.search(search_term)
    input("\nPress any key to return...")


def edit_cards_confirmation(user, coll):
    """selects and confirms edits for a card in a collection for edit cards"""
    print("\nSelect card to edit:")
    user.show_cards(coll)

    # get edit inputs for edit_card()
    key = input("\nEnter selection: ")
    front = input("Enter front: ")
    back = input("Enter back: ")

    confirm = input("You entered front: " + front + " | back: " + back +
                    ". \nKeep edits? Y/N: ")

    if confirm.lower() == "y":
        user.edit_card(coll, key, front, back)

    else:
        "Edit will not be saved."


def edit_cards(user):
    """edit card option from edit/delete menu"""
    print("\nSelect a collection:")
    user.show_coll()

    coll = input("\nEnter selection: ")

    # get card to edit
    if user.valid_index(coll):
        edit_cards_confirmation(user, coll)

    else:
        print("Invalid entry!")


def delete_one_confirmation(user, coll):
    """confirms and deletes one card for delete one"""
    print("\nSelect card to delete:")
    user.show_cards(coll)

    key = input("\nEnter selection: ")
    confirm = input("Delete this card? Y/N: ")

    # delete card
    if confirm.lower() == "y":
        user.delete_card(coll, key)

    else:
        "No changes made."


def delete_one(user):
    """delete one card from edit/delete menu"""
    print("\nSelect a collection:")
    user.show_coll()

    coll = input("\nEnter selection: ")

    # get card to delete
    if user.valid_index(coll):
        delete_one_confirmation(user, coll)

    else:
        print("Invalid entry!")


def delete_all(user):
    """delete all cards from edit/delete menu"""
    delete = input("Delete your card(s)? Y/N: ")

    # delete all cards in user object and hdd flash card file associated with user credentials
    if delete.lower() == "y":
        print("Cards deleted!")
        user.delete_all()

    elif delete.lower() == "n":
        print("Cards will not be deleted.")

    else:
        print("Invalid entry. Returning to account.")


def edit_delete_menu(user):
    """edit/delete menu selection from account"""
    edit_input = input("\nSelect an option below:"
                       "\n1. Edit a card"
                       "\n2. Delete a card"
                       "\n3. Delete ALL cards"
                       "\n-> ")
    # edit a card
    if edit_input == "1":
        edit_cards(user)

    # delete one card
    elif edit_input == "2":
        delete_one(user)

    # delete ALL
    elif edit_input == "3":
        delete_all(user)


def account(name, pwd):
    """account page routine"""
    # create user object with credentials
    user = User(name, pwd)

    while True:
        print_divide()
        account_input = input("Welcome to your FlashCard account! Please enter the number of an option below:"
                              "\n1. View your flash cards - cycles through each card in a collection."
                              "\n2. Create new flash card or collection - create and customize in just two steps!"
                              "\n3. Search your cards"
                              "\n4. Edit/delete your flash cards - new!"
                              "\n5. Logoff"
                              "\n6. Help options"
                              "\n-> ")

        # display flash card
        if account_input == "1":
            display_cards(user)

        # create flash card
        elif account_input == "2":
            create_card(user)

        # search cards
        elif account_input == "3":
            search_cards(user)

        # edit/delete
        elif account_input == "4":
            edit_delete_menu(user)

        # save cards and logoff
        elif account_input == "5":
            user.save_cards()
            break

        # help menu/invalid entry
        else:
            print("\nWelcome to user account help.")
            print("To navigate, please enter the number of the choice you wish after the -> symbol.")
            print("Any other key entry will bring you to the help menu.")
            input("To return to your account page, press any key...")
            continue


# ---------------------------------------------------------------------------
#
# Create new account page functionality
#
# ---------------------------------------------------------------------------

def user_name_select():
    """user name and password selection for create account"""
    while True:
        user_name = input("\nEnter your new user name: ")

        # check if credential file exists
        cred_file = Path(user_name + ".txt")
        if cred_file.is_file():
            print("Error! That user name already exists. Please enter a new choice.")
            exit_create = input("Or type Q to return to the previous screen: ")

            # return to account creation screen
            if exit_create.lower() == "q":
                return

            else:
                continue

        # create new credentials
        else:
            user_pwd = input("Please enter a new password: ")

            print("\nAccount creation successful!")
            input("Logging into your account. Press any key to continue...")

            # log user into account
            account(user_name, user_pwd)
        return


def create_account():
    """create a new user account"""
    while True:
        print_divide()
        # prompt user
        create_input = input("Welcome aboard to FlashCard! Please select an option: "
                             "\n1. Select your user name"
                             "\n2. Return to login screen"
                             "\n3. Help options"
                             "\n-> ")

        if create_input == "1":
            user_name_select()
            return

        # return to previous screen
        elif create_input == "2":
            return

        # help menu/invalid input
        else:
            print("\nWelcome to account creation help.")
            print("To navigate, please enter the number of the choice you wish after the -> symbol.")
            print("Any other key entry will bring you to the help menu.")
            input("To return to account creation, press any key...")
            continue


if __name__ == '__main__':

    # initialize app
    while True:
        print_divide()

        # main menu prompt
        user_input = input("Welcome to FlashCard! Please choose an option: "
                           "\n1. Login"
                           "\n2. Create new account"
                           "\n3. Exit FlashCard"
                           "\n4. Help options"
                           "\n-> ")

        # go to login screen
        if user_input == "1":
            login()

        # go to new account creation
        elif user_input == "2":
            create_account()

        # terminate program
        elif user_input == "3":
            break

        # all other key entries
        else:
            print("\nWelcome to FlashCard help.")
            print("To navigate, please enter the number of the choice you wish after the -> symbol.")
            print("Any other key entry will bring you to the help menu.")
            input("To return to the main menu, press any key...")
            continue
