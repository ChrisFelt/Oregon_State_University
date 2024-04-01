from flask import Flask, render_template, json, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask import request
import os
import database.db_connector as db

# CONFIGURATION
app = Flask(__name__)
app.secret_key = 'rock lobster'
db_connection = db.connect_to_database()

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_behringr'
app.config['MYSQL_PASSWORD'] = '1834'
app.config['MYSQL_DB'] = 'cs340_behringr'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)


# ROUTES
@app.route('/')
def home():
    return redirect("/index")


@app.route('/index')
def index():
    return render_template("index.jinja2")


@app.route('/users', methods=["POST", "GET"])
def user():
    # READ
    if request.method == "GET":
        # get User data
        query = """SELECT Users.userID AS 'User ID', 
                        firstName AS 'First Name', 
                        lastName AS 'Last Name', 
                        address AS Address, 
                        specialization AS Specialization, 
                        bio AS Biography 
                    FROM Users;"""
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("users.jinja2", data=data)

    # CREATE
    if request.method == "POST":
        # get form data
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        address = request.form["address"]
        specialization = request.form["specialization"]
        bio = request.form["bio"]

        if request.form.get("Add_User"):

            # check if duplicate entry
            checkQuery = """SELECT COUNT(userID) AS count FROM Users 
                                WHERE firstName = %s 
                                AND lastName = %s;"""
            cur = mysql.connection.cursor()
            cur.execute(checkQuery, (firstName, lastName))
            checkUser = cur.fetchall()

            if checkUser[0]['count'] != 0:
                flash('Duplicate names are not allowed! Please try again.', 'error')

            else:
                # account for null specialization AND bio
                if specialization == "" and bio == "":

                    # mySQL query to insert a new person into bsg_people with our form inputs
                    query = "INSERT INTO Users (firstName, lastName, address) VALUES (%s, %s, %s);"
                    cur = mysql.connection.cursor()
                    cur.execute(query, (firstName, lastName, address))
                    mysql.connection.commit()
                # account for null specialization
                elif specialization == "":
                    query = "INSERT INTO Users (firstName, lastName, address, bio) VALUES (%s, %s, %s, %s);"
                    cur = mysql.connection.cursor()
                    cur.execute(query, (firstName, lastName, address, bio))
                    mysql.connection.commit()
                # account for null bio
                elif bio == "":
                    query = "INSERT INTO Users (firstName, lastName, address, specialization) VALUES (%s, %s, %s, %s);"
                    cur = mysql.connection.cursor()
                    cur.execute(query, (firstName, lastName, address, specialization))
                    mysql.connection.commit()
                # account for NO null
                else:
                    query = """INSERT INTO Users (firstName, lastName, address, specialization, bio) VALUES (%s, 
                                %s, 
                                %s, 
                                %s, 
                                %s);"""
                    cur = mysql.connection.cursor()
                    cur.execute(query, (firstName, lastName, address, specialization, bio))
                    mysql.connection.commit()

            return redirect("/users")


@app.route('/edit_user/<int:id>', methods=["POST", "GET"])
def edit_user(id):
    # READ
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM Users WHERE userID = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        data = cur.fetchall()

        return render_template("edit_user.jinja2", data=data)

    # UPDATE
    if request.method == "POST":
        # gather form data
        userID = request.form["userID"]
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        address = request.form["address"]
        specialization = request.form["specialization"]
        bio = request.form["bio"]

        if request.form.get("Edit_User"):

            # check if duplicate entry
            checkQuery = """SELECT userID FROM Users 
                                WHERE firstName = %s 
                                AND lastName = %s;"""
            cur = mysql.connection.cursor()
            cur.execute(checkQuery, (firstName, lastName))
            checkUser = cur.fetchall()

            if checkUser and int(userID) != checkUser[0]['userID']:
                flash('Duplicate names are not allowed! Please try again.', 'error')

            else:
                # account for null specialization AND bio
                if specialization == "" and bio == "":
                    query = """UPDATE Users SET Users.firstName = %s, 
                                    Users.lastName = %s, 
                                    Users.address = %s, 
                                    Users.specialization = NULL, 
                                    Users.bio = NULL 
                                    WHERE Users.userID = %s;"""
                    cur = mysql.connection.cursor()
                    cur.execute(query, (firstName, lastName, address, userID))
                    mysql.connection.commit()
                # account for null specialization
                elif specialization == "":
                    query = """UPDATE Users SET Users.firstName = %s, 
                                    Users.lastName = %s, 
                                    Users.address = %s, 
                                    Users.specialization = NULL, 
                                    Users.bio = %s 
                                    WHERE Users.userID = %s;"""
                    cur = mysql.connection.cursor()
                    cur.execute(query, (firstName, lastName, address, bio, userID))
                    mysql.connection.commit()
                # account for null bio
                elif bio == "":
                    query = """UPDATE Users SET Users.firstName = %s, 
                                    Users.lastName = %s, 
                                    Users.address = %s, 
                                    Users.specialization = %s, 
                                    Users.bio = NULL 
                                    WHERE Users.userID = %s;"""
                    cur = mysql.connection.cursor()
                    cur.execute(query, (firstName, lastName, address, specialization, userID))
                    mysql.connection.commit()
                # account for NO null
                else:
                    query = """UPDATE Users SET Users.firstName = %s, 
                                    Users.lastName = %s, 
                                    Users.address = %s, 
                                    Users.specialization = %s, 
                                    Users.bio = %s 
                                    WHERE Users.userID = %s;"""
                    cur = mysql.connection.cursor()
                    cur.execute(query, (firstName, lastName, address, specialization, bio, userID))
                    mysql.connection.commit()

        return redirect("/users")


