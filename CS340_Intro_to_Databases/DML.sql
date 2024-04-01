-- CS 340 Intro to Databases
-- Project Step 3 Draft: DML
-- Team Rock Bottom
-- Members: Robert Behring and Christopher Felt


-- -----------------------------------------------------
-- Users Data Manipulation Queries
-- -----------------------------------------------------

-- CREATE
-- add a new User
-- account for null specialization AND bio
INSERT INTO Users (firstName, lastName, address)
VALUES (:firstNameInput,
        :lastNameInput,
        :addressInput,
        :NULL,
        :NULL);
-- account for null specialization
INSERT INTO Users (firstName, lastName, address, bio)
VALUES (:firstNameInput,
        :lastNameInput,
        :addressInput,
        :NULL,
        :bioInput);
-- account for null bio
INSERT INTO Users (firstName, lastName, address, specialization)
VALUES (:firstNameInput,
        :lastNameInput,
        :addressInput,
        :specializationInput,
        :NULL);
-- account for NO null
INSERT INTO Users (firstName, lastName, address, specialization, bio)
VALUES (:firstNameInput,
        :lastNameInput,
        :addressInput,
        :specializationInput,
        :bioInput);


-- READ
-- get all Users for the browse Users table
SELECT userID         AS 'User ID',
       firstName      AS 'First Name',
       lastName       AS 'Last Name',
       address        AS Address,
       specialization AS Specialization,
       bio            AS Biography
FROM Users;


-- UPDATE '/edit_user'
-- update a User's data using form input data
-- Display selected userID information on edit_user page
SELECT *
FROM Users
WHERE userID = :userIDInput;
-- Accounting for 4 different UPDATES depending on NULL inputs
-- account for null specialization AND bio
UPDATE Users
SET Users.firstName      = :firstNameInput,
    Users.lastName       = :lastNameInput,
    Users.address        = :addressInput,
    Users.specialization = :NULL,
    Users.bio            = :NULL
WHERE Users.userID = :userIDInput;
-- account for null specialization
UPDATE Users
SET Users.firstName      = :firstNameInput,
    Users.lastName       = :lastNameInput,
    Users.address        = :addressInput,
    Users.specialization = :NULL,
    Users.bio            = :bioInput
WHERE Users.userID = :userIDInput;
-- account for null bio
UPDATE Users
SET Users.firstName      = :firstNameInput,
    Users.lastName       = :lastNameInput,
    Users.address        = :addressInput,
    Users.specialization = :specializationInput,
    Users.bio            = :NULL
WHERE Users.userID = :userIDInput;
-- account for NO null
UPDATE Users
SET Users.firstName      = :firstNameInput,
    Users.lastName       = :lastNameInput,
    Users.address        = :addressInput,
    Users.specialization = :specializationInput,
    Users.bio            = :bioInput
WHERE Users.userID = :userIDInput;


-- -----------------------------------------------------
-- Rocks Data Manipulation Queries
-- -----------------------------------------------------

-- CREATE
-- add a new Rock
INSERT INTO Rocks (userID, name, geoOrigin, type, description, chemicalComp)
VALUES (:userIDInput,
        :nameInput,
        :geoOriginInput,
        :typeInput,
        :descriptionInput,
        :chemicalCompInput);


-- READ
-- get all Rocks for the browse Rocks table
SELECT Rocks.rockID                                 AS 'Rock Number',
       CONCAT(Users.firstName, ' ', Users.lastName) AS Owner,
       Rocks.name                                   AS 'Rock Name',
       Rocks.geoOrigin                              AS 'Place of Origin',
       Rocks.type                                   AS 'Rock Type',
       Rocks.description                            AS 'Description',
       Rocks.chemicalComp                           AS 'Chemical Composition'
FROM Rocks
         INNER JOIN Users
                    ON Rocks.userID = Users.userID;
-- get name of User owner
SELECT userID, CONCAT(firstName, ' ', lastName) AS fullName
FROM Users

