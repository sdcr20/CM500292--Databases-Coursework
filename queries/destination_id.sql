SELECT destination.destination_id AS "Destination ID", 
destination.name AS "Airport Name",
destination.city AS "City",
destination.country AS "Country",
timezone.acronym AS "Timezone"
FROM destination
JOIN timezone ON destination.timezone = timezone.code
WHERE destination_id = ?;