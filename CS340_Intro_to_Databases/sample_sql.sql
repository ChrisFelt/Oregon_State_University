-- sample excerpts of potentially useful SQL statements

-- bind the count of duplicates in shipmentID as an additional column WITHOUT grouping rows
SELECT Shipments_has_Rocks.shipmentHasRockID, Shipments_has_Rocks.shipmentID, Shipments_has_Rocks.rockID, temp.numRock
    FROM Shipments_has_Rocks
        INNER JOIN (SELECT Shipments_has_Rocks.shipmentID, COUNT(Shipments_has_Rocks.shipmentID) AS numRock
        FROM Shipments_has_Rocks GROUP BY Shipments_has_Rocks.shipmentID) AS temp
            ON Shipments_has_Rocks.shipmentID = temp.shipmentID
