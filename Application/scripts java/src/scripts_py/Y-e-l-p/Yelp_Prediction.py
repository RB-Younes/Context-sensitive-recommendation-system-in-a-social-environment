import math

import getpass
import pandas as pn
import numpy as np
import matplotlib.pyplot as pl
from matplotlib import gridspec
from keras.models import load_model
from geopy.distance import geodesic
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import time
import argparse
import os


def parse_args():
    u = getpass.getuser()
    parser = argparse.ArgumentParser(description="Prediction Yelp.")
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    parser.add_argument('--friendship_path', nargs='?', default=os.path.join(script_dir, "Y-e-l-p/"),
                        help='Path of friendship values file.')
    parser.add_argument('--test_path', nargs='?', default='C:/users/' + u + '/Desktop/',
                        help='Path of the test set file.')
    parser.add_argument('--model_path', nargs='?', default='C:/users/' + u + '/Desktop/',
                        help='Path of the trained model.')
    parser.add_argument('--users_sample', type=int, default=10,
                        help='sample of users.')
    parser.add_argument('--Choice_model', type=int, default=2,
                        help='Model choice : 1)-HybMLP 2)-MLP.')
    parser.add_argument('--Alpha_combi', type=float, default=0.5,
                        help='Combination ratio.')
    parser.add_argument('--Context_choice', type=int, default=-1,
                        help='Context_choice: "1")- with context "-1")-without context')
    parser.add_argument('--K', type=int, default=1,
                        help='Number of top persons.')
    parser.add_argument('--combination_bool', type=int, default=-1,
                        help='boolean to combine CF/CCF and SocF .')
    parser.add_argument('--distance', type=float, default=20,
                        help='Distance between pertinent item and other items .')
    parser.add_argument('--Mode', type=float, default=1,
                        help='Mode: 1)-Jaccard similarity 2)-Cosine similarity.')
    return parser.parse_args()


# -------------------------------------------------------[Yelp]---------------------------------------------------------
def evaluate_(test):
    hr, ndcg = 0, 0
    i = 1
    for rating in test:
        if rating == 1:
            hr = 1
            ndcg = math.log(2) / math.log(i + 1)
            break
        i = i + 1
    return hr, ndcg


def Context_dis(final, items_set, latitude, longitude, distance):
    co_per_item = "" + str(latitude) + "," + str(longitude) + ""
    result = final
    for index, row in final.iterrows():
        item_id = row['item_id']
        row_item_set = items_set.loc[items_set['item_id'] == item_id]
        x = str(row_item_set['latitude'].values[0])
        y = str(row_item_set['longitude'].values[0])
        co_item = "" + x + "," + y + ""
        calculated_dis = geodesic(co_per_item, co_item).kilometers
        if calculated_dis > distance:
            result = result[result.item_id != item_id]
    return result


def CF_prediction(test, model, user_id):
    test_un_ID = test[test['user_id'] == user_id]
    test_un_ID = test_un_ID.reset_index(drop=True)
    test_userID = test_un_ID['user_id']
    test_itemID = test_un_ID['item_id']

    predictions = model.predict([test_userID, test_itemID], verbose=2)
    predictions = pn.DataFrame(data=predictions, columns=['predicted'])
    predictions = pn.concat([test_un_ID, predictions], axis=1)
    predictions = predictions.sort_values(by=['predicted'], ascending=False)
    RFC_columns = ['item_id', 'rating', 'predicted']
    final_result = predictions[RFC_columns]

    print('CF_prediction', final_result)
    return final_result