@app.route('/rocks', methods=["POST", "GET"])
def rock():
    # READ
    if request.method == "GET":
        # get Rock data
        query = """SELECT Rocks.rockID AS 'Rock Number', 
                        Rocks.name AS 'Rock Name', 
                        CONCAT(Users.firstName, ' ', Users.lastName) AS Owner, 
                        Rocks.geoOrigin AS 'Place of Origin', 
                        Rocks.type AS 'Rock Type', 
                        Rocks.description AS 'Description', 
                        Rocks.chemicalComp AS 'Chemical Composition' 
                    FROM Rocks 
                        INNER JOIN Users ON Rocks.userID = Users.userID;"""
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # get User names
        usersQuery = "SELECT userID, CONCAT(firstName, ' ', lastName) AS fullName FROM Users;"
        cur = mysql.connection.cursor()
        cur.execute(usersQuery)
        users = cur.fetchall()

        return render_template("rocks.jinja2", data=data, users=users)

    # CREATE
    if request.method == "POST":

        if request.form.get("Add_Rock"):
            # get form variables
            userID = request.form["userID"]
            name = request.form["name"]
            geoOrigin = request.form["geoOrigin"]
            type = request.form["type"]
            description = request.form["description"]
            chemicalComp = request.form["chemicalComp"]

            # check if duplicate name
            checkQuery = """SELECT COUNT(rockID) AS count FROM Rocks 
                                WHERE name = %s;"""
            cur = mysql.connection.cursor()
            cur.execute(checkQuery, (name,))  # comma after name is required!
            checkRock = cur.fetchall()

            if checkRock[0]['count'] != 0:
                flash('Duplicate rock names are not allowed! Please try again.', 'error')

            else:
                query = """INSERT INTO Rocks (userID, name, geoOrigin, type, description, chemicalComp) VALUES (%s, 
                            %s, 
                            %s, 
                            %s, 
                            %s, 
                            %s);"""
                cur = mysql.connection.cursor()
                cur.execute(query, (userID, name, geoOrigin, type, description, chemicalComp))
                mysql.connection.commit()

            return redirect("/rocks")

        elif request.form.get("Rock_Search"):
            term = request.form["search"]

            # URI cannot end in a period
            if term == ".":
                return redirect(url_for("rock_search", term='%2E'))

            # send GET request to rock search page
            return redirect(url_for("rock_search", term=str(term)))


@app.route('/rock_search/<string:term>', methods=["POST", "GET"])
def rock_search(term):

    # convert if term is a period
    if term == '%2E':
        term = "."

    # READ
    # get rock column names for table - can't figure out how to make the search work with aliases containing spaces
    colNameQuery = """SELECT Rocks.rockID AS 'Rock Number', 
                    Rocks.name AS 'Rock Name', 
                    CONCAT(Users.firstName, ' ', Users.lastName) AS Owner, 
                    Rocks.geoOrigin AS 'Place of Origin', 
                    Rocks.type AS 'Rock Type', 
                    Rocks.description AS 'Description', 
                    Rocks.chemicalComp AS 'Chemical Composition' 
                FROM Rocks 
                    INNER JOIN Users ON Rocks.userID = Users.userID;"""
    cur = mysql.connection.cursor()
    cur.execute(colNameQuery)
    colData = cur.fetchall()

    # ROCK SEARCH
    if request.method == "GET":
        # mySQL query to return all rows in Rocks that contain the given substring
        query = """WITH rockSearch AS
                     (SELECT Rocks.rockID,
                             Rocks.name,
                             CONCAT(Users.firstName, ' ', Users.lastName) AS owner,
                             Rocks.geoOrigin,
                             Rocks.type,
                             Rocks.description,
                             Rocks.chemicalComp
                      FROM Rocks
                               INNER JOIN Users
                                          ON Rocks.userID = Users.userID -- get name of User owner
                     )
                    -- SELECT rows that match search criteria from rockSearch
                    SELECT *
                    FROM rockSearch
                    WHERE owner LIKE %s
                       OR name LIKE %s
                       OR geoOrigin LIKE %s
                       OR type LIKE %s
                       OR description LIKE %s
                       OR chemicalComp LIKE %s;"""
        cur = mysql.connection.cursor()
        cur.execute(query, ('%' + term + '%', '%' + term + '%', '%' + term + '%', '%' + term + '%',
                            '%' + term + '%', '%' + term + '%'))
        data = cur.fetchall()

        return render_template("rock_search.jinja2", term=term, data=data, colData=colData)


