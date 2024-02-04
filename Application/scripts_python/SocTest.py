import math
import time

import pandas as pn
from numpy import sqrt, NaN
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors


def read_and_trans_data(path, dataset):
    data = []
    if dataset == 2:  # yelp
        yelp_users_columns = ['user_id', 'fans', 'average_stars', 'friends', 'vote_funny', 'useful',
                              'vote_cool', 'hot', 'more', 'profile', 'cute', 'list', 'note', 'plain',
                              'cool', 'funny', 'writer', 'photos']
        Data_users = pn.read_csv(path + 'users.csv', delimiter='::',
                                 names=yelp_users_columns, engine='python')

        yelp_reviews_columns = ['user_id', 'item_id', 'rating', 'rating_val']
        Data_reviews = pn.read_csv(path + 'reviews.csv', delimiter='::',
                                   names=yelp_reviews_columns, engine='python')

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
        DFR = Data_reviews

        return DF, DFUF, DFR
    if dataset == 3:  # Film Trust

        FT_users_columns = ['user_id']
        Data_users = pn.read_csv(path + 'users.csv', delimiter='::',
                                 names=FT_users_columns, engine='python')

        FT_ratings_columns = ['user_id', 'item_id', 'rating', 'rating_val']
        Data_ratings = pn.read_csv(path + 'ratings.csv',delimiter =':delimitewr:',
                                   names=FT_ratings_columns, engine='python')

        FT_user_trustee_columns = ['user_id', 'Trustee', 'trust_val']
        Data_user_trustee = pn.read_csv(path + 'trusts.csv', delimiter='::',
                                        names=FT_user_trustee_columns, engine='python')
        DFU = Data_users
        DFR = Data_ratings
        DF = Data_user_trustee
        return DF, DFR, DFU


def KNN_yelp(path, dataset, user_id):
    DF, DFUF, DFR = read_and_trans_data(path, dataset)
    print(DF)
    print(DFUF.loc[DFUF['user_id'] == user_id])
    user_friends = DFUF.loc[DFUF['user_id'] == user_id]
    friends_ids = list(user_friends["friend_id"])
    friends_ids.append(user_id)
    print(friends_ids)

    print(len(DFR["user_id"].unique()))
    DFR_pivot = DFR.pivot(index='user_id', columns='item_id', values='rating_val').replace(np.nan, 0)
    print(DFR_pivot)
    friends_pivot = DFR_pivot.loc[DFR_pivot.index.isin(friends_ids)]
    print(friends_pivot)
    friends_mat = csr_matrix(friends_pivot.values)
    print(friends_mat)
    model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
    model_knn.fit(friends_mat)
    # print(friends_pivot.shape[0])
    # index = np.random.choice(friends_pivot.shape[0])
    distances, indices = model_knn.kneighbors(friends_pivot.loc[friends_pivot.index == user_id].values.reshape(1, -1),
                                              n_neighbors=len(friends_pivot))
    print(distances.flatten())
    print(indices)
    for i in range(0, len(distances.flatten())):
        if i == 0:
            print("friends for {0}:\n".format(friends_pivot.index[indices.flatten()[i]]))
        else:
            print("{0}:{1} with distance of {2}".format(i, friends_pivot.index[indices.flatten()[i]],
                                                        distances.flatten()[i]))


def friendship_sim_DF(path, dataset):
    DF, DFUF = read_and_trans_data(path, dataset)
    sum = 0

    data = []
    columns = ['user_id_1', 'user_id_2', 'Deg_Sim']

    for i in range(len(DF.index)):
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

    Final_DF = pn.DataFrame(data, columns=columns)

    freindship = Final_DF.pivot(index='user_id_1', columns='user_id_2', values='Deg_Sim')
    print(Final_DF)
    print(freindship)

    print('Moyonne:', + sum / 114921)
    print(Final_DF.loc[Final_DF['Deg_Sim'] > sum / 114921])

    return Final_DF


def Trust_deg_ex_DF(path, dataset):
    data = []
    columns = ['user_id_1', 'user_id_2', 'Deg_ex_T']
    DF, DFR, DFU = read_and_trans_data(path, dataset)
    column_len = len(DF['user_id'])
    # deg chen & al

    for i in range(column_len):
        user = DF.iloc[i, 0]
        user_rows = DF.loc[DF['user_id'] == user]
        deg_user_plus = len(user_rows)  #
        for j in range(deg_user_plus):
            Trustee = user_rows.iloc[j, 1]
            Trustee_rows_plus = DF.loc[DF['user_id'] == Trustee]
            deg_Trustee_plus = len(Trustee_rows_plus)
            Trustee_rows_minus = DF.loc[DF['Trustee'] == Trustee]
            deg_Trustee_minus = len(Trustee_rows_minus)
            Deg_trust = sqrt(deg_Trustee_minus / (deg_user_plus + deg_Trustee_plus))

            if [user, Trustee, Deg_trust] not in data:
                data.append([user, Trustee, Deg_trust])

    Final_DF = pn.DataFrame(data, columns=columns)
    print(Final_DF)
    np.savetxt(path + 'ex_trust.csv', Final_DF, delimiter='::', fmt='%f')

    return Final_DF


