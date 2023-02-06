SELECT DISTINCT name FROM people
 INNER JOIN directors ON person_id = id
 INNER JOIN ratings ON ratings.movie_id = directors.movie_id
 WHERE rating >= 9.0;