def CCF_prediction(test, model, user_id):
    test_un_ID = test[test['user_id'] == user_id]
    test_un_ID = test_un_ID.reset_index(drop=True)
    test_userID = test_un_ID['user_id']
    test_itemID = test_un_ID['item_id']
    test_userDATA = test_un_ID[
        ['fans', 'average_stars', 'friends', 'vote_funny', 'useful', 'vote_cool', 'hot', 'more',
         'profile', 'cute', 'list', 'note', 'plain', 'cool', 'funny', 'writer', 'photos']]
    test_itemDATA = test_un_ID[['latitude', 'longitude', 'Breakfast & Brunch', 'American (Traditional)', 'Burgers',
                                'Fast Food',
                                'American (New)', 'Chinese', 'Pizza', 'Italian', 'Sandwiches', 'Sushi Bars',
                                'Japanese',
                                'Indian', 'Mexican', 'Vietnamese', 'Thai', 'Asian Fusion', 'Take-out', 'Wi-Fi',
                                'dessert', 'latenight', 'lunch', 'dinner', 'breakfast', 'brunch', 'Caters',
                                'Noise Level', 'Takes Reservations', 'Delivery', 'romantic', 'intimate', 'touristy',
                                'hipster', 'divey', 'classy', 'trendy', 'upscale', 'casual',
                                'Parking', 'Has TV', 'Outdoor Seating', 'Attire', 'Alcohol', 'Waiter Service',
                                'Accepts Credit Cards', 'Good for Kids', 'Good For Groups',
                                'Price Range', 'Wheelchair Accessible']]
    predictions = model.predict([test_userID, test_userDATA, test_itemID, test_itemDATA], verbose=2)
    predictions = pn.DataFrame(data=predictions, columns=['predicted'])
    predictions = pn.concat([test_un_ID, predictions], axis=1)
    predictions = predictions.sort_values(by=['predicted'], ascending=False)
    RFC_columns = ['item_id', 'rating', 'predicted']
    final_result = predictions[RFC_columns]

    # add rating column
    test_set_user = test.loc[test['user_id'] == user_id]
    final_result = final_result.assign(rating=0)
    final_result = final_result.reset_index(drop=True)
    pos_row = test_set_user.loc[test_set_user['rating'] == 1]
    final_result.loc[final_result['item_id'] == int(pos_row['item_id']), 'rating'] = 1

    print('CCF_prediction', final_result)
    return final_result


def Cosine_sim(user_id, reviews, user_friends):
    user_friends = user_friends.loc[user_friends['user_id'] == user_id]
    friends_ids = list(user_friends["friend_id"])
    friends_ids.append(user_id)

    reviews_pivot = reviews.pivot(index='user_id', columns='item_id', values='rating_val').replace(np.nan, 0)

    friends_pivot = reviews_pivot.loc[reviews_pivot.index.isin(friends_ids)]

    friends_mat = csr_matrix(friends_pivot.values)
    model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
    model_knn.fit(friends_mat)

    distances, indices = model_knn.kneighbors(
        friends_pivot.loc[friends_pivot.index == user_id].values.reshape(1, -1),
        n_neighbors=len(friends_pivot))
    data = []
    columns = ['user_id', 'friend_id', 'sim']
    for i in range(0, len(distances.flatten())):
        if i != 0:
            data.append([user_id, friends_pivot.index[indices.flatten()[i]], distances.flatten()[i]])
    result = pn.DataFrame(data, columns=columns)
    return result


def Cosine_Jaccard_sim_MLP(friendship, user_id, k, test, Data_items, reviews, user_friends, model, Mode):
    test_set_user = test.loc[test['user_id'] == user_id]
    items_list = list(test_set_user["item_id"])
    items_info = Data_items.loc[Data_items['item_id'].isin(items_list)]
    items_info.reset_index(inplace=True, drop=True)
    if Mode == 1:  # JACCARD SIMILARITY
        friends_deg = friendship.loc[friendship['user_1'] == user_id]
        if len(friends_deg) != 0:
            TOP_friends = friends_deg.sort_values(by='friendship', ascending=False).head(k)
            items_DF = pn.DataFrame(items_list, columns=['item_id'])
            items_list_c = items_DF.copy()
            result = pn.DataFrame(columns=['item_id', 'user_id', 'predicted'])
            for index, row in TOP_friends.iterrows():
                user_items_DF = items_DF.assign(user_id=int(row['user_2']))
                test_userID = user_items_DF['user_id']
                test_itemID = user_items_DF['item_id']
                predictions = model.predict([test_userID, test_itemID], verbose=2)
                predictions = pn.DataFrame(data=predictions, columns=['predicted'])
                predictions = pn.concat([user_items_DF, predictions], axis=1)
                predictions = predictions.sort_values(by=['predicted'], ascending=False)
                result = pn.concat([result, predictions])
                items_DF = items_list_c
            final_result = result.groupby(['item_id'], as_index=False).mean()
            final_result = final_result.sort_values(by=['predicted'], ascending=False)
            return final_result
    else:  # COSINE SIMILARITY
        sort = Cosine_sim(user_id, reviews, user_friends)
        if len(sort) != 0:
            TOP_sorted = sort.head(k)
            items_DF = pn.DataFrame(items_list, columns=['item_id'])
            items_list_c = items_DF.copy()
            result = pn.DataFrame(columns=['item_id', 'user_id', 'predicted'])
            for index, row in TOP_sorted.iterrows():
                user_items_DF = items_DF.assign(user_id=int(row['friend_id']))
                test_userID = user_items_DF['user_id']
                test_itemID = user_items_DF['item_id']
                predictions = model.predict([test_userID, test_itemID], verbose=2)
                predictions = pn.DataFrame(data=predictions, columns=['predicted'])
                predictions = pn.concat([user_items_DF, predictions], axis=1)
                predictions = predictions.sort_values(by=['predicted'], ascending=False)
                result = pn.concat([result, predictions])
                items_DF = items_list_c
            final_result = result.groupby(['item_id'], as_index=False).mean()
            final_result = final_result.sort_values(by=['predicted'], ascending=False)
            return final_result