@app.route('/reviews', methods=["POST", "GET"])
def review():
    # READ
    if request.method == "GET":
        # get Reviews
        query = """SELECT Reviews.reviewID AS 'Review ID', 
                        CONCAT(Users.firstName, ' ', Users.lastName) AS Reviewer, 
                        Rocks.name AS Rock, 
                        Reviews.title AS Title, 
                        Reviews.body AS Review, 
                        Reviews.rating AS Rating 
                            FROM Reviews 
                                LEFT JOIN Users 
                                    ON Reviews.userID = Users.userID 
                                INNER JOIN Rocks 
                                    ON Reviews.rockID = Rocks.rockID 
                        ORDER BY Reviews.reviewID ASC;"""
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # get User names
        usersQuery = "SELECT userID, CONCAT(firstName, ' ', lastName) AS fullName FROM Users;"
        cur = mysql.connection.cursor()
        cur.execute(usersQuery)
        users = cur.fetchall()

        # get Rock names
        rocksQuery = "SELECT rockID, name FROM Rocks;"
        cur = mysql.connection.cursor()
        cur.execute(rocksQuery)
        rocks = cur.fetchall()

        return render_template("reviews.jinja2", data=data, rocks=rocks, users=users)

    # CREATE
    if request.method == "POST":
        # collect form data
        userID = request.form["userID"]
        rockID = request.form["rockID"]
        title = request.form["title"]
        body = request.form["body"]
        rating = request.form["rating"]

        if request.form.get("Add_Review"):

            # check if duplicate Review only if userID NOT NULL
            if userID != "":
                checkQuery = """SELECT COUNT(reviewID) AS count FROM Reviews 
                                    WHERE rockID = %s
                                    AND userID = %s;"""
                cur = mysql.connection.cursor()
                cur.execute(checkQuery, (rockID, userID))
                checkReview = cur.fetchall()

                # notify user if Review is a duplicate
                if checkReview[0]['count'] != 0:
                    flash('Duplicate reviews are not allowed! Please try again.', 'error')

                # CREATE Review with userID
                else:
                    query = "INSERT INTO Reviews (userID, rockID, title, body, rating) VALUES (%s, %s, %s, %s, %s);"
                    cur = mysql.connection.cursor()
                    cur.execute(query, (userID, rockID, title, body, rating))
                    mysql.connection.commit()

                return redirect("/reviews")

            # account for NULL userID
            elif userID == "":
                query = "INSERT INTO Reviews (rockID, title, body, rating) VALUES (%s, %s, %s, %s);"
                cur = mysql.connection.cursor()
                cur.execute(query, (rockID, title, body, rating))
                mysql.connection.commit()

        return redirect("/reviews")


