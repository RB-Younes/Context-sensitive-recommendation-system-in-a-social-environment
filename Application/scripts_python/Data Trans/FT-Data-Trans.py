import numpy as np
import pandas as pn
import scipy.io
import codecs
import time


def read_and_trans_data(rating_path, trust_network_path):
    # -----------------------------------------[ RATING PART ]----------------------------------------------------------

    rating_data = []
    columns = ['user_id', 'item_id', 'rating_val']
    Data = pn.read_csv(rating_path, delimiter='\b', header=None)  # les informations sont sur une seule colonne
    # ratings save csv
    nbr_lignes = len(Data)
    for i in range(nbr_lignes):
        liste = Data.iloc[i, 0].split()
        line_sp = list(map(float, liste))  # split va delimiter mot par mot (donc '1 1 2' devient =>['1', '1', '2'])
        rating_data.append(line_sp)

    ratings = pn.DataFrame(rating_data, columns=columns)
    print(ratings)

    ratings = ratings.groupby(['user_id', 'item_id'], as_index=False).mean()

    # duplicateRowsDF = ratings[ratings.duplicated(['user_id', 'item_id'],keep='first')]

    # j'ai drop le rating pour detecter les doublons      ratings = ratings.drop(['rating'], axis=1)
    ratings = ratings.assign(rating=1)
    ratings = ratings.drop_duplicates()
    ratings = ratings.reset_index(drop=False)
    duplicateRowsDF = ratings[ratings.duplicated(['user_id', 'item_id'], keep='first')]
    print(duplicateRowsDF)

    # users DF length = 1508
    users_list = ratings['user_id'].unique()
    users = pn.DataFrame(users_list, columns=['user_id'])

    # changer les id pour commencer de 0 et faire une copie pour gardes un dictionnaire
    users = users.reset_index(drop=False)
    users_copy = users.copy(deep=True)
    users = users.drop(['user_id'], axis=1)
    users.set_axis(['user_id'], axis='columns', inplace=True)

    # items DF length = 2071
    items_list = ratings['item_id'].unique()
    items = pn.DataFrame(items_list, columns=['item_id'])

    items = items.reset_index(drop=False)
    items_copy = items.copy(deep=True)

    items = items.drop(['item_id'], axis=1)
    items.set_axis(['item_id'], axis='columns', inplace=True)

    # travaille sur les copie
    users_copy = users_copy[['user_id', 'index']]
    users_copy.set_axis(['user_id', 'user_id_V0'], axis='columns', inplace=True)

    items_copy = items_copy[['item_id', 'index']]
    items_copy.set_axis(['item_id', 'item_id_V0'], axis='columns', inplace=True)

    ratings = pn.merge(ratings, users_copy, how='left')
    ratings = pn.merge(ratings, items_copy, how='left')
    # enlever les colonnes ou le id commance par 1
    ratings = ratings.drop(['user_id', 'item_id'], axis=1)
    # ordonner & renomer les colonnes
    ratings = ratings[['user_id_V0', 'item_id_V0', 'rating', 'rating_val']]
    ratings.set_axis(['user_id', 'item_id', 'rating', 'rating_val'], axis='columns', inplace=True)

    # -----------------------------------------[ TRUST PART ]----------------------------------------------------------
    Trust_data = []
    columns = ['user_id', 'Trustee', 'trust_val']
    Data_Trust = pn.read_csv(trust_network_path, delimiter='\b', header=None)

    nbr_lignes = len(Data_Trust)
    for i in range(nbr_lignes):
        liste = Data_Trust.iloc[i, 0].split()
        line_sp = list(map(int, liste))  # Split va delimiter mot par mot (donc '1 1 2' devient =>['1', '1', '2'])
        Trust_data.append(line_sp)

    Trusts = pn.DataFrame(Trust_data, columns=columns)

    # concatener pour changer les id et pour enlver les id qui deborde (NAN)
    Trusts = pn.merge(Trusts, users_copy, how='left')
    Trusts = Trusts.dropna()

    # avoir une copy et renomer ses colonnes pour merge et retrouver les id de la deuxieme colonnes  et les drop
    users_copy_2 = users_copy.copy(deep=True)
    users_copy_2.set_axis(['Trustee', 'user_id_V0_2'], axis='columns', inplace=True)

    Trusts = pn.merge(Trusts, users_copy_2, how='left')
    Trusts = Trusts.dropna()

    # reset l'index et drop lescolonne ou l'id commance par 1
    Trusts = Trusts.reset_index(drop=True)
    Trusts = Trusts.drop(['user_id', 'Trustee'], axis=1)

    # reorder columns
    Trusts = Trusts[['user_id_V0', 'user_id_V0_2', 'trust_val']]
    Trusts.set_axis(['user_id', 'Trustee', 'trust_val'], axis='columns', inplace=True)

    # float values to int
    Trusts.user_id = Trusts.user_id.astype(int)
    Trusts.Trustee = Trusts.Trustee.astype(int)
    Trusts = Trusts.drop_duplicates()
    Trusts = Trusts.reset_index(drop=True)
    print(users)
    print(items)
    print(ratings)
    print(Trusts)

    return users, items, ratings, Trusts


def save_transformed_data(save_path, rating_path, trust_network_path):
    users, items, ratings, Trusts = read_and_trans_data(rating_path, trust_network_path)
    np.savetxt(save_path + 'items.csv', items, delimiter='::', fmt='%s')
    np.savetxt(save_path + 'users.csv', users, delimiter='::', fmt='%s')
    np.savetxt(save_path + 'ratings.csv', ratings, delimiter='::', fmt='%d')
    np.savetxt(save_path + 'trusts.csv', Trusts, delimiter='::', fmt='%d')


if __name__ == '__main__':
    rating_path = "C:/Users/LATITUDE/Desktop/Datasets/filmtrust/ratings.txt"
    trust_network_path = "C:/Users/LATITUDE/Desktop/Datasets/filmtrust/trust.txt"
    save_path = "C:/Users/LATITUDE/Desktop/FILM TRUST Users-Items-Ratings-Trust (csv's)/"

    save_transformed_data(save_path, rating_path, trust_network_path)
