import math
import time

import pandas as pn
import numpy as np
from keras.models import load_model
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors


# ------------------------------------------------------[Yelp]----------------------------------------------------------
def friendship_DF(path):  # yelp
    data = []
    yelp_users_columns = ['user_id', 'fans', 'average_stars', 'friends', 'vote_funny', 'useful',
                          'vote_cool', 'hot', 'more', 'profile', 'cute', 'list', 'note', 'plain',
                          'cool', 'funny', 'writer', 'photos']
    Data_users = pn.read_csv(path + 'users.csv', delimiter='::',
                             names=yelp_users_columns, engine='python')

    yelp_user_fr_columns = ['user_id', 'friend_id', 'val']
    DFUF = pn.read_csv(path + 'friends.csv', delimiter='::',
                       names=yelp_user_fr_columns, engine='python')

    friends_nbr = DFUF['user_id'].value_counts()
    #  friends_nbr n index qui est le id de l"utilisateur et le nombre d'amis

    DF1 = pn.DataFrame(friends_nbr)
    DF1.reset_index(inplace=True, drop=False)
    DF1.rename(columns={'index': 'user_id', 'user_id': 'friends_nbr'}, inplace=True)

    rslt_df = Data_users.loc[~Data_users.index.isin(DF1['user_id'])]

    rslt_df = rslt_df.index
    for j in rslt_df:
        data.append([j, 0])

        # DF2 contient les id qui sont pas dans le fichier donc qui ont 0 amis
        DF2 = pn.DataFrame(data, columns=['user_id', 'friends_nbr'])

        # DF contient DF1 et DF2
        DF = pn.concat([DF1, DF2])

        DF = DF.sort_values(by=['user_id'])
        DF.reset_index(inplace=True, drop=True)
    sum = 0
    data = []
    columns = ['user_id_1', 'user_id_2', 'Deg_Sim']

    for i in range(len(DF.index)):
        print(i)
        result1 = DFUF.loc[DFUF['user_id'] == i]
        row_nbr_friends1 = DF.loc[DF['user_id'] == i]
        nbr_friends1 = row_nbr_friends1.iloc[0, 1]

        friends_list1 = result1['friend_id']

        friends_list1.reset_index(inplace=True, drop=True)

        for j in range(len(friends_list1)):
            row_fr_id = friends_list1.loc[friends_list1.index == j]
            ID_friend = row_fr_id.iloc[0]

            result2 = DFUF.loc[DFUF['user_id'] == row_fr_id.iloc[0]]

            row_nbr_friends2 = DF.loc[DF['user_id'] == ID_friend]

            nbr_friends2 = row_nbr_friends2.iloc[0, 1]

            inter = pn.merge(result1, result2, how='inner', on=['friend_id'])
            # SIM == deg
            Sim = len(inter) / (nbr_friends2 + nbr_friends1 - len(inter))

            sum = sum + Sim
            data.append([i, ID_friend, Sim])

    friendship = pn.DataFrame(data, columns=columns)
    np.savetxt(path + 'friendship.csv', friendship, delimiter='::', fmt='%f')
    return friendship