@app.route('/edit_review/<int:id>', methods=["POST", "GET"])
def edit_review(id):
    # READ
    if request.method == "GET":
        # general READ query for Reviews
        query = """SELECT Reviews.reviewID AS 'Review ID', 
                        CONCAT(Users.firstName, ' ', Users.lastName) AS Reviewer, 
                        Rocks.name AS Rock, 
                        Reviews.title AS Title, 
                        Reviews.body AS Review, 
                        Reviews.rating AS Rating 
                            FROM Reviews 
                                LEFT JOIN Users 
                                    ON Reviews.userID = Users.userID 
                                INNER JOIN Rocks 
                                    ON Reviews.rockID = Rocks.rockID
                        WHERE Reviews.reviewID = %s;"""
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        readData = cur.fetchall()

        # READ query for UPDATE
        query = "SELECT * FROM Reviews WHERE reviewID = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        data = cur.fetchall()

        # fetch Reviewers
        usersQuery = "SELECT userID, CONCAT(firstName, ' ', lastName) AS fullName FROM Users;"
        cur = mysql.connection.cursor()
        cur.execute(usersQuery)
        users = cur.fetchall()

        # fetch Rocks
        rocksQuery = "SELECT rockID, name FROM Rocks;"
        cur = mysql.connection.cursor()
        cur.execute(rocksQuery)
        rocks = cur.fetchall()

        return render_template("edit_review.jinja2", readData=readData, data=data, users=users, rocks=rocks)

    # UPDATE
    if request.method == "POST":
        # collect form data
        reviewID = id
        userID = request.form["userID"]
        rockID = request.form["rockID"]
        title = request.form["title"]
        body = request.form["body"]
        rating = request.form["rating"]
        # get original User and Rock
        prevUserID = request.form["prevUserID"]
        prevRockID = request.form["prevRockID"]

        if request.form.get("Edit_Review"):

            # check if duplicate Review only if userID NOT NULL
            if userID != "" and (prevUserID != userID or prevRockID != rockID):
                checkQuery = """SELECT COUNT(reviewID) AS count FROM Reviews 
                                    WHERE rockID = %s
                                    AND userID = %s;"""
                cur = mysql.connection.cursor()
                cur.execute(checkQuery, (rockID, userID))
                checkReview = cur.fetchall()

                # notify user if Review is a duplicate
                if checkReview[0]['count'] != 0:
                    flash('Duplicate reviews are not allowed! Please try again.', 'error')
                    return redirect("/reviews")

            # account for NULL userID
            if userID == "":
                query = """UPDATE Reviews SET Reviews.userID = NULL, 
                                    Reviews.rockID = %s, 
                                    Reviews.title = %s, 
                                    Reviews.body = %s, 
                                    Reviews.rating = %s 
                                    WHERE Reviews.reviewID = %s;"""
                cur = mysql.connection.cursor()
                cur.execute(query, (rockID, title, body, rating, reviewID))
                mysql.connection.commit()

            # account for no NULL
            else:
                query = """UPDATE Reviews SET Reviews.userID = %s, 
                                    Reviews.rockID = %s, 
                                    Reviews.title = %s, 
                                    Reviews.body = %s, 
                                    Reviews.rating = %s 
                                    WHERE Reviews.reviewID = %s;"""
                cur = mysql.connection.cursor()
                cur.execute(query, (userID, rockID, title, body, rating, reviewID))
                mysql.connection.commit()

        return redirect("/reviews")