def Trust_deg_imp_DF(path, dataset):
    data = []
    d1 = []
    columns = ['user_id_1', 'user_id_2', 'Deg_imp_T']
    if dataset == 2:
        # yelp
        yelp_users_columns = ['user_id', 'fans', 'average_stars', 'friends', 'vote_funny', 'useful',
                              'vote_cool', 'hot', 'more', 'profile', 'cute', 'list', 'note', 'plain',
                              'cool', 'funny', 'writer', 'photos']
        Data_users = pn.read_csv(path + 'users.csv', delimiter='::',
                                 names=yelp_users_columns, engine='python')

        yelp_reviews_columns = ['user_id', 'item_id', 'rating', 'rating_val']
        Data_reviews = pn.read_csv(path + 'reviews.csv', delimiter='::',
                                   names=yelp_reviews_columns, engine='python')

        DFR = Data_reviews
        DFU = Data_users
    elif dataset == 3:
        FT_users_columns = ['user_id']
        Data_users = pn.read_csv(path + 'users.csv', delimiter='::',
                                 names=FT_users_columns, engine='python')

        FT_ratings_columns = ['user_id', 'item_id', 'rating', 'rating_val']
        Data_ratings = pn.read_csv(path + 'ratings.csv', delimiter='::',
                                   names=FT_ratings_columns, engine='python')
        DFU = Data_users
        DFR = Data_ratings

    DFU = DFU.astype(int)
    DFR = DFR.astype(int)

    column_len = len(DFU['user_id'])
    print(DFU)

    DFR = DFR.pivot(index='user_id', columns='item_id', values='rating_val').fillna(0)
    for i in range(column_len):
        user_1 = DFU.iloc[i, 0]  # user 1
        print(user_1)
        row_user_1 = pn.DataFrame(DFR.iloc[user_1, :])
        row_user_1 = row_user_1.reset_index(drop=False)
        row_user_1.columns = ['item_id', 'rating_val']

        ratings_user_1 = row_user_1.loc[row_user_1['rating_val'] != 0]
        avrg_rating_user1 = ratings_user_1['rating_val']
        avrg_rating_user1 = avrg_rating_user1.mean(axis=0)

        for j in range(column_len):
            user_2 = DFU.iloc[j, 0]  # user 2

            row_user_2 = pn.DataFrame(DFR.iloc[user_2, :])
            row_user_2 = row_user_2.reset_index(drop=False)
            row_user_2.columns = ['item_id', 'rating_val']

            ratings_user_2 = row_user_2.loc[row_user_2['rating_val'] != 0]

            avrg_rating_user2 = ratings_user_2['rating_val']
            avrg_rating_user2 = avrg_rating_user2.mean(axis=0)

            # common
            common_ratings = pn.merge(ratings_user_1, ratings_user_2, how='inner', on='item_id')
            # TOP
            sum1 = 0
            it = NaN
            for k in range(len(common_ratings['item_id'])):
                row = common_ratings.iloc[k]
                rating_val_x = row['rating_val_x']
                rating_val_y = row['rating_val_y']
                p = avrg_rating_user1 + (rating_val_y - avrg_rating_user2)
                sum1 = sum1 + (1 - abs(p - rating_val_x) / 4.0)
            if len(common_ratings['item_id']) > 0:
                it = sum1 / len(common_ratings['item_id'])
            data.append([user_1, user_2, it])
        Final_DF = pn.DataFrame(data, columns=columns)

        print(Final_DF)
        np.savetxt(path + 'imp_trust.csv', Final_DF, delimiter='::', fmt='%f')