def Cosine_Jaccard_sim_HybMLP(friendship, user_id, k, test, Data_items, Data_users, reviews, user_friends, model, Mode):
    test_set_user = test.loc[test['user_id'] == user_id]
    items_list = list(test_set_user["item_id"])
    items_info = Data_items.loc[Data_items['item_id'].isin(items_list)]
    items_info.reset_index(inplace=True, drop=True)
    if Mode == 1:  # JACCARD SIMILARITY
        friends_deg = friendship.loc[friendship['user_1'] == user_id]
        if len(friends_deg) != 0:
            TOP_friends = friends_deg.sort_values(by='friendship', ascending=False).head(k)
            top_friends_list = list(TOP_friends["user_2"])
            friends_info = Data_users.loc[Data_users['user_id'].isin(top_friends_list)]
            friends_info.reset_index(inplace=True, drop=True)

            final_result = pn.DataFrame(columns=['item_id', 'latitude', 'longitude', 'Breakfast & Brunch',
                                                 'American (Traditional)', 'Burgers', 'Fast Food', 'American (New)',
                                                 'Chinese', 'Pizza', 'Italian', 'Sandwiches', 'Sushi Bars',
                                                 'Japanese',
                                                 'Indian', 'Mexican', 'Vietnamese', 'Thai', 'Asian Fusion',
                                                 'Take-out',
                                                 'Wi-Fi', 'dessert', 'latenight', 'lunch', 'dinner', 'breakfast',
                                                 'brunch', 'Caters', 'Noise Level', 'Takes Reservations',
                                                 'Delivery',
                                                 'romantic', 'intimate', 'touristy', 'hipster', 'divey', 'classy',
                                                 'trendy', 'upscale', 'casual', 'Parking', 'Has TV',
                                                 'Outdoor Seating',
                                                 'Attire', 'Alcohol', 'Waiter Service', 'Accepts Credit Cards',
                                                 'Good for Kids', 'Good For Groups', 'Price Range',
                                                 'Wheelchair Accessible', 'user_id', 'fans', 'average_stars',
                                                 'friends',
                                                 'vote_funny', 'useful', 'vote_cool', 'hot', 'more', 'profile',
                                                 'cute',
                                                 'list', 'note', 'plain', 'cool', 'funny', 'writer', 'photos',
                                                 'predicted'])
            for i in range(len(TOP_friends)):
                print(TOP_friends)
                print(i)
                userDATA = friends_info[
                    ['user_id', 'fans', 'average_stars', 'friends', 'vote_funny', 'useful', 'vote_cool', 'hot',
                     'more',
                     'profile', 'cute', 'list', 'note', 'plain', 'cool', 'funny', 'writer', 'photos']].iloc[i]
                userDATA = userDATA.to_frame().T
                userDATA = pn.concat([userDATA] * len(items_info), ignore_index=True)

                result = pn.concat([items_info, userDATA], axis=1)
                test_userID = result['user_id']
                test_userDATA = result[
                    ['fans', 'average_stars', 'friends', 'vote_funny', 'useful', 'vote_cool', 'hot', 'more',
                     'profile', 'cute', 'list', 'note', 'plain', 'cool', 'funny', 'writer', 'photos']]

                test_itemID = result['item_id']
                test_itemDATA = result[
                    ['latitude', 'longitude', 'Breakfast & Brunch', 'American (Traditional)', 'Burgers',
                     'Fast Food',
                     'American (New)', 'Chinese', 'Pizza', 'Italian', 'Sandwiches', 'Sushi Bars', 'Japanese',
                     'Indian', 'Mexican', 'Vietnamese', 'Thai', 'Asian Fusion', 'Take-out', 'Wi-Fi',
                     'dessert', 'latenight', 'lunch', 'dinner', 'breakfast', 'brunch', 'Caters',
                     'Noise Level', 'Takes Reservations', 'Delivery', 'romantic', 'intimate', 'touristy',
                     'hipster', 'divey', 'classy', 'trendy', 'upscale', 'casual',
                     'Parking', 'Has TV', 'Outdoor Seating', 'Attire', 'Alcohol', 'Waiter Service',
                     'Accepts Credit Cards', 'Good for Kids', 'Good For Groups',
                     'Price Range', 'Wheelchair Accessible']]
                predictions = model.predict([test_userID, test_userDATA, test_itemID, test_itemDATA],
                                            verbose=2)
                predictions = pn.DataFrame(data=predictions, columns=['predicted'])
                predictions = pn.concat([result, predictions], axis=1)
                predictions = predictions.sort_values(by=['predicted'], ascending=False)
                final_result = pn.concat([final_result, predictions])
            final_result = final_result.groupby(['item_id'], as_index=False).mean()
            final_result = final_result.sort_values(by=['predicted'], ascending=False)
            col_list = ['item_id', 'latitude', 'longitude', 'Breakfast & Brunch',
                        'American (Traditional)', 'Burgers', 'Fast Food', 'American (New)',
                        'Chinese', 'Pizza', 'Italian', 'Sandwiches', 'Sushi Bars', 'Japanese',
                        'Indian', 'Mexican', 'Vietnamese', 'Thai', 'Asian Fusion', 'Take-out',
                        'Wi-Fi', 'dessert', 'latenight', 'lunch', 'dinner', 'breakfast',
                        'brunch', 'Caters', 'Noise Level', 'Takes Reservations', 'Delivery',
                        'romantic', 'intimate', 'touristy', 'hipster', 'divey', 'classy',
                        'trendy', 'upscale', 'casual', 'Parking', 'Has TV', 'Outdoor Seating',
                        'Attire', 'Alcohol', 'Waiter Service', 'Accepts Credit Cards',
                        'Good for Kids', 'Good For Groups', 'Price Range',
                        'Wheelchair Accessible', 'predicted']
            final_result = final_result[col_list]
            return final_result
    else:  # COSINE SIMILARITY
        sort = Cosine_sim(user_id, reviews, user_friends)
        if len(sort) != 0:
            TOP_sorted = sort.head(k)
            top_friends_list = list(TOP_sorted["friend_id"])
            friends_info = Data_users.loc[Data_users['user_id'].isin(top_friends_list)]
            friends_info.reset_index(inplace=True, drop=True)

            final_result = pn.DataFrame(columns=['item_id', 'latitude', 'longitude', 'Breakfast & Brunch',
                                                 'American (Traditional)', 'Burgers', 'Fast Food', 'American (New)',
                                                 'Chinese', 'Pizza', 'Italian', 'Sandwiches', 'Sushi Bars',
                                                 'Japanese',
                                                 'Indian', 'Mexican', 'Vietnamese', 'Thai', 'Asian Fusion',
                                                 'Take-out',
                                                 'Wi-Fi', 'dessert', 'latenight', 'lunch', 'dinner', 'breakfast',
                                                 'brunch', 'Caters', 'Noise Level', 'Takes Reservations',
                                                 'Delivery',
                                                 'romantic', 'intimate', 'touristy', 'hipster', 'divey', 'classy',
                                                 'trendy', 'upscale', 'casual', 'Parking', 'Has TV',
                                                 'Outdoor Seating',
                                                 'Attire', 'Alcohol', 'Waiter Service', 'Accepts Credit Cards',
                                                 'Good for Kids', 'Good For Groups', 'Price Range',
                                                 'Wheelchair Accessible', 'user_id', 'fans', 'average_stars',
                                                 'friends',
                                                 'vote_funny', 'useful', 'vote_cool', 'hot', 'more', 'profile',
                                                 'cute',
                                                 'list', 'note', 'plain', 'cool', 'funny', 'writer', 'photos',
                                                 'predicted'])
            for i in range(len(friends_info)):
                userDATA = friends_info[
                    ['user_id', 'fans', 'average_stars', 'friends', 'vote_funny', 'useful', 'vote_cool', 'hot',
                     'more',
                     'profile', 'cute', 'list', 'note', 'plain', 'cool', 'funny', 'writer', 'photos']].iloc[i]
                userDATA = userDATA.to_frame().T
                userDATA = pn.concat([userDATA] * len(items_info), ignore_index=True)

                result = pn.concat([items_info, userDATA], axis=1)
                test_userID = result['user_id']
                test_userDATA = result[
                    ['fans', 'average_stars', 'friends', 'vote_funny', 'useful', 'vote_cool', 'hot', 'more',
                     'profile', 'cute', 'list', 'note', 'plain', 'cool', 'funny', 'writer', 'photos']]

                test_itemID = result['item_id']
                test_itemDATA = result[
                    ['latitude', 'longitude', 'Breakfast & Brunch', 'American (Traditional)', 'Burgers',
                     'Fast Food',
                     'American (New)', 'Chinese', 'Pizza', 'Italian', 'Sandwiches', 'Sushi Bars', 'Japanese',
                     'Indian', 'Mexican', 'Vietnamese', 'Thai', 'Asian Fusion', 'Take-out', 'Wi-Fi',
                     'dessert', 'latenight', 'lunch', 'dinner', 'breakfast', 'brunch', 'Caters',
                     'Noise Level', 'Takes Reservations', 'Delivery', 'romantic', 'intimate', 'touristy',
                     'hipster', 'divey', 'classy', 'trendy', 'upscale', 'casual',
                     'Parking', 'Has TV', 'Outdoor Seating', 'Attire', 'Alcohol', 'Waiter Service',
                     'Accepts Credit Cards', 'Good for Kids', 'Good For Groups',
                     'Price Range', 'Wheelchair Accessible']]
                predictions = model.predict([test_userID, test_userDATA, test_itemID, test_itemDATA],
                                            verbose=2)
                predictions = pn.DataFrame(data=predictions, columns=['predicted'])
                predictions = pn.concat([result, predictions], axis=1)
                predictions = predictions.sort_values(by=['predicted'], ascending=False)
                final_result = pn.concat([final_result, predictions])
            final_result = final_result.groupby(['item_id'], as_index=False).mean()
            final_result = final_result.sort_values(by=['predicted'], ascending=False)
            col_list = ['item_id', 'latitude', 'longitude', 'Breakfast & Brunch',
                        'American (Traditional)', 'Burgers', 'Fast Food', 'American (New)',
                        'Chinese', 'Pizza', 'Italian', 'Sandwiches', 'Sushi Bars', 'Japanese',
                        'Indian', 'Mexican', 'Vietnamese', 'Thai', 'Asian Fusion', 'Take-out',
                        'Wi-Fi', 'dessert', 'latenight', 'lunch', 'dinner', 'breakfast',
                        'brunch', 'Caters', 'Noise Level', 'Takes Reservations', 'Delivery',
                        'romantic', 'intimate', 'touristy', 'hipster', 'divey', 'classy',
                        'trendy', 'upscale', 'casual', 'Parking', 'Has TV', 'Outdoor Seating',
                        'Attire', 'Alcohol', 'Waiter Service', 'Accepts Credit Cards',
                        'Good for Kids', 'Good For Groups', 'Price Range',
                        'Wheelchair Accessible', 'predicted']
            final_result = final_result[col_list]
            return final_result


