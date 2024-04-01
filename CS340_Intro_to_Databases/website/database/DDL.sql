-- CS 340 Intro to Databases
-- Project Step 2 Draft: DDL
-- Team Rock Bottom
-- Members: Robert Behring and Christopher Felt
-- Modified from MySQL Workbench Forward Engineering


SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

-- #####################################################
-- TABLE PARAMETERS
-- #####################################################

-- -----------------------------------------------------
-- Table Users
-- -----------------------------------------------------
CREATE OR REPLACE TABLE Users (
  userID INT NOT NULL AUTO_INCREMENT UNIQUE,
  firstName VARCHAR(75) NOT NULL,
  lastName VARCHAR(75) NOT NULL,
  address VARCHAR(155) NOT NULL,
  specialization VARCHAR(155) NULL,
  bio VARCHAR(3000) NULL,
  CONSTRAINT full_name_Users1
    UNIQUE (firstName, lastName),
  PRIMARY KEY (userID));


-- -----------------------------------------------------
-- Table Rocks
-- -----------------------------------------------------
CREATE OR REPLACE TABLE Rocks (
  rockID INT NOT NULL AUTO_INCREMENT UNIQUE,
  userID INT NOT NULL,
  name VARCHAR(75) NOT NULL UNIQUE, -- Rock names are unique
  geoOrigin VARCHAR(155) NOT NULL,
  type VARCHAR(75) NOT NULL,
  description VARCHAR(255) NOT NULL,
  chemicalComp VARCHAR(155) NOT NULL,
  PRIMARY KEY (rockID),
  CONSTRAINT fk_Rocks_Users1
    FOREIGN KEY (userID)
    REFERENCES Users (userID)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table Reviews
-- -----------------------------------------------------
CREATE OR REPLACE TABLE Reviews (
  reviewID INT NOT NULL AUTO_INCREMENT UNIQUE,
  userID INT NULL, -- userID can be removed
  rockID INT NOT NULL,
  title VARCHAR(75) NOT NULL,
  body VARCHAR(3000) NOT NULL,
  rating TINYINT(1) UNSIGNED NOT NULL,
  PRIMARY KEY (reviewID),
  CONSTRAINT fk_Reviews_Users1
    FOREIGN KEY (userID)
    REFERENCES Users (userID)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION,
  CONSTRAINT fk_Reviews_Rocks1
    FOREIGN KEY (rockID)
    REFERENCES Rocks (rockID)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table Shipments
-- -----------------------------------------------------
CREATE OR REPLACE TABLE Shipments (
  shipmentID INT NOT NULL AUTO_INCREMENT UNIQUE,
  userID INT NOT NULL,
  shipOrigin VARCHAR(255) NOT NULL,
  shipDest VARCHAR(255) NOT NULL,
  shipDate DATE NOT NULL,
  miscNote VARCHAR(3000) NULL,
  PRIMARY KEY (shipmentID),
  CONSTRAINT fk_Shipments_Users1
    FOREIGN KEY (userID)
    REFERENCES Users (userID)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table Shipments_has_Rocks
-- -----------------------------------------------------
CREATE OR REPLACE TABLE Shipments_has_Rocks (
  shipmentHasRockID INT NOT NULL AUTO_INCREMENT UNIQUE,
  shipmentID INT NOT NULL,
  rockID INT NOT NULL,
  PRIMARY KEY (shipmentHasRockID),
  -- combination of shipmentID and rockID FKs must always be unique
  CONSTRAINT fk_shipmentID_and_rockID_unique
    UNIQUE (shipmentID, rockID),
  CONSTRAINT fk_Shipments_has_Rocks_Shipments1
    FOREIGN KEY (shipmentID)
    REFERENCES Shipments (shipmentID)
    ON DELETE CASCADE  -- delete Shipments_has_Rocks when Shipment with matching shipmentID is deleted
    ON UPDATE NO ACTION,
  CONSTRAINT fk_Shipments_has_Rocks_Rocks1
    FOREIGN KEY (rockID)
    REFERENCES Rocks (rockID)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION);


-- #####################################################
-- INSERT QUERIES
-- #####################################################

-- -----------------------------------------------------
-- Table Users
-- -----------------------------------------------------
INSERT INTO Users (
    firstName,
    lastName,
    address,
    specialization,
    bio
)
VALUES (
    'Ricky',
    'McFarley',
    '101 Sedimentary Way, New York City, NY 10001',
    NULL,
    NULL
), (
    'Bobby',
    'James',
    '6000 Metamorphic Drive, Rock City, NM 87311 USA',
    'Gem Cutter',
    NULL
), (
    'Alice',
    'Liddel',
    '1 Igneous Court, Sydney, NSW 2000 Australia',
    'Amateur Rockhound',
    NULL
), (
    'Jimothy',
    'Riley',
    'Riley Castle Way, London, W1D 3AF United Kingdom',
    'Mineral Photographer',
    "I've spent the last 23 years photographing priceless rocks all across the UK and US."
);

-- -----------------------------------------------------
-- Table Rocks
-- -----------------------------------------------------
INSERT INTO Rocks (
    userID,
    name,
    geoOrigin,
    type,
    description,
    chemicalComp
)
VALUES (
    (SELECT userID FROM Users WHERE firstName='Alice' AND lastName='Liddel'),
    'The One Rock',
    'Mt. Ruapehu, New Zealand',
    'Igneous',
    'Vastly superior to rocks that suffer from any form of plurality.',
    'KALSi3O8'
), (
    (SELECT userID FROM Users WHERE firstName='Jimothy' AND lastName='Riley'),
    'Old Man of the Mountain',
    'White Mountains, USA',
    'Igneous',
    'Shard from the OG.',
    'SiO2'
), (
    (SELECT userID FROM Users WHERE firstName='Bobby' AND lastName='James'),
    'Scarlet',
    'Wah Wah Mountains, USA',
    'Metamorphic',
    'Uncut red beryl in original rhyolite matrix. So shiny.',
    'Be3Al2Si6O18 + Mn'
), (
    (SELECT userID FROM Users WHERE firstName='Bobby' AND lastName='James'),
    'Rocky',
    'K2, Pakistan',
    'Igneous',
    'My little blue buddy',
    'SiO2 + Cu3(CO3)2(OH)2'
);

-- -----------------------------------------------------
-- Table Reviews
-- -----------------------------------------------------
INSERT INTO Reviews (
    userID,
    rockID,
    title,
    body,
    rating
)
VALUES (
    (SELECT userID FROM Users WHERE firstName='Ricky' AND lastName='McFarley'),
    (SELECT rockID FROM Rocks WHERE name='Scarlet'),
    'not so good rock',
    "too shiny, didn't like it. ",
    2
), (
    (SELECT userID FROM Users WHERE firstName='Bobby' AND lastName='James'),
    (SELECT rockID FROM Rocks WHERE name='The One Rock'),
    'WOW THAT CRYSTAL STRUCTURE THO',
    'I cut it and ground it down into a thin section just so I could see the FANTASTIC twinning structure of the K-spar crystals under a microscope - THREE DAYS OF ROCK GRINDING WELL SPENT.',
    5
), (
    (SELECT userID FROM Users WHERE firstName='Alice' AND lastName='Liddel'),
    (SELECT rockID FROM Rocks WHERE name='Old Man of the Mountain'),
    'meh',
    "Kind of your average, middle of the road rock. Honestly I'm not sure what the individual who sent this in was thinking.",
    3
), (
    (SELECT userID FROM Users WHERE firstName='Jimothy' AND lastName='Riley'),
    (SELECT rockID FROM Rocks WHERE name='Rocky'),
    'Nope',
    'Not nearly as good as my rock, which is the best rock.',
    1
);

-- -----------------------------------------------------
-- Table Shipments
-- -----------------------------------------------------
INSERT INTO Shipments (
    userID,
    shipOrigin,
    shipDest,
    shipDate,
    miscNote
)
VALUES (
    (SELECT userID FROM Users WHERE firstName='Alice' AND lastName='Liddel'),
    'YouBreccia Way 71, Ramersberg 6060 Switzerland',
    '1 Igneous Court, Sydney, NSW 2000 Australia',
    '2022-11-08',
    'VIP, HANDLE WITH CARE'
), (
    (SELECT userID FROM Users WHERE firstName='Jimothy' AND lastName='Riley'),
    'YouBreccia Way 71, Ramersberg 6060 Switzerland',
    'Riley Castle Way, London, W1D 3AF United Kingdom',
    '2023-07-07',
    'Special delivery instructions by Mr. Riley - leave at portcullis #2.'
), (
    (SELECT userID FROM Users WHERE firstName='Bobby' AND lastName='James'),
    'YouBreccia Way 71, Ramersberg 6060 Switzerland',
    '6000 Metamorphic Drive, Rock City, NM 87311 USA',
    '2023-04-10',
    'User has requested the rock be rolled to its destination'
), (
    (SELECT userID FROM Users WHERE firstName='Ricky' AND lastName='McFarley'),
    '101 Sedimentary Way, New York City, NY 10001',
    'YouBreccia Way 71, Ramersberg 6060 Switzerland',
    '2022-12-24',
    NULL
);

-- -----------------------------------------------------
-- Table Shipments_has_Rocks
-- -----------------------------------------------------
INSERT INTO Shipments_has_Rocks (
    shipmentID,
    rockID
)
VALUES (
    (SELECT shipmentID FROM Shipments
        WHERE shipOrigin='YouBreccia Way 71, Ramersberg 6060 Switzerland'
        AND shipDest='1 Igneous Court, Sydney, NSW 2000 Australia'
        AND shipDate='2022-11-08'),
    (SELECT rockID FROM Rocks WHERE name='Scarlet')
), (
    (SELECT shipmentID FROM Shipments
        WHERE shipOrigin='YouBreccia Way 71, Ramersberg 6060 Switzerland'
        AND shipDest='Riley Castle Way, London, W1D 3AF United Kingdom'
        AND shipDate='2023-07-07'),
    (SELECT rockID FROM Rocks WHERE name='Rocky')
), (
    (SELECT shipmentID FROM Shipments
        WHERE shipOrigin='YouBreccia Way 71, Ramersberg 6060 Switzerland'
        AND shipDest='6000 Metamorphic Drive, Rock City, NM 87311 USA'
        AND shipDate='2023-04-10'),
    (SELECT rockID FROM Rocks WHERE name='The One Rock')
), (
    (SELECT shipmentID FROM Shipments
        WHERE shipOrigin='101 Sedimentary Way, New York City, NY 10001'
        AND shipDest='YouBreccia Way 71, Ramersberg 6060 Switzerland'
        AND shipDate='2022-12-24'),
    (SELECT rockID FROM Rocks WHERE name='Scarlet')
);


SET FOREIGN_KEY_CHECKS=1;
COMMIT;