@app.route('/shipments', methods=["POST", "GET"])
def shipment():
    # READ
    if request.method == "GET":
        # get Shipment data
        shipmentsQuery = """SELECT Shipments.shipmentID AS 'Shipment Number', 
                                CONCAT(Users.firstName, ' ', Users.lastName) AS 'User', 
                                Shipments.shipOrigin AS 'Origin', 
                                Shipments.shipDest AS 'Destination', 
                                Shipments.shipDate AS 'Date Shipped', 
                                Shipments.miscNote AS 'Notes' 
                                FROM Shipments 
                                    INNER JOIN Users 
                                        ON Shipments.userID = Users.userID;"""
        cur = mysql.connection.cursor()
        cur.execute(shipmentsQuery)
        data = cur.fetchall()

        # fetch Rocks
        rocksQuery = "SELECT name FROM Rocks;"
        cur = mysql.connection.cursor()
        cur.execute(rocksQuery)
        rocks = cur.fetchall()

        # fetch Users
        usersQuery = "SELECT CONCAT(firstName, ' ', lastName) FROM Users;"
        cur = mysql.connection.cursor()
        cur.execute(usersQuery)
        users = cur.fetchall()

        return render_template("shipments.jinja2", data=data, rocks=rocks, users=users)

    # CREATE Shipment
    if request.method == "POST":
        # collect form data
        user = request.form["user"]
        rock = request.form["rock"]
        shipOrigin = request.form["shipOrigin"]
        shipDest = request.form["shipDest"]
        shipDate = request.form["shipDate"]
        miscNote = request.form["miscNote"]

        if request.form.get("Add_Shipment"):

            # display error popup if shipment exists with same date and same rock
            checkRock = """SELECT COUNT(Shipments_has_Rocks.shipmentID) AS count,
                                Shipments.shipDate,
                                Rocks.name 
                                FROM Shipments_has_Rocks
                                INNER JOIN Shipments
                                ON Shipments_has_Rocks.shipmentID = Shipments.shipmentID
                                INNER JOIN Rocks
                                ON Shipments_has_Rocks.rockID = Rocks.rockID
                                WHERE Rocks.name = %s AND Shipments.shipDate = %s;"""
            cur = mysql.connection.cursor()
            cur.execute(checkRock, (rock, shipDate))
            checkRockShip = cur.fetchall()

            # notify user if entry is a duplicate
            if checkRockShip[0]['count'] != 0:
                flash('The same rock cannot be in more than one shipment on the same date! Please try again.', 'error')
                return redirect("/shipments")

            # account for null miscNote
            if miscNote == "":

                # check if duplicate entry
                checkQuery1 = """SELECT COUNT(shipmentID) AS count FROM Shipments 
                                    WHERE shipOrigin = %s 
                                    AND shipDest = %s
                                    AND shipDate = %s
                                    AND miscNote IS NULL;"""
                cur = mysql.connection.cursor()
                cur.execute(checkQuery1, (shipOrigin, shipDest, shipDate))
                checkShipNull = cur.fetchall()

                # Null value could be converted to 'None' in the form
                checkQuery2 = """SELECT COUNT(shipmentID) AS count FROM Shipments 
                                    WHERE shipOrigin = %s 
                                    AND shipDest = %s
                                    AND shipDate = %s
                                    AND miscNote = 'None';"""
                cur = mysql.connection.cursor()
                cur.execute(checkQuery2, (shipOrigin, shipDest, shipDate))
                checkShipNone = cur.fetchall()

                # notify user if entry is a duplicate
                if checkShipNull[0]['count'] != 0 or checkShipNone[0]['count'] != 0:
                    flash('Duplicate entry! Shipment not added. Please try again.', 'error')

                else:
                    # first, SQL query to insert new Shipment
                    shipQuery = """INSERT INTO Shipments (userID, shipOrigin, shipDest, shipDate, miscNote) 
                                    VALUES ((SELECT userID FROM Users WHERE CONCAT(firstName, ' ', lastName) = %s), 
                                    %s, 
                                    %s, 
                                    %s, 
                                    NULL);"""
                    cur = mysql.connection.cursor()
                    cur.execute(shipQuery, (user, shipOrigin, shipDest, shipDate))
                    mysql.connection.commit()
                    # next, SQL query to insert new Shipments_has_Rocks
                    shipRockQuery = """INSERT INTO Shipments_has_Rocks (shipmentID, rockID) 
                                        VALUES ((SELECT shipmentID FROM Shipments 
                                            WHERE shipOrigin = %s 
                                                AND shipDest = %s 
                                                AND shipDate = %s 
                                                AND miscNote IS NULL), 
                                        (SELECT rockID FROM Rocks WHERE name = %s));"""
                    cur = mysql.connection.cursor()
                    cur.execute(shipRockQuery, (shipOrigin, shipDest, shipDate, rock))
                    mysql.connection.commit()

            # account for NO null
            else:

                # check if duplicate entry
                checkQuery = """SELECT COUNT(shipmentID) AS count FROM Shipments 
                                    WHERE shipOrigin = %s 
                                    AND shipDest = %s
                                    AND shipDate = %s
                                    AND miscNote = %s;"""
                cur = mysql.connection.cursor()
                cur.execute(checkQuery, (shipOrigin, shipDest, shipDate, miscNote))
                checkShip = cur.fetchall()

                # notify user if entry is a duplicate
                if checkShip[0]['count'] != 0:
                    flash('Duplicate entry! Shipment not added. Please try again.', 'error')

                else:
                    # first, SQL query to insert new Shipment
                    shipQuery = """INSERT INTO Shipments (userID, shipOrigin, shipDest, shipDate, miscNote) 
                                    VALUES ((SELECT userID FROM Users WHERE CONCAT(firstName, ' ', lastName) = %s), 
                                    %s, 
                                    %s, 
                                    %s, 
                                    %s);"""
                    cur = mysql.connection.cursor()
                    cur.execute(shipQuery, (user, shipOrigin, shipDest, shipDate, miscNote))
                    mysql.connection.commit()
                    # next, SQL query to insert new Shipments_has_Rocks
                    shipRockQuery = """INSERT INTO Shipments_has_Rocks (shipmentID, rockID) 
                                        VALUES ((SELECT shipmentID FROM Shipments 
                                            WHERE shipOrigin = %s 
                                                AND shipDest = %s 
                                                AND shipDate = %s 
                                                AND miscNote = %s), 
                                        (SELECT rockID FROM Rocks WHERE name = %s));"""
                    cur = mysql.connection.cursor()
                    cur.execute(shipRockQuery, (shipOrigin, shipDest, shipDate, miscNote, rock))
                    mysql.connection.commit()

            return redirect("/shipments")


