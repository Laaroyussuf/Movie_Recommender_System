#Importing Libraries
import streamlit as st
import pandas as pd
import numpy as np
import pickle
from random import shuffle

#Loading Files
user_item = pd.read_pickle(open('user_item.pkl', 'rb'))
user_similarity = pd.read_pickle(open('user_similarity.pkl', 'rb'))
item_tag = pd.read_pickle(open('item_tag.pkl', 'rb'))
title_poster_path = pd.read_pickle(open('title_poster_path.pkl', 'rb'))

# Load each split file and concatenate them back together
splits = []
for i in range(21):
    with open(f'split_{i}.pkl', 'rb') as f:
        split = pd.read_pickle(f)
        splits.append(split)
data = np.concatenate(splits, axis=0)
similarity = data


#Functions

##For getting movie poster url
def get_poster_url(movie_list):
    poster_url_list = []
    for movie in movie_list:
        poster_url = title_poster_path[title_poster_path.Recommendation == movie]['poster_path'].values[0]
        poster_url_list.append(poster_url)
    return poster_url_list

##For item(Movie) based recommendation
def movie_based_recommendation(movie):
    item_based_rec = []
    mov_index = item_tag[item_tag.title == movie].index[0]
    distance  =  similarity[mov_index]
    
    #First 20 similar movies excluding the target itself
    movie_list = sorted(list(enumerate(distance)), key= lambda x: x[1], reverse= True)[1:6] 
    
    for i in movie_list:
        mov_title = item_tag[item_tag.index ==i[0]]['title'].values[0] 
        item_based_rec.append(mov_title)
    return item_based_rec

def user_based_recommendation(userId):
    similar_users = sorted(list(enumerate(user_similarity[userId - 1])), key=lambda x: x[1], reverse=True)
    recommendations = []
    item_index = user_item.loc[userId]
    unrated_movie = item_index[item_index == 0].index.to_list() #Movies which user has no interaction with
    # Recommend the top-rated movies from similar users
    for user, similarity_score in similar_users[1:4]:  #The first 3 similar users excluding the target user
        user = user + 1
        user_movies = user_item.loc[user]
        recommended_movies = user_movies[user_movies > 2].index.to_list() #Any movie rated above 2 by the similar users
        for movie in recommended_movies:
            recommendations.append(movie)
    recommendations = list(set(recommendations))
    rec_mov = [x for x in unrated_movie if x in recommendations]
    return rec_mov

def recommend_movie(id, title):
    user_based = user_based_recommendation(userId=id)
    movie_based = movie_based_recommendation(movie=title)
    final_rec = [x for x in user_based if x in movie_based] #Prioritizing intersecting movie
    if final_rec == []:
        #If there's no intersection
        user_fin = user_based[:5]
        mov_fin = movie_based[:5]
        final_rec = user_fin + mov_fin
        shuffle(final_rec)
        return final_rec
    else:
        #If there is an intersection 
        final_rec = final_rec + [x for x in user_based if x not in movie_based]
        return final_rec[:10]

def show_result(title, poster):
    for ind, col in enumerate(st.columns(5)):
        with col:
            st.text(title[ind])
            st.image(poster[ind])


#Popular movies
st.header('Movie Recommendation System')
st.markdown('**Popular Movies (recent till 2020)**')
top_5 = title_poster_path.Recommendation.values[:5]
show_result(top_5, title_poster_path.poster_path.values)
# col1, col2, col3, col4, col5 = st.columns(5)
# with col1:
#     st.text(top_5[0])
#     st.image(title_poster_path.poster_path.values[0])
# with col2:
#     st.text(top_5[1])
#     st.image(title_poster_path.poster_path.values[1])
# with col3:
#     st.text(top_5[2])
#     st.image(title_poster_path.poster_path.values[2])
# with col4:
#     st.text(top_5[3])
#     st.image(title_poster_path.poster_path.values[3])
# with col5:
#     st.text(top_5[4])
#     st.image(title_poster_path.poster_path.values[4])




#Similar Movie recommendation
st.header('Similar Movie Recommendation')
selected_movies = st.selectbox('Select a movie you want recommendation for', item_tag.title.values)
if st.button('Recommend'):
    mov_result = movie_based_recommendation(selected_movies)
    poster_urls = get_poster_url(mov_result)
    show_result(mov_result, poster_urls)
    # col1, col2, col3, col4, col5 = st.columns(5)
    # with col1:
    #     st.text(mov_result[0])
    #     st.image(poster_urls[0])
    # with col2:
    #     st.text(mov_result[1])
    #     st.image(poster_urls[1])
    # with col3:
    #     st.text(mov_result[2])
    #     st.image(poster_urls[2])
    # with col4:
    #     st.text(mov_result[3])
    #     st.image(poster_urls[3])
    # with col5:
    #     st.text(mov_result[4])
    #     st.image(poster_urls[4])



st.header('Movie Recommendation for User')
user_ids = user_item.index.tolist()
col1, col2 = st.columns(2)
with col1:
    input1 = st.selectbox('Select your User ID', user_ids)
with col2:
    input2 = st.selectbox('Select a movie to get recommendation', item_tag.title.values)
if st.button("Get Movies Recommendation"):
    mov_result = recommend_movie(id=input1, title=input2)
    poster_urls = get_poster_url(mov_result)
    show_result(mov_result, poster_urls)
    # col1, col2, col3, col4, col5 = st.columns(5)
    # with col1:
    #     st.text(mov_result[0])
    #     st.image(poster_urls[0])
    # with col2:
    #     st.text(mov_result[1])
    #     st.image(poster_urls[1])
    # with col3:
    #     st.text(mov_result[2])
    #     st.image(poster_urls[2])
    # with col4:
    #     st.text(mov_result[3])
    #     st.image(poster_urls[3])
    # with col5:
    #     st.text(mov_result[4])
    #     st.image(poster_urls[4])
