SELECT flight.flight_number AS "Flight Number", dep.name AS "Departure Airport", arr.name AS "Arrival Airport", flight.departure_time_utc AS "Departure Time UTC", flight.arrival_time_utc AS "Arrival Time UTC", printf('%d:%02d', flight.flight_duration_minutes / 60, flight.flight_duration_minutes % 60) AS "Flight Duration"
FROM flight
JOIN destination AS dep ON flight.departure_id = dep.destination_id
JOIN destination AS arr ON flight.arrival_id = arr.destination_id
ORDER BY flight.flight_id ASC;
