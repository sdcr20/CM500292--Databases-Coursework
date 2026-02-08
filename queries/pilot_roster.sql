SELECT pilot_id AS "Pilot ID", 
pilot.name AS "Name", 
pilot.licence_number AS "Licence Number",
destination.name AS "Base Airport",
rating.rating_name AS "Aircraft Rating", 
last_medical_date AS "Last Medical"
FROM pilot
JOIN destination ON pilot.base_id = destination.destination_id
JOIN rating ON pilot.aircraft_rating = rating.rating_code
ORDER BY pilot.pilot_id ASC;