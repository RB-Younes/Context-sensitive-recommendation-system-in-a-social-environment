import numpy as np
import pandas as pn
import scipy.io
import codecs
import time


def read_data(rating_path, trust_network_path):
    rating_mat = scipy.io.loadmat(rating_path)
    rm_data = rating_mat['rating']
    ratings = pn.DataFrame(rm_data, columns=['user_id',
                                             'item_id', 'category', 'rating','helpfulness'])
    ratings.drop(columns=['category', 'helpfulness'], axis=1, inplace=True)
    ratings['rating'] = 1
    ratings = ratings.drop_duplicates()
    ratings.reset_index(inplace=True, drop=True)
    print(ratings)
    # Prendre les users_id
    users = ratings['user_id']
    users = users.drop_duplicates()
    users_df = pn.DataFrame(users, columns=['user_id'])
    users_df.reset_index(inplace=True, drop=True)
    print(users_df)

    # Prendre les users_id
    items = ratings['item_id']
    items = items.drop_duplicates()
    items_df = pn.DataFrame(items, columns=['item_id'])
    items_df.reset_index(inplace=True, drop=True)
    print(items_df)




if __name__ == '__main__':
    rating_path = "C:/Users/LATITUDE/Desktop/Datasets/ciao/rating.mat"
    trust_network_path = "C:/Users/LATITUDE/Desktop/Datasets/ciao/trustnetwork.mat"
    read_data(rating_path, trust_network_path)