def read_data_load_models(path_test, friendship_path, model_path, Choice_model):
    if Choice_model == 1:
        model = load_model(model_path + "MODEL HybMLP.h5")
    else:
        model = load_model(model_path + "MODEL MLP.h5")

    test_columns = ['user_id', 'item_id', 'rating', 'fans', 'average_stars', 'friends',
                    'vote_funny', 'useful', 'vote_cool', 'hot', 'more', 'profile', 'cute',
                    'list', 'note', 'plain', 'cool', 'funny', 'writer', 'photos',
                    'latitude', 'longitude', 'Breakfast & Brunch', 'American (Traditional)',
                    'Burgers', 'Fast Food', 'American (New)', 'Chinese', 'Pizza', 'Italian',
                    'Sandwiches', 'Sushi Bars', 'Japanese', 'Indian', 'Mexican',
                    'Vietnamese', 'Thai', 'Asian Fusion', 'Take-out', 'Wi-Fi', 'dessert',
                    'latenight', 'lunch', 'dinner', 'breakfast', 'brunch', 'Caters',
                    'Noise Level', 'Takes Reservations', 'Delivery', 'romantic', 'intimate',
                    'touristy', 'hipster', 'divey', 'classy', 'trendy', 'upscale', 'casual',
                    'Parking', 'Has TV', 'Outdoor Seating', 'Attire', 'Alcohol',
                    'Waiter Service', 'Accepts Credit Cards', 'Good for Kids',
                    'Good For Groups', 'Price Range', 'Wheelchair Accessible']
    test = pn.read_csv(path_test + 'test.csv', delimiter='::',
                       names=test_columns, engine='python')

    user1_user2_Fr_columns = ['user_1', 'user_2', 'friendship']
    friendship = pn.read_csv(friendship_path + 'friendship.csv', delimiter='::',
                             names=user1_user2_Fr_columns, engine='python')
    friendship.user_1 = friendship.user_1.astype(int)
    friendship.user_2 = friendship.user_2.astype(int)

    yelp_reviews_columns = ['user_id', 'item_id', 'rating', 'rating_val']
    reviews = pn.read_csv(friendship_path + 'reviews.csv', delimiter='::',
                          names=yelp_reviews_columns, engine='python')

    yelp_user_fr_columns = ['user_id', 'friend_id', 'val']
    user_friends = pn.read_csv(friendship_path + 'friends.csv', delimiter='::',
                               names=yelp_user_fr_columns, engine='python')
    users_columns = ['user_id', 'fans', 'average_stars', 'friends', 'vote_funny', 'useful',
                     'vote_cool', 'hot', 'more', 'profile', 'cute', 'list', 'note', 'plain',
                     'cool', 'funny', 'writer', 'photos']
    Data_users = pn.read_csv(friendship_path + 'users.csv', delimiter='::',
                             names=users_columns, engine='python')

    columns_items = ['item_id', 'latitude', 'longitude', 'Breakfast & Brunch', 'American (Traditional)', 'Burgers',
                     'Fast Food',
                     'American (New)', 'Chinese', 'Pizza', 'Italian', 'Sandwiches', 'Sushi Bars', 'Japanese',
                     'Indian', 'Mexican', 'Vietnamese', 'Thai', 'Asian Fusion', 'Take-out', 'Wi-Fi',
                     'dessert', 'latenight', 'lunch', 'dinner', 'breakfast', 'brunch', 'Caters',
                     'Noise Level', 'Takes Reservations', 'Delivery', 'romantic', 'intimate', 'touristy',
                     'hipster', 'divey', 'classy', 'trendy', 'upscale', 'casual',
                     'Parking', 'Has TV', 'Outdoor Seating', 'Attire', 'Alcohol', 'Waiter Service',
                     'Accepts Credit Cards', 'Good for Kids', 'Good For Groups',
                     'Price Range', 'Wheelchair Accessible']
    Data_items = pn.read_csv(friendship_path + 'restaurants.csv', delimiter='::', encoding='cp1252',
                             names=columns_items, engine='python')

    return test, model, friendship, reviews, user_friends, Data_items, Data_users


