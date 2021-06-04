import requests_with_caching
import json


def get_movies_from_tastedive(name):
    """
    It should take one input parameter, a string that is the name of a movie or music artist.
    The function should return the 5 TasteDive results that are associated with that string;
    be sure to only get movies, not other kinds of media.
    It will be a python dictionary with just one key, 'Similar'.
    """
    base_url = 'https://tastedive.com/api/similar'
    d = {'q': name, 'type': 'movies', 'limit': 5}
    response = requests_with_caching.get(base_url, params=d)
    return json.loads(response)


def extract_movie_titles(data):
    """
    A function that extracts just the list of movie titles from a dictionary
    returned by get_movies_from_tastedive.
    """
    return [d['Name'] for d in data['Similar']['Results']]


def get_related_titles(movie_titles):
    """
    It takes a list of movie titles as input. It gets five related movies for each from TasteDive,
    extracts the titles for all of them, and combines them all into a single list.
    Don’t include the same movie twice.
    """
    movie_list_res = []
    for title in movie_titles:
        lst = extract_movie_titles(get_movies_from_tastedive(title))
        movie_list_res.extend(lst)
    return list(set(movie_list_res))


def get_movie_data(title):
    """
    It takes in one parameter which is a string that should represent the title of a movie you want to search.
    The function should return a dictionary with information about that movie.
    """
    apikey_val = ''
    base_url = 'http://www.omdbapi.com/'
    d = {'t': title, 'r': 'json', 'apikey': apikey_val}
    response = requests_with_caching.get(base_url, params=d)
    return json.loads(response)


def get_movie_rating(omdb_dict):
    """
    It takes an OMDB dictionary result for one movie and extracts the Rotten Tomatoes rating as an integer.
    For example, if given the OMDB dictionary for “Black Panther”, it would return 97.
    If there is no Rotten Tomatoes rating, return 0.
    """
    ratings = omdb_dict['Ratings']
    r = [d['Value'] for d in ratings if d['Source'] == 'Rotten Tomatoes']
    for d in ratings:
        if d['Source'] == 'Rotten Tomatoes':
            return int(d['Value'][:-1])
    return 0
            

def get_sorted_recommendations(movies):
    """
    It takes a list of movie titles as an input.
    It returns a sorted list of related movie titles as output, up to five related movies for each input movie title.
    The movies should be sorted in descending order by their Rotten Tomatoes rating, as returned by the get_movie_rating function.
    Break ties in reverse alphabetic order, so that ‘Yahşi Batı’ comes before ‘Eyyvah Eyvah’.
    """
    lst = get_related_titles(movies)
    res = {}
    for movie in lst:
        res[movie] = get_movie_rating(get_movie_data(movie))
    return [el[0] for el in sorted(res.items(), key=lambda x: (x[1], x[0]), reverse=True)]


# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
if __name__ == '__main__':
    get_movies_from_tastedive("Bridesmaids")
    get_movies_from_tastedive("Black Panther")

    extract_movie_titles(get_movies_from_tastedive("Tony Bennett"))
    extract_movie_titles(get_movies_from_tastedive("Black Panther"))

    get_related_titles(["Black Panther", "Captain Marvel"])
    get_related_titles([])

    get_movie_data("Venom")
    get_movie_data("Baby Mama")

    get_movie_rating(get_movie_data("Deadpool 2"))

    print(get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"]))
