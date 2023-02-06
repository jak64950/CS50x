SELECT name FROM people
 INNER JOIN stars ON person_id = people.id
 INNER JOIN movies ON movies.id = movie_id
 WHERE title = "Toy Story";