import pandas as pd
import streamlit as st
import pickle
import requests
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
def fetch_poster(movie_id):
    responses = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=f513adf52ad2106eb3519c383032167e'.format(movie_id))
    data = responses.json()
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        #fetch the poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies, recommended_movies_posters

st.title('Movie Recommender System')
selected_movie_name = st.selectbox(
    'select the movie for which you want recommendations'
   ,movies['title'].values)
if st.button("recommend"):
    names, recommendations = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(recommendations[0])

    with col2:
        st.text(names[1])
        st.image(recommendations[1])

    with (col3):
        st.text(names[2])
        st.image(recommendations[2])
    with col4:
        st.text(names[3])
        st.image(recommendations[3])
    with col5:
        st.text(names[4])
        st.image(recommendations[4])