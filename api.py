from fastapi import FastAPI
import pickle 
import requests
from typing import List

app = FastAPI()

movies = pickle.load(open('engines/movies_list.pkl', 'rb'))
similarity = pickle.load(open('engines/similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=d5bbfef02cf91c2b3c8dabad33c3bb0b&language=en-US".format(movie_id)
    data= requests.get(url)
    data = data.json()
    poster_path = data.get('poster_path')
    if not poster_path:
        return ""
    
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def  recommender(movie):
    try:
        movie_index = movies[movies['title']==movie].index[0]
        distance = sorted(list(enumerate(similarity[movie_index])), reverse= True, key=lambda x: x[1])
        recommended_movies = []
        recommened_posters = []
        for i in distance[1:6]:
            movie_id = movies.iloc[i[0]].id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommened_posters.append(fetch_poster(movie_id))
        return {"movies": recommended_movies, "posters": recommened_posters}
    
    except IndexError:
        return {"error": "Movie not found"}



@app.get("/recommend/")
def get_recommendations(movie: str):
    return recommender(movie)