def Combi(prediction_1, prediction_2, a):
    prediction_1 = prediction_1.copy(deep=True)

    prediction_1.loc[:, 'predicted'] *= a
    if prediction_2 is not None and a != 1:
        prediction_2 = prediction_2.copy(deep=True)
        prediction_2.loc[:, 'predicted'] *= (1 - a)

        prediction_2 = prediction_2.sort_values(by=['predicted'], ascending=False)
        prediction_1 = prediction_1.sort_values(by=['predicted'], ascending=False)

        result_data = []
        columns = ['item_id', 'predicted']
        for k in range(len(prediction_1)):
            row_1 = prediction_1.iloc[k]
            item_id = row_1['item_id']
            val_1 = row_1['predicted']
            row_2 = prediction_2.loc[prediction_2['item_id'] == item_id]
            val_2 = row_2['predicted'].values[0]
            result = val_1 + val_2
            result_data.append([item_id, result])
        final = pn.DataFrame(data=result_data, columns=columns)
    else:
        final = prediction_1
    return final


def General_result(users_sample, test, model, friendship, reviews, user_friends, Data_items, Mode, k, Data_users,
                   Choice_model, Alpha_combi, combination_bool, Context_choice, distance):
    all_diffs, all_hrs, all_ndcgs = {}, {}, {}
    for i in range(users_sample):
        if Choice_model == 1:
            SocF_result = Cosine_Jaccard_sim_HybMLP(friendship, i, k, test, Data_items, Data_users, reviews,
                                                    user_friends, model, Mode)
            if combination_bool == 1:
                CCF_result = CCF_prediction(test, model, i)
                result = Combi(CCF_result, SocF_result, Alpha_combi)
            else:
                result = SocF_result
        else:
            SocF_result = Cosine_Jaccard_sim_MLP(friendship, i, k, test, Data_items, reviews, user_friends, model, Mode)
            print(SocF_result)
            if combination_bool == 1:
                CF_result = CF_prediction(test, model, i)
                result = Combi(CF_result, SocF_result, Alpha_combi)
                print(result)
            else:
                result = SocF_result
        # add rating column
        test_set_user = test.loc[test['user_id'] == i]
        final_result = result.assign(rating=0)
        final_result = final_result.reset_index(drop=True)
        pos_row = test_set_user.loc[test_set_user['rating'] == 1]
        final_result.loc[final_result['item_id'] == int(pos_row['item_id']), 'rating'] = 1

        if Context_choice == 1:
            item_longitude = pos_row["longitude"].values[0]
            item_latitude = pos_row["latitude"].values[0]
            predicted_filtered = Context_dis(final_result, test_set_user, item_latitude, item_longitude, distance)
            final_result = predicted_filtered
            print("Context", final_result)
        # hit@10 NDCG@10
        r = final_result.loc[:, 'rating'].head(10)
        hr, ndcg = evaluate_(r)
        # Ecart
        diff = final_result.loc[final_result['item_id'] == int(pos_row['item_id']), 'rating'] - final_result.loc[
            final_result['item_id'] == int(pos_row['item_id']), 'predicted']

        all_diffs[i], all_hrs[i], all_ndcgs[i] = diff.values[0], hr, ndcg

    return all_diffs, all_hrs, all_ndcgs


