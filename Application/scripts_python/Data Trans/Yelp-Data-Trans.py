import numpy as np
import pandas as pn
import codecs
import argparse


def parse_args():
    # DEFAULT PATHS TO CHANGE
    parser = argparse.ArgumentParser(description="Yelp Dataset Processing.")
    parser.add_argument('--users', nargs='?', default='D:/Yelp-data/users.json',
                        help='Input users path.')
    parser.add_argument('--items', nargs='?', default='D:/Yelp-data/restaurants.json',
                        help='Input items path.')
    parser.add_argument('--ratings', nargs='?', default='D:/Yelp-data/reviews.json',
                        help='Input ratings path.')
    parser.add_argument('--path_save', nargs='?', default='D:/Yelp-data/',
                        help='Path to save the train and test data files.')
    return parser.parse_args()


def friends_list(users_str_int, users_init, users_final):
    data = []
    columns = ['user_id', 'friend_id', 'val']  # exp {132,201,1} le user 132 est ami avec le user 201

    col_list = ['user_id', 'friends']
    user_fr_str_list = users_init[col_list]
    for index, row in user_fr_str_list.iterrows():
        if row['friends']:
            int_user_id = Sid_to_Iid(users_str_int, row['user_id'])
            friends_list = row['friends']
            for i in range(len(friends_list)):
                int_friend_id = Sid_to_Iid(users_str_int, friends_list[i])
                if int_friend_id is not None:
                    data.append([int_user_id, int_friend_id, 1])
    friends = pn.DataFrame(data, columns=columns)
    print(friends)
    return friends


def Sid_to_Iid(users_str_int, str_id):
    row_user = users_str_int.loc[users_str_int['user_id_str'] == str_id]
    if row_user.empty:
        id_int = None
    else:
        id_int = row_user.iloc[0, 0]
    return id_int


def transform_users(users):
    data = []

    vote_keys = ['funny', 'useful', 'cool']
    compliment_keys = ['hot', 'more', 'profile', 'cute', 'list', 'note', 'plain',
                       'cool', 'funny', 'writer', 'photos']

    for index, row in users.iterrows():
        # 1 for user_id
        # 1 for nb friends
        # 4 types of votes
        # 11 types of compliment

        vec = np.zeros(16).astype(int)
        vec[0] = row['user_id']

        # number of riends
        vec[1] = len(row['friends'])

        # votes
        i = 2
        for c in vote_keys:
            vec[i] = row['votes'][c]
            i = i + 1

        # compliments

        for c in compliment_keys:
            dict1 = row['compliments']
            if c in dict1.keys():
                vec[i] = dict1[c]
            else:
                vec[i] = 0
            i = i + 1

        data.append(vec)

    columns = ['user_id', 'friends', 'vote_funny', 'useful', 'vote_cool', 'hot', 'more',
               'profile', 'cute', 'list', 'note', 'plain',
               'cool', 'funny', 'writer', 'photos']

    data = pn.DataFrame(data=data, columns=columns)

    users.drop(['name', 'type', 'yelping_since', 'review_count', 'elite', 'friends',
                'votes', 'compliments'], axis=1, inplace=True)

    users = pn.merge(users, data, left_on='user_id', right_on='user_id', how='left')

    return users