# MODE==0 ==> FRIENDSHIP  || MODE==1 ==>  KNN
def friendship_KNN(path, user_id, k, test, Data_items, Data_users, model_hybMLP, model_mlp, Mode, Model):
    # list of items
    test_set_user = test.loc[test['user_id'] == user_id]
    items_list = list(test_set_user["item_id"])
    items_info = Data_items.loc[Data_items['item_id'].isin(items_list)]
    items_info.reset_index(inplace=True, drop=True)

    if Mode == 1:  # FRIENDSHIP
        user1_user2_Fr_columns = ['user_1', 'user_2', 'friendship']
        friendship = pn.read_csv(path + 'friendship.csv', delimiter='::',
                                 names=user1_user2_Fr_columns, engine='python')
        friendship.user_1 = friendship.user_1.astype(int)
        friendship.user_2 = friendship.user_2.astype(int)

        friends_deg = friendship.loc[friendship['user_1'] == user_id]
        if len(friends_deg) != 0:
            TOP_friends = friends_deg.sort_values(by='friendship', ascending=False).head(k)
            top_friends_list = list(TOP_friends["user_2"])
            if Model == 1:
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
                    predictions = model_hybMLP.predict([test_userID, test_userDATA, test_itemID, test_itemDATA],
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
            elif Model == 2:
                items_DF = pn.DataFrame(items_list, columns=['item_id'])
                items_list_c = items_DF.copy()
                result = pn.DataFrame(columns=['item_id', 'user_id', 'predicted'])
                for index, row in TOP_friends.iterrows():
                    user_items_DF = items_DF.assign(user_id=int(row['user_2']))
                    test_userID = user_items_DF['user_id']
                    test_itemID = user_items_DF['item_id']
                    predictions = model_mlp.predict([test_userID, test_itemID], verbose=2)
                    predictions = pn.DataFrame(data=predictions, columns=['predicted'])
                    predictions = pn.concat([user_items_DF, predictions], axis=1)
                    predictions = predictions.sort_values(by=['predicted'], ascending=False)
                    result = pn.concat([result, predictions])
                    items_DF = items_list_c
                final_result = result.groupby(['item_id'], as_index=False).mean()
                final_result = final_result.sort_values(by=['predicted'], ascending=False)
            return final_result
    elif Mode == 2:  # KNN
        sort = KNN_yelp(path, user_id)
        if len(sort) != 0:
            TOP_sorted = sort.head(k)
            top_friends_list = list(TOP_sorted["friend_id"])
            if Model == 1:
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
                    predictions = model_hybMLP.predict([test_userID, test_userDATA, test_itemID, test_itemDATA],
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
            elif Model == 2:
                items_DF = pn.DataFrame(items_list, columns=['item_id'])
                items_list_c = items_DF.copy()
                result = pn.DataFrame(columns=['item_id', 'user_id', 'predicted'])
                for index, row in TOP_sorted.iterrows():
                    user_items_DF = items_DF.assign(user_id=int(row['friend_id']))
                    test_userID = user_items_DF['user_id']
                    test_itemID = user_items_DF['item_id']
                    predictions = model_mlp.predict([test_userID, test_itemID], verbose=2)
                    predictions = pn.DataFrame(data=predictions, columns=['predicted'])
                    predictions = pn.concat([user_items_DF, predictions], axis=1)
                    predictions = predictions.sort_values(by=['predicted'], ascending=False)
                    result = pn.concat([result, predictions])
                    items_DF = items_list_c
                final_result = result.groupby(['item_id'], as_index=False).mean()
                final_result = final_result.sort_values(by=['predicted'], ascending=False)
            return final_result


def KNN_yelp(path, user_id):
    yelp_reviews_columns = ['user_id', 'item_id', 'rating', 'rating_val']
    DFR = pn.read_csv(path + 'reviews.csv', delimiter='::',
                      names=yelp_reviews_columns, engine='python')

    yelp_user_fr_columns = ['user_id', 'friend_id', 'val']
    DFUF = pn.read_csv(path + 'friends.csv', delimiter='::',
                       names=yelp_user_fr_columns, engine='python')

    user_friends = DFUF.loc[DFUF['user_id'] == user_id]
    friends_ids = list(user_friends["friend_id"])
    friends_ids.append(user_id)

    DFR_pivot = DFR.pivot(index='user_id', columns='item_id', values='rating_val').replace(np.nan, 0)

    friends_pivot = DFR_pivot.loc[DFR_pivot.index.isin(friends_ids)]

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


# ------------------------------------------------[Evaluation Yelp FR-KNN]----------------------------------------------

def evaluate_(result):
    ndcg = 0
    i = 1
    for rating in result:
        if rating == 1:
            ndcg = math.log(2) / math.log(i + 1)
            break
        i = i + 1
    return ndcg


def Yelp_soc_evaluation(path, k, test_path, model_path, Mode, Model):
    Data_items, test, Data_users, model_hybMLP, model_mlp = read_files_evaluation_yelp(path, test_path, model_path)
    ndcgs = 0
    i = 0
    for index, row in Data_users.iterrows():
        print('user: ', row['user_id'])
        result = friendship_KNN(path, row['user_id'], k, test, Data_items, Data_users, model_hybMLP, model_mlp, Mode,
                                Model)
        if result is not None:
            test_set_user = test.loc[test['user_id'] == row['user_id']]
            result = result.assign(rating=0)
            result = result.reset_index(drop=True)
            pos_row = test_set_user.loc[test_set_user['rating'] == 1]
            result.loc[result['item_id'] == int(pos_row['item_id']), 'rating'] = 1
            r = result.loc[:, 'rating']
            ndcg = evaluate_(r)
            ndcgs = ndcgs + ndcg
            i = i + 1
    mean_ndcg = ndcgs / i
    print('MEAN NDCG:', mean_ndcg)
    return mean_ndcg


def read_files_evaluation_yelp(path, test_path, model_path):
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
    test = pn.read_csv(test_path + 'test.csv', delimiter='::',
                       names=test_columns, engine='python')

    users_columns = ['user_id', 'fans', 'average_stars', 'friends', 'vote_funny', 'useful',
                     'vote_cool', 'hot', 'more', 'profile', 'cute', 'list', 'note', 'plain',
                     'cool', 'funny', 'writer', 'photos']
    Data_users = pn.read_csv(path + 'users.csv', delimiter='::',
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
    Data_items = pn.read_csv(path + 'restaurants.csv', delimiter='::', encoding='cp1252',
                             names=columns_items, engine='python')

    model_hybMLP = load_model(model_path + "MODEL HybMLP.h5")
    model_mlp = load_model(model_path + "MODEL MLP.h5")
    return Data_items, test, Data_users, model_hybMLP, model_mlp


# ------------------------------------------------------[Film Trust]----------------------------------------------------
def Trust_imp_ex_DF(path, Alpha):  # Film trust imp exp ratio
    print('Processing data alpha =' + str(Alpha) + '...')
    user1_user2_it_columns = ['user_1', 'user_2', 'it']
    Data_imp_trust = pn.read_csv(path + 'imp_trust.csv', delimiter='::',
                                 names=user1_user2_it_columns, engine='python')
    Data_imp_trust.user_1 = Data_imp_trust.user_1.astype(int)
    Data_imp_trust.user_2 = Data_imp_trust.user_2.astype(int)
    # print(Data_imp_trust.isna().sum())
    it_pivot = Data_imp_trust.pivot(index='user_1', columns='user_2', values='it')
    user1_user2_et_columns = ['user_1', 'user_2', 'et']
    et = pn.read_csv(path + 'ex_prop.csv', delimiter='::',
                     names=user1_user2_et_columns, engine='python')
    et.user_1 = et.user_1.astype(int)
    et.user_2 = et.user_2.astype(int)
    for i in range(len(it_pivot)):
        for j in range(len(it_pivot)):
            print(i, j)
            if i == j:
                it_pivot.iloc[i, j] = it_pivot.iloc[i, j]
            else:
                it_pivot.iloc[i, j] = it_pivot.iloc[i, j] * (1 - Alpha)

    for i in range(len(et)):
        et_value = et['et'].iloc[i]
        it_value = it_pivot.iloc[et['user_1'].iloc[i], et['user_2'].iloc[i]]
        if math.isnan(it_value):
            ct_value = (Alpha * et_value)
        else:
            ct_value = (Alpha * et_value) + it_value
        it_pivot.iloc[et['user_1'].iloc[i], et['user_2'].iloc[i]] = ct_value

    it_ex_pivot = it_pivot
    it_ex = it_ex_pivot.unstack().reset_index(name='value')
    it_ex.rename(columns={'user_2': 'user_1', 'user_1': 'user_2', 'value': 'it_ex'}, inplace=True)
    np.savetxt(path + 'imp_ex_trust.csv', it_ex, delimiter='::', fmt='%f')
    print('Data  processed alpha =' + str(Alpha) + '.')
    return it_ex


def MLP_imp_ex(it_ex, user_id, k, test, model):  # Film trust combination with MLP (path, Alpha, user_id,
    # item_set):
    it_ex.user_1 = it_ex.user_1.astype(int)
    it_ex.user_2 = it_ex.user_2.astype(int)
    # get top gens de confiance
    it_ex_piv = it_ex.pivot(index='user_1', columns='user_2', values='it_ex')
    it_ex_piv = it_ex_piv.replace(0, np.nan)
    it_ex_piv.iloc[user_id, user_id] = np.nan
    user_trust_row = it_ex_piv.loc[it_ex_piv.index == user_id]
    user_trust_row = user_trust_row.unstack().reset_index(name='value').dropna()
    TOP_con = user_trust_row.sort_values(by='value', ascending=False).head(k)
    # items list
    if not TOP_con.empty:
        test_set_user = test.loc[test['user_id'] == user_id]
        items_list = list(test_set_user["item_id"])
        items_DF = pn.DataFrame(items_list, columns=['item_id'])
        items_list_c = items_DF.copy()
        # i = 0
        result = pn.DataFrame(columns=['item_id', 'user_id', 'predicted'])
        for index, row in TOP_con.iterrows():
            if int(row['user_2']) != user_id:
                user_items_DF = items_DF.assign(user_id=int(row['user_2']))
                test_userID = user_items_DF['user_id']
                test_itemID = user_items_DF['item_id']
                predictions = model.predict([test_userID, test_itemID], verbose=2)
                predictions = pn.DataFrame(data=predictions, columns=['predicted'])
                predictions = pn.concat([user_items_DF, predictions], axis=1)
                predictions = predictions.sort_values(by=['predicted'], ascending=False)
                result = pn.concat([result, predictions])
            items_DF = items_list_c
            # i = +1
        result = result.groupby(['item_id'], as_index=False).mean()
        final_result = result.sort_values(by=['predicted'], ascending=False)
    else:
        final_result = None
    return final_result


# ---------------------------------------------[Evaluation Film Trust imp exp]------------------------------------------

def Film_Trust_soc_evaluation(path, k, test_path, model_path):
    test_columns = ['user_id', 'item_id', 'rating']
    test = pn.read_csv(test_path + 'test.csv', delimiter='::',
                       names=test_columns, engine='python')

    ex_it_columns = ['user_1', 'user_2', 'it_ex']
    it_ex = pn.read_csv(path + 'imp_ex_trust.csv', delimiter='::',
                        names=ex_it_columns, engine='python')
    Data_users = pn.read_csv(path + 'users.csv', delimiter='::',
                             names=['user_id'], engine='python')
    # load the model
    model = load_model(model_path + "MODEL MLP.h5")
    ndcgs = 0
    for index, row in Data_users.iterrows():
        result = MLP_imp_ex(it_ex, row['user_id'], k, test, model)
        print(result)
        if result is not None:
            test_set_user = test.loc[test['user_id'] == row['user_id']]
            result = result.assign(rating=0)
            result = result.reset_index(drop=True)
            pos_row = test_set_user.loc[test_set_user['rating'] == 1]
            result.loc[result['item_id'] == int(pos_row['item_id']), 'rating'] = 1
            r = result.loc[:, 'rating']
            ndcg = evaluate_(r)
            ndcgs = ndcgs + ndcg
            print(ndcg)
    mean_ndcg = ndcgs / len(Data_users)
    print('MEAN NDCG:', mean_ndcg)
    return mean_ndcg


def Film_Trust_soc_diff(path, k, test_path, model_path):
    test_columns = ['user_id', 'item_id', 'rating']
    test = pn.read_csv(test_path + 'test.csv', delimiter='::',
                       names=test_columns, engine='python')

    ex_it_columns = ['user_1', 'user_2', 'it_ex']
    it_ex = pn.read_csv(path + 'imp_ex_trust.csv', delimiter='::',
                        names=ex_it_columns, engine='python')
    Data_users = pn.read_csv(path + 'users.csv', delimiter='::',
                             names=['user_id'], engine='python')
    # load the model
    model = load_model(model_path + "MODEL MLP.h5")
    i = 0
    diffs = 0
    for index, row in Data_users.iterrows():
        result = MLP_imp_ex(it_ex, row['user_id'], k, test, model)
        print('User:', row['user_id'])
        if result is not None:
            test_set_user = test.loc[test['user_id'] == row['user_id']]
            result = result.assign(rating=0)
            result = result.reset_index(drop=True)
            pos_row = test_set_user.loc[test_set_user['rating'] == 1]
            result.loc[result['item_id'] == int(pos_row['item_id']), 'rating'] = 1
            # ecart
            diff = result.loc[result['item_id'] == int(pos_row['item_id']), 'rating'] - result.loc[
                result['item_id'] == int(pos_row['item_id']), 'predicted']
            diffs = diffs + diff.values[0]
            i = i + 1
            print(i)
    mean_diff = diffs / i
    print('MEAN', mean_diff)
    return mean_diff


# ------------------------------------------------------[Combination]---------------------------------------------------
def evaluate_COMBI(test):
    hr, ndcg = 0, 0
    i = 1
    for rating in test:
        if rating == 1:
            hr = 1
            ndcg = math.log(2) / math.log(i + 1)
            break
        i = i + 1
    return hr, ndcg


# FILM TRUST
def COMBI_TOTAL_FT(test_path, path, model_path, Alpha):  # alpha du imp et exp == 0,4   !!!!!!!!!!!!
    test_columns = ['user_id', 'item_id', 'rating']
    test = pn.read_csv(test_path + 'test.csv', delimiter='::',
                       names=test_columns, engine='python')
    ex_it_columns = ['user_1', 'user_2', 'it_ex']
    it_ex = pn.read_csv(path + 'imp_ex_trust.csv', delimiter='::',
                        names=ex_it_columns, engine='python')
    Data_users = pn.read_csv(path + 'users.csv', delimiter='::',
                             names=['user_id'], engine='python')
    hrs = 0
    ndcgs = 0
    diffs = 0
    j = 0  # test
    # load the model
    model = load_model(model_path + "MODEL MLP.h5")
    for index, row in Data_users.iterrows():
        result_FCS = MLP_imp_ex(it_ex, row['user_id'], 1, test, model)
        if result_FCS is not None:
            print('FCS IN')
            test_set_user = test.loc[test['user_id'] == row['user_id']]
            result_FCS = result_FCS.assign(rating=0)
            result_FCS = result_FCS.reset_index(drop=True)
            pos_row = test_set_user.loc[test_set_user['rating'] == 1]
            result_FCS.loc[result_FCS['item_id'] == int(pos_row['item_id']), 'rating'] = 1

        if Alpha != 0:
            test_un_ID = test[test['user_id'] == row['user_id']]
            test_un_ID = test_un_ID.reset_index(drop=True)
            test_userID = test_un_ID['user_id']
            test_itemID = test_un_ID['item_id']
            predictions = model.predict([test_userID, test_itemID], verbose=2)
            predictions = pn.DataFrame(data=predictions, columns=['predicted'])
            predictions = pn.concat([test_un_ID, predictions], axis=1)
            predictions = predictions.sort_values(by=['predicted'], ascending=False)
            RFC_columns = ['item_id', 'rating', 'predicted']
            ressult_FC = predictions[RFC_columns]

            final_result = CONMBI(ressult_FC, result_FCS, Alpha)
            # add rating column
            test_set_user = test.loc[test['user_id'] == row['user_id']]
            final_result = final_result.assign(rating=0)
            final_result = final_result.reset_index(drop=True)
            pos_row = test_set_user.loc[test_set_user['rating'] == 1]
            final_result.loc[final_result['item_id'] == int(pos_row['item_id']), 'rating'] = 1
        else:
            final_result = result_FCS
        if final_result is not None:
            # hit@10 NDCG@10
            r = final_result.loc[:, 'rating'].head(10)
            hr, ndcg = evaluate_COMBI(r)
            hrs = hrs + hr
            ndcgs = ndcgs + ndcg
            # Ecart
            diff = final_result.loc[final_result['item_id'] == int(pos_row['item_id']), 'rating'] - final_result.loc[
                final_result['item_id'] == int(pos_row['item_id']), 'predicted']
            diffs = diffs + diff.values[0]
            j = j + 1
            print(j)

    print("Number of iterrations:", j)
    mean_diff = diffs / j
    print('MEAN DIFF:', mean_diff)
    mean_hr = hrs / len(Data_users)
    print('MEAN HR:', mean_hr)
    mean_ndcg = ndcgs / len(Data_users)
    print('MEAN NDCG:', mean_ndcg)
    return mean_diff, mean_hr, mean_ndcg, j


# Yelp Knn
def COMBI_TOTAL_Yelp(path, test_path, model_path, Alpha):
    Data_items, test, Data_users, model_hybMLP, model_mlp = read_files_evaluation_yelp(path, test_path, model_path)
    hrs = 0
    ndcgs = 0
    diffs = 0
    j = 0
    for index, row in Data_users.iterrows():
        print('user: ', row['user_id'])
        result_FCS = friendship_KNN(path, row['user_id'], 5, test, Data_items, Data_users, model_hybMLP, model_mlp, 2,
                                    1)
        if result_FCS is not None:
            print('FCS IN')
            test_set_user = test.loc[test['user_id'] == row['user_id']]
            result_FCS = result_FCS.assign(rating=0)
            result_FCS = result_FCS.reset_index(drop=True)
            pos_row = test_set_user.loc[test_set_user['rating'] == 1]
            result_FCS.loc[result_FCS['item_id'] == int(pos_row['item_id']), 'rating'] = 1
        # FC
        test_un_ID = test[test['user_id'] == row['user_id']]
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
        predictions = model_hybMLP.predict([test_userID, test_userDATA, test_itemID, test_itemDATA], verbose=2)
        predictions = pn.DataFrame(data=predictions, columns=['predicted'])
        predictions = pn.concat([test_un_ID, predictions], axis=1)
        predictions = predictions.sort_values(by=['predicted'], ascending=False)
        RFC_columns = ['item_id', 'rating', 'predicted']
        ressult_FC = predictions[RFC_columns]

        final_result = CONMBI(ressult_FC, result_FCS, Alpha)
        # add rating column
        test_set_user = test.loc[test['user_id'] == row['user_id']]
        final_result = final_result.assign(rating=0)
        final_result = final_result.reset_index(drop=True)
        pos_row = test_set_user.loc[test_set_user['rating'] == 1]
        final_result.loc[final_result['item_id'] == int(pos_row['item_id']), 'rating'] = 1

        # hit@10 NDCG@10
        r = final_result.loc[:, 'rating'].head(10)
        hr, ndcg = evaluate_COMBI(r)
        hrs = hrs + hr
        ndcgs = ndcgs + ndcg
        # Ecart
        diff = final_result.loc[final_result['item_id'] == int(pos_row['item_id']), 'rating'] - final_result.loc[
            final_result['item_id'] == int(pos_row['item_id']), 'predicted']
        diffs = diffs + diff.values[0]
        j = j + 1

    print("Number of iterrations:", j)
    mean_diff = diffs / j
    print('MEAN DIFF:', mean_diff)
    mean_hr = hrs / len(Data_users)
    print('MEAN HR:', mean_hr)
    mean_ndcg = ndcgs / len(Data_users)
    print('MEAN NDCG:', mean_ndcg)
    return mean_diff, mean_hr, mean_ndcg, j


def COMBI_TOTAL_Yelp_MLP(path, test_path, model_path, Alpha):
    Data_items, test, Data_users, model_hybMLP, model_mlp = read_files_evaluation_yelp(path, test_path, model_path)
    hrs = 0
    ndcgs = 0
    diffs = 0
    j = 0
    for index, row in Data_users.iterrows():
        print('user: ', row['user_id'])
        result_FCS = friendship_KNN(path, row['user_id'], 5, test, Data_items, Data_users, model_hybMLP, model_mlp, 2,
                                    2)
        if result_FCS is not None:
            print('FCS IN')
            test_set_user = test.loc[test['user_id'] == row['user_id']]
            result_FCS = result_FCS.assign(rating=0)
            result_FCS = result_FCS.reset_index(drop=True)
            pos_row = test_set_user.loc[test_set_user['rating'] == 1]
            result_FCS.loc[result_FCS['item_id'] == int(pos_row['item_id']), 'rating'] = 1
        # FC
        test_un_ID = test[test['user_id'] == row['user_id']]
        test_un_ID = test_un_ID.reset_index(drop=True)
        test_userID = test_un_ID['user_id']
        test_itemID = test_un_ID['item_id']

        predictions = model_mlp.predict([test_userID, test_itemID], verbose=2)
        predictions = pn.DataFrame(data=predictions, columns=['predicted'])
        predictions = pn.concat([test_un_ID, predictions], axis=1)
        predictions = predictions.sort_values(by=['predicted'], ascending=False)
        RFC_columns = ['item_id', 'rating', 'predicted']
        ressult_FC = predictions[RFC_columns]

        final_result = CONMBI(ressult_FC, result_FCS, Alpha)
        # add rating column
        test_set_user = test.loc[test['user_id'] == row['user_id']]
        final_result = final_result.assign(rating=0)
        final_result = final_result.reset_index(drop=True)
        pos_row = test_set_user.loc[test_set_user['rating'] == 1]
        final_result.loc[final_result['item_id'] == int(pos_row['item_id']), 'rating'] = 1

        # hit@10 NDCG@10
        r = final_result.loc[:, 'rating'].head(10)
        hr, ndcg = evaluate_COMBI(r)
        hrs = hrs + hr
        ndcgs = ndcgs + ndcg
        # Ecart
        diff = final_result.loc[final_result['item_id'] == int(pos_row['item_id']), 'rating'] - final_result.loc[
            final_result['item_id'] == int(pos_row['item_id']), 'predicted']
        diffs = diffs + diff.values[0]
        j = j + 1

    print("Number of iterrations:", j)
    mean_diff = diffs / j
    print('MEAN DIFF:', mean_diff)
    mean_hr = hrs / len(Data_users)
    print('MEAN HR:', mean_hr)
    mean_ndcg = ndcgs / len(Data_users)
    print('MEAN NDCG:', mean_ndcg)
    return mean_diff, mean_hr, mean_ndcg, j



def CONMBI(prediction_1, prediction_2, a):
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


if __name__ == '__main__':

    OPT = int(input("Train/test Enter 1)-Exp Imp Trust 2)-Friendship knn : "))
    if OPT == 1:
        # result = Film_Trust_soc_evaluation(path_imp_ex, 2, path_test, model_path)
        st = time.time()
        data = []
        print('Loading & Processing data...')
        path_imp_ex = "C:/Users/LATITUDE/Desktop/FILM TRUST Users-Items-Ratings-Trust (csv's)/"
        path_test = 'C:/Users/LATITUDE/Desktop/Train & Test Save film trust/'
        model_path = 'C:/Users/LATITUDE/Desktop/Train & Test Save film trust/'

        alpha = 1
        mean_diff, mean_hr, mean_ndcg, j = COMBI_TOTAL_FT(path_test, path_imp_ex, model_path, alpha)
        data.append([alpha, mean_diff, mean_hr, mean_ndcg, j])
        DF = pn.DataFrame(data, columns=['alpha', 'Diff', 'HR', 'NDCG', 'it'])
        np.savetxt("C:/Users/LATITUDE/Desktop/evaluations/film trust/Combinaison/" +
                   str(alpha) + ' COMBI FC FCSOC a=0,4 k=1.csv', DF, delimiter='::', fmt='%f')
        print(DF)
        print('Data loaded and processed.')
        print("----%.2f----" % (time.time() - st))
    elif OPT == 2:
        st = time.time()
        path_data = "C:/Users/LATITUDE/Desktop/Users-Items-Rating-UF (csv's)/"
        path_test = 'C:/Users/LATITUDE/Desktop/Train & Test Save yelp/'
        model_path = 'C:/Users/LATITUDE/Desktop/Train & Test Save yelp/'
        data = []

        for i in range(10, 12):
            alpha = i / 10
            mean_diff, mean_hr, mean_ndcg, j = COMBI_TOTAL_Yelp_MLP(path_data, path_test, model_path, alpha)
            data.append([alpha, mean_diff, mean_hr, mean_ndcg, j])
            DF = pn.DataFrame(data, columns=['alpha', 'Diff', 'HR', 'NDCG', 'it'])
            np.savetxt("C:/Users/LATITUDE/Desktop/evaluations/yelp/Combinaison/MLP/" +
                       str(alpha) + 'COMBI FC FCSOC a=0,4 k=5 KNN MLP.csv', DF, delimiter='::', fmt='%f')
        print(DF)
        print('Data loaded and processed.')
        print("----%.2f----" % (time.time() - st))