# edit Shipments and Shipments_has_Rocks page
@app.route('/edit_shipment/<int:id>', methods=["POST", "GET"])
def edit_shipment(id):
    # READ
    if request.method == "GET":
        # get shipment data with some snappy monikers
        readShipmentQuery = """SELECT Shipments.shipmentID AS 'Shipment Number', 
                                CONCAT(Users.firstName, ' ', Users.lastName) AS 'User', 
                                Shipments.shipOrigin AS 'Origin', 
                                Shipments.shipDest AS 'Destination', 
                                Shipments.shipDate AS 'Date Shipped', 
                                Shipments.miscNote AS 'Notes'
                                FROM Shipments 
                                    INNER JOIN Users 
                                        ON Shipments.userID = Users.userID 
                                WHERE Shipments.shipmentID = %s;"""
        cur = mysql.connection.cursor()
        cur.execute(readShipmentQuery, (id,))
        readShipment = cur.fetchall()

        # get shipment data vanilla style
        editShipmentQuery = """SELECT Shipments.shipmentID, 
                                CONCAT(Users.firstName, ' ', Users.lastName) AS user, 
                                Shipments.shipOrigin, 
                                Shipments.shipDest, 
                                Shipments.shipDate, 
                                Shipments.miscNote
                                FROM Shipments 
                                    INNER JOIN Users 
                                        ON Shipments.userID = Users.userID 
                                WHERE Shipments.shipmentID = %s;"""
        cur = mysql.connection.cursor()
        cur.execute(editShipmentQuery, (id,))
        editShipment = cur.fetchall()

        # get Rock names and their owner's names
        rocksQuery = """SELECT Shipments_has_Rocks.shipmentHasRockID,
                            CONCAT(Users.firstName, ' ', Users.lastName) AS 'Owner', 
                            Rocks.name AS 'Rock Name' 
                            From Shipments_has_Rocks
                                INNER JOIN Shipments
                                    ON Shipments_has_Rocks.shipmentID = Shipments.shipmentID
                                INNER JOIN Rocks
                                    ON Shipments_has_Rocks.rockID = Rocks.rockID
                                LEFT JOIN Users
                                    ON Rocks.userID = Users.userID
                            WHERE Shipments_has_Rocks.shipmentID = %s;"""
        cur = mysql.connection.cursor()
        cur.execute(rocksQuery, (id,))
        rocks = cur.fetchall()

        # get Rock names and their owner's names
        addRocksQuery = """SELECT Rocks.name AS rock
                            FROM Rocks
                                WHERE rockID NOT IN (SELECT rockID FROM Shipments_has_Rocks WHERE shipmentID = %s);"""
        cur = mysql.connection.cursor()
        cur.execute(addRocksQuery, (id,))
        addRocks = cur.fetchall()

        # get all User names BESIDES the original User in the Shipment
        shipUsersOptionQuery = """SELECT CONCAT(firstName, ' ', lastName) AS name
                                    FROM Users 
                                    WHERE userID != (SELECT userID from Shipments WHERE shipmentID = %s)
                                    GROUP BY name;"""
        cur = mysql.connection.cursor()
        cur.execute(shipUsersOptionQuery, (id,))
        shipUsersOption = cur.fetchall()

        # get the original User in the Shipment
        shipUserQuery = """SELECT CONCAT(firstName, ' ', lastName) AS name 
                            FROM Users 
                            WHERE userID = (SELECT userID from Shipments WHERE shipmentID = %s);"""
        cur = mysql.connection.cursor()
        cur.execute(shipUserQuery, (id,))
        shipUser = cur.fetchall()

        return render_template("edit_shipment.jinja2", readShipment=readShipment, editShipment=editShipment,
                               rocks=rocks, addRocks=addRocks, shipUsersOption=shipUsersOption, shipUser=shipUser)

    # UPDATE
    if request.method == "POST":
        # update shipment attributes only
        if request.form.get("Edit_Shipment"):

            # gather variables from Add_Shipment form
            user = request.form["user"]
            shipOrigin = request.form["shipOrigin"]
            shipDest = request.form["shipDest"]
            shipDate = request.form["shipDate"]
            miscNote = request.form["miscNote"]

            # get previous values
            prevUser = request.form["prevUser"]
            prevShipOrigin = request.form["prevShipOrigin"]
            prevShipDest = request.form["prevShipDest"]
            prevShipDate = request.form["prevShipDate"]
            prevMiscNote = request.form["prevMiscNote"]

            # replace 'None' with ""
            if prevMiscNote == 'None':
                prevMiscNote = ""

            # check previous values against new
            unchangedUser = (user == prevUser)
            unchangedShipment = (shipOrigin == prevShipOrigin) \
                                and (shipDest == prevShipDest) \
                                and (shipDate == prevShipDate) \
                                and (miscNote == prevMiscNote)

            # account for null miscNote
            if miscNote == "":

                # skip if no values changed
                if not unchangedShipment or not unchangedUser:
                    # check if duplicate entry
                    checkQuery1 = """SELECT COUNT(shipmentID) AS count FROM Shipments 
                                        WHERE shipOrigin = %s 
                                        AND shipDest = %s
                                        AND shipDate = %s
                                        AND miscNote IS NULL;"""
                    cur = mysql.connection.cursor()
                    cur.execute(checkQuery1, (shipOrigin, shipDest, shipDate))
                    checkShipNull = cur.fetchall()

                    # Null value could be converted to 'None' in the form
                    checkQuery2 = """SELECT COUNT(shipmentID) AS count FROM Shipments 
                                        WHERE shipOrigin = %s 
                                        AND shipDest = %s
                                        AND shipDate = %s
                                        AND miscNote = 'None';"""
                    cur = mysql.connection.cursor()
                    cur.execute(checkQuery2, (shipOrigin, shipDest, shipDate))
                    checkShipNone = cur.fetchall()

                    if checkShipNull[0]['count'] != 0 or checkShipNone[0]['count'] != 0:
                        flash('Duplicate entry! Shipment not added. Please try again.', 'error')
                        return redirect("/edit_shipment/" + str(id))

                    else:
                        # first, SQL query to insert new Shipment
                        shipUpdateQuery = """UPDATE Shipments
                                                SET userID = (SELECT userID FROM Users 
                                                WHERE CONCAT(firstName, ' ', lastName) = %s),
                                                shipOrigin = %s,
                                                shipDest = %s,
                                                shipDate = %s, 
                                                miscNote = NULL
                                                WHERE shipmentID = %s;"""
                        cur = mysql.connection.cursor()
                        cur.execute(shipUpdateQuery, (user, shipOrigin, shipDest, shipDate, id))
                        mysql.connection.commit()

                # if just user changed, allow update
                elif not unchangedUser:
                    # first, SQL query to insert new Shipment
                    shipUpdateQuery = """UPDATE Shipments
                                            SET userID = (SELECT userID FROM Users 
                                            WHERE CONCAT(firstName, ' ', lastName) = %s),
                                            shipOrigin = %s,
                                            shipDest = %s,
                                            shipDate = %s, 
                                            miscNote = NULL
                                            WHERE shipmentID = %s;"""
                    cur = mysql.connection.cursor()
                    cur.execute(shipUpdateQuery, (user, shipOrigin, shipDest, shipDate, id))
                    mysql.connection.commit()

            # account for NO null
            else:

                # skip if no values changed
                if not unchangedShipment or not unchangedUser:
                    # check if duplicate entry
                    checkQuery = """SELECT COUNT(shipmentID) AS count FROM Shipments 
                                        WHERE shipOrigin = %s 
                                        AND shipDest = %s
                                        AND shipDate = %s
                                        AND miscNote = %s;"""
                    cur = mysql.connection.cursor()
                    cur.execute(checkQuery, (shipOrigin, shipDest, shipDate, miscNote))
                    checkShip = cur.fetchall()

                    # notify user of duplicate shipment
                    if checkShip[0]['count'] != 0:
                        flash('Duplicate entry! Shipment not added. Please try again.', 'error')
                        return redirect("/edit_shipment/" + str(id))

                    else:
                        # first, SQL query to insert new Shipment
                        shipUpdateQuery = """UPDATE Shipments
                                                SET userID = (SELECT userID FROM Users 
                                                WHERE CONCAT(firstName, ' ', lastName) = %s),
                                                shipOrigin = %s,
                                                shipDest = %s,
                                                shipDate = %s,
                                                miscNote = %s
                                                WHERE shipmentID = %s;"""
                        cur = mysql.connection.cursor()
                        cur.execute(shipUpdateQuery, (user, shipOrigin, shipDest, shipDate, miscNote, id))
                        mysql.connection.commit()

                # if just user changed, allow update
                elif not unchangedUser:
                    # first, SQL query to insert new Shipment
                    shipUpdateQuery = """UPDATE Shipments
                                            SET userID = (SELECT userID FROM Users 
                                            WHERE CONCAT(firstName, ' ', lastName) = %s),
                                            shipOrigin = %s,
                                            shipDest = %s,
                                            shipDate = %s, 
                                            miscNote = NULL
                                            WHERE shipmentID = %s;"""
                    cur = mysql.connection.cursor()
                    cur.execute(shipUpdateQuery, (user, shipOrigin, shipDest, shipDate, id))
                    mysql.connection.commit()

            return redirect("/shipments")


