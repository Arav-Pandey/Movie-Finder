import streamlit as st
from calculations import search_movies, search_movies_by_rating, get_movie_by_title
import numpy as np
import datetime

def main():
    st.set_page_config(page_title="Movie Finder", page_icon="🎞️", layout="centered")
    st.title("Movie Finder")

    st.header("Search For Movies With A Keyword")
    search = st.text_input("Search Here",placeholder="Abc...", key=1)

    if search:
        res = search_movies(search)
        if res["status"] == "Good":
            st.write("Successful Find!")
        else:
            st.write("Error Found")

        for index in range(len(res["data"])):
            st.write(f"**{res["data"][index]["Title"]}** ({res["data"][index]["Year"]})")
            
            if res["data"][index]["Poster"] != "N/A":
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image(res["data"][index]["Poster"])
    
    st.header("Search For A Specific Movie")
    movie = st.text_input("Search Here",placeholder="Batman",key=2)

    if movie:
        res = get_movie_by_title(movie)

        if res != None:
            st.write("Successful Find!")

           
            st.write(f"**{res["Title"]}** ({res["Released"]})")
            
            col1, col2, col3 = st.columns(3)

            with col1:
                st.write(f"MPA Rating: {res["Rated"]}")
            with col2:
                st.write(f"Duration: {res["Runtime"]}")
            with col3:
                st.write(f"Genre: {res["Genre"]}")
            
            if res["Poster"] != "N/A":
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image(res["Poster"])
            st.write(res["Plot"])
        
        else:
            st.write("Error Found")
        
    MPA_ORDER = ["G", "PG", "PG-13", "R", "NC-17", "NR", "N/A"]
    GENRES = ["Action","Adventure", "AnimationBiography", "Comedy", "CrimeDocumentary", "Drama", "FamilyFantasy", "Film-Noir", "HistoryHorror", "Music", "MusicalMystery", "Romance", "Sci-FiShort", "Sport", "ThrillerWar", "Western"]
    current_year = datetime.date.today().year
    years_array = np.arange(1894,current_year + 1)

    st.header("Filter Movies")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        filter = st.text_input("Search Here", placeholder="Abc...", key=3)
    with col2:
        rated = st.multiselect("Choose MPA Rating(s)", MPA_ORDER, default=["PG-13"])
    with col3:
        genres = st.multiselect("Choose Genre(s)", GENRES, default=["Action"])
    with col4:
        years = st.multiselect("Choose the release year(s)",years_array, default=[current_year])

    if filter and rated and genres and years:
        res = search_movies_by_rating(filter,rated,genres,years)

        if res["status"] == "Good":
            st.write("Successful Find!")

            for movie in res["data"]:
                st.write(f"**{movie["Title"]}** ({movie["Released"]})")
            
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.write(f"MPA Rating: {movie["Rated"]}")
                with col2:
                    st.write(f"Duration: {movie["Runtime"]}")
                with col3:
                    st.write(f"Genre: {movie["Genre"]}")
            
            if movie["Poster"] != "N/A":
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image(movie["Poster"])
            st.write(movie["Plot"])
        else:
            st.write(f"Error Found: {res["data"]}")


if __name__ == "__main__":
    main()