-- SEARCH
-- search all non-key attributes as well as owners of Rocks for any rows that match the search criteria
         WITH rockSearch AS
         (SELECT Rocks.rockID,
                 CONCAT(Users.firstName, ' ', Users.lastName) AS owner,
                 Rocks.name,
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
WHERE owner LIKE :searchInput
   OR name LIKE :searchInput
   OR geoOrigin LIKE :searchInput
   OR type LIKE :searchInput
   OR description LIKE :searchInput
   OR chemicalComp LIKE :searchInput;


-- -----------------------------------------------------
-- Reviews Data Manipulation Queries
-- -----------------------------------------------------

-- CREATE
-- add a new Review
INSERT INTO Reviews (userID, rockID, title, body, rating)
VALUES (SELECT userID FROM Users WHERE CONCAT(firstName, ' ', lastName) = :name_from_dropdown_input,
        SELECT rockID FROM Rocks WHERE name = :name_from_dropdown_input,
        title = :titleInput,
        body = :bodyInput,
        rating = :rating_from_dropdown_input);


-- READ
-- get all Reviews for the browse Reviews table
SELECT Reviews.reviewID,
       CONCAT(Users.firstName, ' ', Users.lastName) AS reviewer,
       Rocks.name                                   AS rock,
       Reviews.title,
       Reviews.body,
       Reviews.rating
FROM Reviews
         LEFT JOIN Users -- select Reviews that have a NULL userID as well
                   ON Reviews.userID = Users.userID -- User doing Review
         INNER JOIN Rocks
                    ON Reviews.rockID = Rocks.rockID;
-- name of Rock for Review


-- UPDATE
-- update Review data using form input data
-- first, get Review
SELECT reviewID,
       reviewer,
       rock,
       title,
       body,
       rating
FROM Reviews
WHERE reviewID = :reviewID_selected_in_form;
-- pulled from onclick event when edit Review link is clicked
-- then, update Review
UPDATE Reviews
SET reviewer = :userID_from_dropdown_input,
    rock     = :rockID_from_rock_input,
    title    = :titleInput,
    body     = :bodyInput,
    rating   = :ratingInput
WHERE reviewID = :reviewID_selected_in_form;


-- -----------------------------------------------------
-- Shipments Data Manipulation Queries
-- and Shipments_has_Rocks Data Manipulation Queries
-- -----------------------------------------------------

-- ACCOUNT FOR NULL miscNotes INPUT
-- CREATE I
-- SHIP -FROM- USER (the User's address will auto-populate in the shipOrigin field)
-- Part I: insert new row in Shipments
INSERT INTO Shipments (userID, shipOrigin, shipDest, shipDate)
VALUES (SELECT userID FROM Users WHERE CONCAT(firstName, ' ', lastName) = :name_from_dropdown_input,
        SELECT address FROM Users WHERE CONCAT(firstName, ' ', lastName) = :auto_populates_from_name_dropdown_input,
        shipDest = :shipDestInput,
        shipDate = :shipDateInput,);
-- Part II: insert new row in Shipments_has_Rocks intersection table for each rock shipped
INSERT INTO Shipments_has_Rocks (shipmentID, rockID)
VALUES (SELECT shipmentID
        FROM Shipments
        WHERE shipOrigin = :shipOrigin_in_form
          AND shipDest = :shipDest_in_form
          AND shipDate = :shipDate_in_form,
        SELECT rockID FROM Rocks WHERE name = :name_from_dropdown_input);

-- ACCOUNT FOR NULL miscNotes INPUT
-- CREATE II
-- SHIP -TO- USER (the User's address will auto-populate in the shipDest field)
-- Part I: insert new row in Shipments
INSERT INTO Shipments (userID, shipOrigin, shipDest, shipDate)
VALUES (SELECT address FROM Users WHERE CONCAT(firstName, ' ', lastName) = :auto_populates_from_name_dropdown_input,
        SELECT userID FROM Users WHERE CONCAT(firstName, ' ', lastName) = :name_from_dropdown_input,
        shipDest = :shipDestInput,
        shipDate = :shipDateInput,);
-- Part II: insert new row in Shipments_has_Rocks intersection table for each rock shipped
INSERT INTO Shipments_has_Rocks (shipmentID, rockID)
VALUES (SELECT shipmentID
        FROM Shipments
        WHERE shipOrigin = :shipOrigin_in_form
          AND shipDest = :shipDest_in_form
          AND shipDate = :shipDate_in_form,
        SELECT rockID FROM Rocks WHERE name = :name_from_dropdown_input);

---------------------------------------------------------------------------------------------------------

-- CREATE I
-- NULL miscNote
-- Part I: check for duplicate entry (cannot have duplicate Shipments)
SELECT COUNT(shipmentID) AS count FROM Shipments
    WHERE shipOrigin = shipOriginInput
    AND shipDest = :shipDestInput
    AND shipDate = :shipDateInput
    AND miscNote IS NULL;

-- Part II: insert new row in Shipments
INSERT INTO Shipments (userID, shipOrigin, shipDest, shipDate, miscNote)
VALUES (SELECT userID FROM Users WHERE CONCAT(firstName, ' ', lastName) = :name_from_dropdown_input,
        SELECT address FROM Users WHERE CONCAT(firstName, ' ', lastName) = :auto_populates_from_name_dropdown_input,
        shipDest = :shipDestInput,
        shipDate = :shipDateInput,
        miscNote = :miscNoteInput);

-- Part III: insert new row in Shipments_has_Rocks intersection table for each rock shipped
INSERT INTO Shipments_has_Rocks (shipmentID, rockID)
VALUES ((SELECT shipmentID
        FROM Shipments
        WHERE shipOrigin = :shipOrigin_in_form
          AND shipDest = :shipDest_in_form
          AND shipDate = :shipDate_in_form
          AND miscNote IS NULL),
        (SELECT rockID FROM Rocks WHERE name = :name_from_dropdown_input));

-- CREATE II
-- Not NULL miscNote
-- Part I: check for duplicate entry (cannot have duplicate Shipments)
SELECT COUNT(shipmentID) AS count FROM Shipments
    WHERE shipOrigin = shipOriginInput
    AND shipDest = :shipDestInput
    AND shipDate = :shipDateInput
    AND miscNote = :miscNoteInput;

-- Part II: insert new row in Shipments
INSERT INTO Shipments (userID, shipOrigin, shipDest, shipDate, miscNote)
VALUES (SELECT address FROM Users WHERE CONCAT(firstName, ' ', lastName) = :auto_populates_from_name_dropdown_input,
        SELECT userID FROM Users WHERE CONCAT(firstName, ' ', lastName) = :name_from_dropdown_input,
        shipDest = :shipDestInput,
        shipDate = :shipDateInput,
        miscNote = :miscNoteInput);

-- Part III: insert new row in Shipments_has_Rocks intersection table for each rock shipped
INSERT INTO Shipments_has_Rocks (shipmentID, rockID)
VALUES ((SELECT shipmentID
        FROM Shipments
        WHERE shipOrigin = :shipOrigin_in_form
          AND shipDest = :shipDest_in_form
          AND shipDate = :shipDate_in_form
          AND miscNote = :miscNote_in_form),
        (SELECT rockID FROM Rocks WHERE name = :name_from_dropdown_input));


-- READ I
-- with user friendly AS labels
-- get all Shipments for the browse Shipments table
SELECT Shipments.shipmentID                         AS 'Shipment Number',
       CONCAT(Users.firstName, ' ', Users.lastName) AS 'User',
       Shipments.shipOrigin                         AS 'Origin',
       Shipments.shipDest                           AS 'Destination',
       Shipments.shipDate                           AS 'Date Shipped',
       Shipments.miscNote                           AS 'Notes'
       FROM Shipments
            INNER JOIN Users
                ON Shipments.userID = Users.userID;

-- READ II
-- for server side /edit_shipment
-- get all Shipments for the browse Shipments table
SELECT Shipments.shipmentID,
    CONCAT(Users.firstName, ' ', Users.lastName),
    Shipments.shipOrigin,
    Shipments.shipDest,
    Shipments.shipDate,
    Shipments.miscNote
    FROM Shipments
        INNER JOIN Users
            ON Shipments.userID = Users.userID
    WHERE Shipments.shipmentID = :shipmentIDInput;

-- display rocks by name
SELECT name
FROM Rocks;

-- display users by full name
SELECT CONCAT(firstName, ' ', lastName)
FROM Users;

-- display shipment by ID
SELECT shipmentID
FROM Shipments;

-- display Rocks with Owner's name for specific shipment
SELECT Shipments_has_Rocks.shipmentHasRockID,
                            CONCAT(Users.firstName, ' ', Users.lastName) AS 'Owner',
                            Rocks.name AS 'Rock Name'
                            From Shipments_has_Rocks
                                INNER JOIN Shipments
                                    ON Shipments_has_Rocks.shipmentID = Shipments.shipmentID
                                INNER JOIN Rocks
                                    ON Shipments_has_Rocks.rockID = Rocks.rockID
                                LEFT JOIN Users
                                    ON Rocks.userID = Users.userID
                            WHERE Shipments_has_Rocks.shipmentID = :shipmentIDInput;

-- display Rocks with Owner's name for all BUT a specific shipment
SELECT Rocks.name AS rock
    FROM Rocks
        WHERE rockID NOT IN (SELECT rockID FROM Shipments_has_Rocks WHERE shipmentID = :shipmentIDInput);

-- display Users BESIDES the User in the Shipment
SELECT CONCAT(firstName, ' ', lastName) AS name
    FROM Users
        WHERE userID != (SELECT userID from Shipments WHERE shipmentID = %s)
            GROUP BY name;

-- display User from Shipment
SELECT CONCAT(firstName, ' ', lastName) AS name
    FROM Users
        WHERE userID = (SELECT userID from Shipments WHERE shipmentID = :shipmentIDInput;

-- UPDATE '/edit_shipment'
-- update Shipment from form data
-- first, get Shipment and Shipments_has_Rocks
SELECT Shipments.shipmentID AS 'Shipment Number',
                                CONCAT(Users.firstName, ' ', Users.lastName) AS 'User',
                                Shipments.shipOrigin AS 'Origin',
                                Shipments.shipDest AS 'Destination',
                                Shipments.shipDate AS 'Date Shipped',
                                Shipments.miscNote AS 'Notes'
                                FROM Shipments
                                    INNER JOIN Users
                                        ON Shipments.userID = Users.userID
                                WHERE Shipments.shipmentID = :shipmentIDInput;
-- then, update Shipment
UPDATE Shipments
SET name       = :userID_from_dropdown_input,
    rock       = :rockID_from_rock_input,
    shipOrigin = :shipOriginInput,
    shipDest   = :shipDestInput,
    shipDate   = :shipDateInput,
    miscNote   = :miscNoteInput
WHERE shipmentID = :shipmentID_selected_in_form;


-- DELETE I
-- delete a Shipment from form data
-- also deletes records with matching shipmentID from Shipments_has_Rocks
-- because of ON DELETE CASCADE operation under shipmentID FK CONSTRAINT
DELETE
FROM Shipments
WHERE shipmentID = :shipmentID_from_browse_shipment_page;

-- DELETE II
-- delete a rock from a Shipment
DELETE
FROM Shipments_has_Rocks
WHERE rockID = :rockID_from_browse_shipment_page;
-- check Shipment to see if last Rock was removed
SELECT COUNT(shipmentID) AS count
    FROM Shipments_has_Rocks
    WHERE shipmentHasRockID = :shipmentHasRockID_from_browse_shipment_page;
-- if empty set is returned, browser runs DELETE I as well

-- get Rock name to use in popup for notifying user rock has been removed.
SELECT Rocks.name AS Rock
    FROM Rocks
        INNER JOIN Shipments_has_Rocks
            ON Rocks.rockID = Shipments_has_Rocks.rockID
    WHERE shipmentHasRockID = :shipmentHasRockID_from_browse_shipment_page;