@app.route("/delete_shipment/<int:id>")
def delete_shipment(id):
    # SQL query to delete the Shipment given id
    query = "DELETE FROM Shipments WHERE shipmentID =  %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    return redirect("/shipments")


# add Shipments_has_Rocks (single Rock addition to existing Shipment)
@app.route("/add_shipments_has_rocks/<int:id>", methods=["POST"])
def add_shipments_has_rocks(id):
    # add rock to shipment
    if request.form.get("Add_Shipments_has_Rocks"):
        # gather variable from Add_Shipments_has_Rocks form
        rock = request.form["rock"]
        shipDate = request.form["shipDate"]

        # display error popup if shipment exists with same date and same rock
        checkRock = """SELECT COUNT(Shipments_has_Rocks.shipmentID) AS count,
                                        Shipments.shipDate,
                                        Rocks.name 
                                        FROM Shipments_has_Rocks
                                        INNER JOIN Shipments
                                        ON Shipments_has_Rocks.shipmentID = Shipments.shipmentID
                                        INNER JOIN Rocks
                                        ON Shipments_has_Rocks.rockID = Rocks.rockID
                                        WHERE Rocks.name = %s AND Shipments.shipDate = %s;"""
        cur = mysql.connection.cursor()
        cur.execute(checkRock, (rock, shipDate))
        checkRockShip = cur.fetchall()

        # notify user if entry is a duplicate
        if checkRockShip[0]['count'] != 0:
            flash('The same rock cannot be in more than one shipment on the same date! Please try again.', 'error')

        # CREATE Shipments_has_Rocks
        else:
            query = """INSERT INTO Shipments_has_Rocks (shipmentID, rockID)
                        VALUES (%s,
                        (SELECT rockID FROM Rocks WHERE name = %s));"""
            cur = mysql.connection.cursor()
            cur.execute(query, (id, rock))
            mysql.connection.commit()

            flash(rock + ' added to shipment.', 'success')

        return redirect("/edit_shipment/" + str(id))


