-- Query to determine the average rating of all movies released in 2012
SELECT AVG(rating) FROM ratings JOIN movies on ratings.movie_id = movies.id WHERE year = 2012;