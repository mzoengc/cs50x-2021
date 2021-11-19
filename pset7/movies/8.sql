SELECT people.name FROM people
JOIN stars ON stars.person_id = people.id
WHERE stars.movie_id IN (SELECT id FROM movies WHERE title = "Toy Story");