@app.route("/delete_shipments_has_rocks/<int:id>")
def delete_shipments_has_rocks(id):
    # save shipmentID
    shipQuery = "SELECT shipmentID FROM Shipments_has_Rocks WHERE shipmentHasRockID = %s;"
    cur = mysql.connection.cursor()
    cur.execute(shipQuery, (id,))
    shipmentID = cur.fetchall()
    # get value from query
    shipmentID = str(shipmentID[0]["shipmentID"])

    # get Rock name
    rockQuery = """SELECT Rocks.name AS Rock
                        FROM Rocks 
                        INNER JOIN Shipments_has_Rocks
                        ON Rocks.rockID = Shipments_has_Rocks.rockID
                        WHERE shipmentHasRockID = %s;"""
    cur = mysql.connection.cursor()
    cur.execute(rockQuery, (id,))
    rock = cur.fetchall()
    # get value from query
    rock = str(rock[0]["Rock"])

    # SQL query to delete the Shipment given id
    query = "DELETE FROM Shipments_has_Rocks WHERE shipmentHasRockID =  %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # check if no Rocks left in Shipment
    checkQuery = "SELECT COUNT(shipmentID) AS count FROM Shipments_has_Rocks WHERE shipmentID = %s;"
    cur = mysql.connection.cursor()
    cur.execute(checkQuery, (shipmentID,))
    checkRocks = cur.fetchall()
    # get value from query
    checkRocks = str(checkRocks[0]["count"])

    # if no Rocks left in Shipment, delete Shipment
    if checkRocks == "0":
        # delete Shipment
        deleteShipmentQuery = "DELETE FROM Shipments WHERE shipmentID = %s;"
        cur = mysql.connection.cursor()
        cur.execute(deleteShipmentQuery, (shipmentID,))
        mysql.connection.commit()

        flash('Last rock removed! Shipment deleted.', 'success')
        return redirect("/shipments")

    else:
        flash(rock + ' removed from shipment.', 'success')
        return redirect("/edit_shipment/" + shipmentID)


###########################################

# LISTENER
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 41992))

    app.run(port=port, debug=True)
