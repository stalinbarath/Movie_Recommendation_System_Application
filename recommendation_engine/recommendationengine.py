import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

from recommendation.models import Movie, Rating

class TriggerRecommendationEngine:

    def __init__(self, movie_name):
        self.movie_name = movie_name.title() #title() converts string to camel case
    
    def get_movie_recommendation(self, movie_data, final_dataset, csr_data, knn):
    
        n_movies_to_recommend = 10
        movie_list = movie_data[movie_data['title'].str.contains(self.movie_name)]
        
        if len(movie_list):
            
            #Get index of the first movie in movie_list
            movie_idx= movie_list.iloc[0]['movieId']
            #Get index of the final_dataset with movie_idx
            movie_idx = final_dataset[final_dataset['movieId'] == movie_idx].index[0]
            
            distances , indices = knn.kneighbors(csr_data[movie_idx],n_neighbors=n_movies_to_recommend+1)    
            
            rec_movie_indices = sorted(list(zip(indices.squeeze().tolist(),distances.squeeze().tolist())),key=lambda x: x[1])[:0:-1]
            
            recommend_frame = []
            for val in rec_movie_indices:
                movie_idx = final_dataset.iloc[val[0]]['movieId']
                idx = movie_data[movie_data['movieId'] == movie_idx].index
                recommend_frame.append({'Title':movie_data.iloc[idx]['title'].values[0],'Distance':val[1]})
            
            df = pd.DataFrame(recommend_frame,index=range(1,n_movies_to_recommend+1))
            
            return df
        
        else:
            return "No movies found. Please check your input"

    def trigger(self):

        movie_data_queryset = Movie.objects.all()
        rating_data_queryset = Rating.objects.all()

        movie_data = pd.DataFrame(list(movie_data_queryset.values()))
        rating_data = pd.DataFrame(list(rating_data_queryset.values()))

        final_dataset = rating_data.pivot(index='movieId', columns='userId', values='rating')
        final_dataset.fillna(0, inplace=True)

        no_movies_voted = rating_data.groupby('userId')['movieId'].agg('count')
        no_users_voted = rating_data.groupby('movieId')['userId'].agg('count')

        final_dataset = final_dataset.loc[no_users_voted[no_users_voted > 10].index,:]
        final_dataset = final_dataset.loc[:,no_movies_voted[no_movies_voted > 50].index]
        final_dataset.reset_index(inplace=True)

        csr_data = csr_matrix(final_dataset.values)

        knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
        knn.fit(csr_data)

        final_df = self.get_movie_recommendation(movie_data, final_dataset, csr_data, knn)

        return final_df