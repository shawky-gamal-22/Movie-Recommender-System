import streamlit as st
import pickle 
import requests
import streamlit.components.v1 as components

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=d5bbfef02cf91c2b3c8dabad33c3bb0b&language=en-US".format(movie_id)
    data= requests.get(url)
    data = data.json()
    poster_path= data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path

    return full_path


def  recommender(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distance = sorted(list(enumerate(similarity[movie_index])), reverse= True, key=lambda x: x[1])
    recommended_movies = []
    recommened_poster = []
    for i in distance[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommened_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommened_poster


movies = pickle.load(open('engines/movies_list.pkl', 'rb'))
similarity = pickle.load(open('engines/similarity.pkl', 'rb'))
movies_list = movies['title'].values

st.header('Movie Recommender System')




imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")

imageUrls = [
    fetch_poster(1632),
    fetch_poster(299536),
    fetch_poster(17455),
    fetch_poster(2830),
    fetch_poster(429422),
    fetch_poster(9722),
    fetch_poster(13972),
    fetch_poster(240),
    fetch_poster(155),
    fetch_poster(598),
    fetch_poster(914),
    fetch_poster(255709),
    fetch_poster(572154)
   
    ]
imageCarouselComponent(imageUrls=imageUrls, height=200)
select_value = st.selectbox('Select a movie', movies_list)



if st.button("Show Recommendation"):
    movies_names, movie_poster = recommender(select_value)

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