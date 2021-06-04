# rest_api_make_movie_recommendations

This project take  through the process of mashing up data from two different APIs to make movie recommendations.

The TasteDive API lets you provide a movie (or bands, TV shows, etc.) as a query input, and returns a set of related items.(https://tastedive.com/read/api)

The OMDB API lets to provide a movie title as a query input and get back data about the movie, including scores from various review sites (Rotten Tomatoes, IMDB, etc.).
(https://www.omdbapi.com/)

I use TasteDive to get related movies for a whole list of titles combining the resulting lists of related movies, and sort them according to their Rotten Tomatoes scores (which will require making API calls to the OMDB API.)