if __name__ == '__main__':
    st = time.time()

    args = parse_args()
    test_path = args.test_path
    model_path = args.model_path
    friendship_path = args.friendship_path
    users_sample = int(args.users_sample)
    Choice_model = int(args.Choice_model)
    Context_choice = int(args.Context_choice)
    Alpha_combi = float(args.Alpha_combi)
    distance = float(args.distance)
    Mode = int(args.Mode)
    combination_bool = int(args.combination_bool)
    K = int(args.K)

    # read data
    test, model, friendship, reviews, user_friends, Data_items, Data_users = read_data_load_models(test_path,
                                                                                                   friendship_path,
                                                                                                   model_path,
                                                                                                   Choice_model)
    diffs, hrs, ndcgs = General_result(users_sample, test, model, friendship, reviews, user_friends,
                                       Data_items, Mode, K, Data_users,
                                       Choice_model, Alpha_combi, combination_bool, Context_choice,
                                       distance)

    pl.figure(figsize=(8, 6), dpi=110)
    x1, y1 = zip(*(hrs.items()))
    x2, y2 = zip(*(ndcgs.items()))
    x3, y3 = zip(*(diffs.items()))
    # Create 2x2 sub plots

    gs = gridspec.GridSpec(2, 2)
    ax1 = pl.subplot(gs[0, 0])
    ax1.plot(x1, y1, 'ro--', linestyle='dashed')
    ax1.set_title("all HR's")
    ax1.set_ylabel('HR@10')
    ax1.set_xlabel('users')

    ax2 = pl.subplot(gs[0, 1])
    ax2.plot(x2, y2, 'bd--', linestyle='dashed')
    ax2.set_ylabel('NDCG@10')
    ax2.set_xlabel('users')
    ax2.set_title("all NDCG's")

    ax3 = pl.subplot(gs[1, :])
    ax3.plot(x3, y3, 'gd--', linestyle='dashed')
    ax3.set_title("all ecart's")
    ax3.set_ylabel('Ecart')
    ax3.set_xlabel('users')

    manager = pl.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())
    # script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    # pl.savefig(os.path.join(script_dir, 'P-r-e-s/result.png'))
    pl.show()
    print("----%.2f----" % (time.time() - st))
