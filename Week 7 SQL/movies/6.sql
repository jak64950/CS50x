SELECT AVG(rating) FROM ratings
 INNER JOIN movies ON id = movie_id
 WHERE year = 2012;