def transform_items(items):
    data = []

    attributes_keys = ['Take-out', 'Wi-Fi', 'Good For', 'Caters', 'Noise Level',
                       'Takes Reservations', 'Delivery', 'Ambience', 'Parking', 'Has TV',
                       'Outdoor Seating', 'Attire', 'Alcohol', 'Waiter Service',
                       'Accepts Credit Cards', 'Good for Kids', 'Good For Groups',
                       'Price Range', 'Wheelchair Accessible']

    categories_keys = ['Breakfast & Brunch', 'American (Traditional)', 'Burgers', 'Fast Food',
                       'American (New)', 'Chinese', 'Pizza', 'Italian', 'Sandwiches', 'Sushi Bars', 'Japanese',
                       'Indian', 'Mexican', 'Vietnamese', 'Thai', 'Asian Fusion']

    keys = {
        'Wi-Fi': {'no': 0, 'paid': 1, 'free': 2},
        'Noise Level': {'average': 2, 'quiet': 3, 'loud': 1, 'very_loud': 0},
        'Alcohol': {'none': 0, 'full_bar': 2, 'beer_and_wine': 1},
        'Attire': {'casual': 0, 'dressy': 1, 'formal': 2},
        'Good For': ['dessert', 'latenight', 'lunch', 'dinner', 'breakfast', 'brunch'],
        'Ambience': ['romantic', 'intimate', 'touristy', 'hipster', 'divey', 'classy', 'trendy', 'upscale', 'casual']
    }

    for index, row in items.iterrows():

        vec = np.zeros(49).astype(int)
        vec[0] = row['item_id']

        # Categories
        i = 1
        for c in categories_keys:
            list1 = row['categories']
            if c in list1:
                vec[i] = 1
            i = i + 1

        if i != 17:
            print('ERROR')

        # Attributes
        for c in attributes_keys:
            if c in row['attributes'].keys():
                obj = row['attributes'][c]

                if isinstance(obj, int):
                    vec[i] = obj
                elif isinstance(obj, bool):
                    if obj:
                        vec[i] = 1
                elif isinstance(obj, str):
                    vec[i] = keys[c][obj]
                elif isinstance(obj, dict):
                    if c == 'Parking':
                        if True in obj.values():
                            vec[i] = 1
                    else:
                        i = i - 1
                        for att in keys[c]:
                            i = i + 1
                            if att in obj.keys() and obj[att]:
                                vec[i] = 1
                else:
                    print('error')
                i = i + 1
            else:
                if c == 'Good For' or c == 'Ambience':
                    i = i + len(keys[c])
                else:
                    i = i + 1

        if (i != 49):
            print('ERROR')

        data.append(vec)

    columns = ['item_id', 'Breakfast & Brunch', 'American (Traditional)', 'Burgers', 'Fast Food',
               'American (New)', 'Chinese', 'Pizza', 'Italian', 'Sandwiches', 'Sushi Bars', 'Japanese',
               'Indian', 'Mexican', 'Vietnamese', 'Thai', 'Asian Fusion', 'Take-out', 'Wi-Fi',
               'dessert', 'latenight', 'lunch', 'dinner', 'breakfast', 'brunch', 'Caters',
               'Noise Level', 'Takes Reservations', 'Delivery', 'romantic', 'intimate', 'touristy',
               'hipster', 'divey', 'classy', 'trendy', 'upscale', 'casual',
               'Parking', 'Has TV', 'Outdoor Seating', 'Attire', 'Alcohol', 'Waiter Service',
               'Accepts Credit Cards', 'Good for Kids', 'Good For Groups',
               'Price Range', 'Wheelchair Accessible']

    data = pn.DataFrame(data=data, columns=columns)

    items.drop(['attributes', 'categories', 'full_address',
                'hours', 'name', 'neighborhoods', 'open',
                'review_count', 'stars', 'type'], axis=1, inplace=True)

    items = pn.merge(items, data, left_on='item_id', right_on='item_id', how='left')

    return items