def Trust_deg_imp_DF_chen_al(path, dataset):
    global sum1
    data = []
    columns = ['user_id_1', 'user_id_2', 'Deg_imp_T']
    DF, DFR, DFU = read_and_trans_data(path, dataset)
    column_len = len(DF['user_id'])
    print(DFU)
    print(DFR)
    user_1 = DFU.iloc[0, 0]  # user 1
    user_2 = DFU.iloc[2, 0]  # user 2

    DFR = DFR.pivot(index='user_id', columns='item_id', values='rating_val').fillna(0)

    # hash don on doit la trasformer en list puis recreer un dataframe pour etre plis libre
    row_user_1 = pn.DataFrame(DFR.iloc[user_1, :])
    row_user_1 = row_user_1.reset_index(drop=False)
    row_user_1.columns = ['item_id', 'rating_val']

    row_user_2 = pn.DataFrame(DFR.iloc[user_2, :])
    row_user_2 = row_user_2.reset_index(drop=False)
    row_user_2.columns = ['item_id', 'rating_val']

    ratings_user_1 = row_user_1.loc[row_user_1['rating_val'] != 0]
    print(ratings_user_1)
    ratings_user_2 = row_user_2.loc[row_user_2['rating_val'] != 0]
    print(ratings_user_2)

    avrg_rating_user1 = ratings_user_1['rating_val'].sum() / len(ratings_user_1['rating_val'])
    avrg_rating_user2 = ratings_user_2['rating_val'].sum() / len(ratings_user_2['rating_val'])

    print(avrg_rating_user1)
    print(avrg_rating_user2)
    # common
    common_ratings = pn.merge(ratings_user_1, ratings_user_2, how='inner', on='item_id')
    print(common_ratings)
    # TOP
    sum1 = 0
    for i in range(len(common_ratings['item_id'])):
        row = common_ratings.iloc[i]
        rating_val_x = row['rating_val_x']
        rating_val_y = row['rating_val_y']
        sum1 = sum1 + (rating_val_x - avrg_rating_user1) * (rating_val_y - avrg_rating_user2)
    print(sum1)
    # Bottom
    sum2_a = 0
    sum2_b = 0
    for i in range(len(common_ratings['item_id'])):
        row = common_ratings.iloc[i]
        rating_val_x = row['rating_val_x']
        rating_val_y = row['rating_val_y']
        sum2_a = sum2_a + sqrt((rating_val_x - avrg_rating_user1) ** 2)
        sum2_b = sum2_b + sqrt((rating_val_y - avrg_rating_user2) ** 2)

    sum2 = sum2_a * sum2_b
    print("sum2\n", sum2)
    SUM = sum1 / sum2
    print(SUM)
    It = (SUM + 1) / 2
    print(It)


def Trust_imp_ex_DF(path, dataset):
    FT_user_trustee_columns = ['user_1', 'user_2', 'it']
    Data_imp_trust = pn.read_csv(path + 'imp_trust.csv', delimiter='::',
                                 names=FT_user_trustee_columns, engine='python')
    Data_imp_trust.user_1 = Data_imp_trust.user_1.astype(int)
    Data_imp_trust.user_2 = Data_imp_trust.user_2.astype(int)
    print(Data_imp_trust.isna().sum())
    it_pivot = Data_imp_trust.pivot(index='user_1', columns='user_2', values='it')
    print(it_pivot)
    et = Trust_deg_ex_DF(path, dataset)
    print(len(it_pivot))
    for i in range(len(it_pivot)):
        for j in range(len(it_pivot)):
            if i == j:
                it_pivot.iloc[i, j] = it_pivot.iloc[i, j]
            else:
                it_pivot.iloc[i, j] = it_pivot.iloc[i, j] * 0.5

    for i in range(len(et)):
        et_value = et['Deg_ex_T'].iloc[i]
        it_value = it_pivot.iloc[et['user_id_1'].iloc[i], et['user_id_2'].iloc[i]]
        if math.isnan(it_value):
            ct_value = (0.5 * et_value)
        else:

            ct_value = (0.5 * et_value) + it_value
        it_pivot.iloc[et['user_id_1'].iloc[i], et['user_id_2'].iloc[i]] = ct_value

    it_ex_pivot = it_pivot
    print(it_ex_pivot)
    it_ex_pivot = it_ex_pivot.unstack().reset_index(name='value')
    it_ex_pivot.rename(columns={'user_2': 'user_1', 'user_1': 'user_2', 'value': 'it_ex'}, inplace=True)
    print(it_ex_pivot)
    np.savetxt(path + 'imp_ex_trust.csv', it_ex_pivot, delimiter='::', fmt='%f')


if __name__ == '__main__':
    st = time.time()
    opt = int(input("Enter  2)-yelp 3)-Film Trust : "))
    if opt == 3:  # Film Trust
        path = "C:/Users/LATITUDE/Desktop/FILM TRUST Users-Items-Ratings-Trust (csv's)/"
        Trust_deg_imp_DF(path, opt)
    elif opt == 2:  # yelp
        path = "C:/Users/LATITUDE/Desktop/Users-Items-Rating-UF (csv's)/"
        Trust_deg_imp_DF(path, opt)

    print("----%.2f----" % (time.time() - st))
