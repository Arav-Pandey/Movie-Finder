import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MOVIE_API_KEY")

def get_movie_by_title(title, year=None):
    params = {
        "apikey":API_KEY,
        "t":title,
        "plot": "full"
    }
    if year:
        params["y"] = year # Add the year parameter if applied

    res = requests.get("http://www.omdbapi.com/", params=params)
    if res.status_code == 200:
        return res.json()
    return None

def search_movies(keyword):
    params= {
        "apikey": API_KEY,
        "s":keyword
    }
    res = requests.get("http://www.omdbapi.com/", params=params)
    data = res.json()
    if res.status_code == 200:
        if data.get("Response") == "True":
            return {"status": "Good", "data": data.get("Search", [])}
        return {"status": "Bad", "data": data.get("Error")}

    return {"status": "Bad", "data": data.get("Error")}

def search_movies_by_rating(keyword, rating, genres, years):
    params = {
        "apikey": API_KEY, 
        "s": keyword
    }
    res = requests.get("http://www.omdbapi.com/", params=params)
    data = res.json()

    if res.status_code == 200 and data.get("Response") == "True":
        movies = []
        for movie in data.get("Search", []):
            # Fetch full details for each result to get the MPA rating
            details = get_movie_by_title(movie["Title"])
            if details:
                movie_rating = details.get("Rated")
                movie_genres = details.get("Genre", "")   # "Action, Adventure, Sci-Fi"
                movie_year = details.get("Year", "")       # "2005"

                rating_match = movie_rating in rating
                # Check if ANY of the selected genres appear in the movie's genre string
                genre_match = any(g in movie_genres for g in genres)
                # Convert year to int to match numpy int from years array
                year_match = int(movie_year) in years if movie_year.isdigit() else False

                if rating_match and genre_match and year_match:
                    movies.append(details)
        
        if movies:
            return {"status": "Good", "data": movies}
        return {"status": "Bad", "data": f"No movies found with those filters{rating} + {genres}"}

    return {"status": "Bad", "data": data.get("Error")}