def load_data(users_path, items_path, ratings_path, save):
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

    columns_users = ['user_id', 'fans', 'average_stars', 'friends', 'vote_funny', 'useful', 'vote_cool', 'hot', 'more',
                     'profile', 'cute', 'list', 'note', 'plain',
                     'cool', 'funny', 'writer', 'photos']

    columns_reviews = ['user_id', 'item_id', 'rating', 'rating_val']

    users = pn.read_json(codecs.open(users_path, 'r', 'utf-8'), lines=True)
    items = pn.read_json(codecs.open(items_path, 'r', 'utf-8'), lines=True)
    reviews = pn.read_json(codecs.open(ratings_path, 'r', 'utf-8'), lines=True)

    reviews.rename(columns={"stars": "rating_val", "business_id": "item_id"}, inplace=True)
    items.rename(columns={"business_id": "item_id"}, inplace=True)

    reviews.drop(['date', 'review_id', 'text', 'type', 'votes'], axis=1, inplace=True)
    reviews = reviews.groupby(['user_id', 'item_id'], as_index=False).mean()
    reviews = reviews.assign(rating=1)
    reviews = reviews.drop_duplicates()
    reviews = reviews.reindex(columns=columns_reviews)
    reviews = pn.merge(reviews, users, left_on='user_id', right_on='user_id', how='left')
    reviews = pn.merge(reviews, items, left_on='item_id', right_on='item_id', how='left')
    # ---------------------------------------------------[ID's]---------------------------------------------------------
    # copie ID=>str
    col_list = ['user_id', 'item_id']
    COP_reviews_str_id = reviews.copy()
    COP_reviews_str_id = COP_reviews_str_id[col_list]

    users_str_id = COP_reviews_str_id['user_id']
    users_str_id = users_str_id.drop_duplicates()
    users_str_id = users_str_id.reset_index(drop=True)

    items_str_id = COP_reviews_str_id['item_id']
    items_str_id = items_str_id.drop_duplicates()
    items_str_id = items_str_id.reset_index(drop=True)

    reviews.user_id = reviews.user_id.astype('category').cat.codes.values
    reviews.item_id = reviews.item_id.astype('category').cat.codes.values

    # copie ID=>int
    COP_reviews_int_id = reviews.copy()
    COP_reviews_int_id = COP_reviews_int_id[col_list]

    users_int_id = COP_reviews_int_id['user_id']
    users_int_id = users_int_id.drop_duplicates()
    users_int_id = users_int_id.reset_index(drop=True)

    items_int_id = COP_reviews_int_id['item_id']
    items_int_id = items_int_id.drop_duplicates()
    items_int_id = items_int_id.reset_index(drop=True)
    users_str_int = pn.concat([users_int_id, users_str_id], axis=1)
    users_str_int.columns = ['user_id_int', 'user_id_str']
    items_str_int = pn.concat([items_int_id, items_str_id], axis=1)

    reviews.rename(columns={"review_count_x": "review_count", "name_x": "name", "type_x": "type"}, inplace=True)
    COP_users = users.copy()

    users = reviews.loc[:, users.columns]
    users = transform_users(users)
    users = users.drop_duplicates()
    users = users.reindex(columns=columns_users)
    users = users.sort_values(by=['user_id'])
    users.reset_index(inplace=True, drop=True)
    print('users:\n', users)

    items = reviews.loc[:, items.columns]
    items = transform_items(items)
    items = items.drop_duplicates()
    items = items.reindex(columns=columns_items)
    items = items.sort_values(by=['item_id'])
    items.reset_index(inplace=True, drop=True)
    print('restaurants:\n', items)

    reviews = reviews.loc[:, columns_reviews]
    reviews = reviews.sort_values(by=['user_id', 'item_id'])
    reviews.reset_index(inplace=True, drop=True)
    print('reviews:\n', reviews)

    friends = friends_list(users_str_int, COP_users, users)

    np.savetxt(save + 'restaurants.csv', items, delimiter='::', fmt='%s')
    np.savetxt(save + 'users.csv', users, delimiter='::', fmt='%s')
    np.savetxt(save + 'reviews.csv', reviews, delimiter='::', fmt='%d')
    np.savetxt(save + 'friends.csv', friends, delimiter='::', fmt='%d')


if __name__ == '__main__':
    users_path = 'C:/Users/LATITUDE/Desktop/Datasets/yelp/Yelp-data/users.txt'
    items_path = 'C:/Users/LATITUDE/Desktop/Datasets/yelp/Yelp-data/restaurants.txt'
    ratings_path = 'C:/Users/LATITUDE/Desktop/Datasets/yelp/Yelp-data/reviews.txt'
    save_path = "C:/Users/LATITUDE/Desktop/Users-Items-Rating-UF (csv's)/"

    print('Loading & Processing data...')
    load_data(users_path, items_path, ratings_path, save_path)
    print('Data loaded and processed.')
