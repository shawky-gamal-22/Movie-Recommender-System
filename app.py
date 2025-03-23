import streamlit as st
import requests
import streamlit.components.v1 as components

import pickle

st.header('Movie Recommender System')

# API URL
FASTAPI_URL = "http://127.0.0.1:8000/recommend/"  # Change this when hosting

# Fetch movie list (from pickle)
movies = pickle.load(open('engines/movies_list.pkl', 'rb'))
movies_list = movies['title'].values

# Movie carousel
imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")
imageCarouselComponent(imageUrls=[
    "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
    "https://image.tmdb.org/t/p/w500/6ELJEzQJ3Y45HczvreC3dg0GV5R.jpg",
    "https://image.tmdb.org/t/p/w500/9O7gLzmreU0nGkIB6K3BsJbzvNv.jpg",
    "https://image.tmdb.org/t/p/w500/7WsyChQLEftFiDOVTGkv3hFpyyt.jpg",
    "https://image.tmdb.org/t/p/w500/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg",
    "https://image.tmdb.org/t/p/w500/5KCVkau1HEl7ZzfPsKAPM0sMiKc.jpg",
    "https://image.tmdb.org/t/p/w500/3iYQTLGoy7QnjcUYRJy4YrAgGvp.jpg",
    "https://image.tmdb.org/t/p/w500/4q2NNj4S5dG2RLF9CpXsej7yXl.jpg"
], height=200)

# Movie selection dropdown
select_value = st.selectbox('Select a movie', movies_list)

if st.button("Show Recommendation"):
    response = requests.get(FASTAPI_URL, params={"movie": select_value})
    
    if response.status_code == 200:
        data = response.json()
        if "error" in data:
            st.error("Movie not found!")
        else:
            movies_names = data["movies"]
            movie_poster = data["posters"]

            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.text(movies_names[0])
                st.image(movie_poster[0])
            with col2:
                st.text(movies_names[1])
                st.image(movie_poster[1])
            with col3:
                st.text(movies_names[2])
                st.image(movie_poster[2])
            with col4:
                st.text(movies_names[3])
                st.image(movie_poster[3])
            with col5:
                st.text(movies_names[4])
                st.image(movie_poster[4])
    else:
        st.error("Error fetching recommendations!")
