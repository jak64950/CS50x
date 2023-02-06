SELECT DISTINCT name FROM people
 INNER JOIN stars ON person_id = people.id
 WHERE movie_id IN (
SELECT movie_id FROM stars
 WHERE person_id IN (
SELECT id FROM people
 WHERE name = "Kevin Bacon"))
   AND name != "Kevin Bacon";