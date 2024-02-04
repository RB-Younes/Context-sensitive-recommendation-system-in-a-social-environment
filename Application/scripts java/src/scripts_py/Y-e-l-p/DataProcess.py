import argparse
import time
import pandas as pd
import numpy as np
import getpass
import os

getpass.getuser()


def parse_args():
    # DEFAULT PATHS TO CHANGE
    parser = argparse.ArgumentParser(description="Datasets Processing.")
    parser.add_argument('--dataset', type=int, default=3,
                        help='Choose a dataset:\n 1)MovieLens 1M  2)Yelp 2013  3)FilmTrust.')
    parser.add_argument('--negs', type=int, default=1,
                        help='Number of negatives per positive instance.')  # 3 for ML-1M  5 for yelp
    u = getpass.getuser()
    parser.add_argument('--path_save', nargs='?', default='C:/users/' + u + '/Desktop/',
                        help='Path to save the train and test data files.')

    return parser.parse_args()


def read_data(users_path, items_path, ratings_path, dataset):
    if dataset == 1:  # ML 1M
        users = pd.read_csv(users_path, delimiter='::', encoding='cp1252',
                            names=['user_id', 'sexe', 'age', 'occupation', 'postal_code'], engine='python')
        users.drop('postal_code', axis=1, inplace=True)
        users.loc[users.sexe == 'F', 'sexe'] = 0
        users.loc[users.sexe == 'M', 'sexe'] = 1

        items = pd.read_csv(items_path, delimiter='::', encoding='cp1252',
                            names=['item_id', 'title', 'genre'], engine='python')
        items.drop('title', axis=1, inplace=True)

        ratings = pd.read_csv(ratings_path, delimiter='::', encoding='cp1252',
                              names=['user_id', 'item_id', 'rating_val', 'timestamp'], engine='python')
        ratings.drop('timestamp', axis=1, inplace=True)
        ratings = ratings.groupby(['user_id', 'item_id'], as_index=False).mean()
        ratings = ratings.assign(rating=1)

        ratings = pd.merge(ratings, users, left_on='user_id', right_on='user_id', how='left')
        ratings = pd.merge(ratings, items, left_on='item_id', right_on='item_id', how='left')

        ratings.user_id = ratings.user_id.astype('category').cat.codes.values
        ratings.item_id = ratings.item_id.astype('category').cat.codes.values

        items = ratings.loc[:, ['item_id', 'genre']]
        items = items.drop_duplicates()
        items = genres_items(items)

        users = ratings.loc[:, ['user_id', 'sexe', 'age', 'occupation']]
        users = users.drop_duplicates()

        ratings = ratings.iloc[:, 0:4]
        print(ratings)
    elif dataset == 2:  # yelp restaurant
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

        columns_users = ['user_id', 'fans', 'average_stars', 'friends', 'vote_funny', 'useful', 'vote_cool', 'hot',
                         'more',
                         'profile', 'cute', 'list', 'note', 'plain',
                         'cool', 'funny', 'writer', 'photos']

        columns_reviews = ['user_id', 'item_id', 'rating', 'rating_val']

        users = pd.read_csv(users_path, delimiter='::', encoding='cp1252',
                            names=columns_users, engine='python')
        items = pd.read_csv(items_path, delimiter='::', encoding='cp1252',
                            names=columns_items, engine='python')
        reviews = pd.read_csv(ratings_path, delimiter='::', encoding='cp1252',
                              names=columns_reviews, engine='python')

        ratings = reviews.loc[:, columns_reviews]

    elif dataset == 3:  # Film trust
        columns_items = ['item_id']

        columns_users = ['user_id']

        columns_reviews = ['user_id', 'item_id', 'rating', 'rating_val']

        users = pd.read_csv(users_path, delimiter='::', encoding='cp1252',
                            names=columns_users, engine='python')
        items = pd.read_csv(items_path, delimiter='::', encoding='cp1252',
                            names=columns_items, engine='python')
        reviews = pd.read_csv(ratings_path, delimiter='::', encoding='cp1252',
                              names=columns_reviews, engine='python')

        ratings = reviews.loc[:, columns_reviews]

    return users, items, ratings


def genres_items(items):  # for ML 1m
    result = []
    for index, row in items.iterrows():
        genre = row['genre']
        vec = np.zeros(19).astype(int)
        vec[0] = row['item_id']
        if 'Action' in genre:
            vec[1] = 1
        if 'Adventure' in genre:
            vec[2] = 1

        if 'Animation' in genre:
            vec[3] = 1

        if 'Children\'s' in genre:
            vec[4] = 1

        if 'Comedy' in genre:
            vec[5] = 1

        if 'Crime' in genre:
            vec[6] = 1

        if 'Documentary' in genre:
            vec[7] = 1

        if 'Drama' in genre:
            vec[8] = 1

        if 'Fantasy' in genre:
            vec[9] = 1

        if 'Film-Noir' in genre:
            vec[10] = 1

        if 'Horror' in genre:
            vec[11] = 1

        if 'Musical' in genre:
            vec[12] = 1

        if 'Mystery' in genre:
            vec[13] = 1

        if 'Romance' in genre:
            vec[14] = 1

        if 'Sci-Fi' in genre:
            vec[15] = 1

        if 'Thriller' in genre:
            vec[16] = 1

        if 'War' in genre:
            vec[17] = 1

        if 'Western' in genre:
            vec[18] = 1

        result.append(vec)
    result = np.vstack(result)

    new_items = pd.DataFrame(data=result,
                             columns=['item_id', 'Action', 'Adventure', 'Animation', 'Children\'s', 'Comedy', 'Crime',
                                      'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery',
                                      'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'], )
    return new_items


def load_data(users_path, items_path, ratings_path, save, num_neg, dataset):
    # read the data
    users, items, ratings = read_data(users_path, items_path, ratings_path, dataset)
    print(users.columns)
    print(items)
    print(ratings.columns)
    # splitting the dataset
    train, test = dataset_split(ratings, num_neg, 99)
    print("--------------------------------------LOAD-------------------------------------------")
    train = pd.merge(train, users, left_on='user_id', right_on='user_id', how='left')
    train = pd.merge(train, items, left_on='item_id', right_on='item_id', how='left')
    print("TRAIN :\n", train)
    print("TRAIN columns:\n", train.columns)

    test = pd.merge(test, users, left_on='user_id', right_on='user_id', how='left')
    test = pd.merge(test, items, left_on='item_id', right_on='item_id', how='left')
    print("TEST :\n", test)
    print("TEST columns:\n", test.columns)

    np.savetxt(save + 'train.csv', train, delimiter='::', fmt='%s')
    np.savetxt(save + 'test.csv', test, delimiter='::', fmt='%s')


def dataset_split(dataset, train_neg, test_neg):  # normal testset (test_neg => nombre d'instance negatives
    # Best_value =99 )
    ratings = dataset.pivot(index='user_id', columns='item_id', values='rating')
    # print(ratings)
    ratings.fillna(0, inplace=True)
    ratings = np.matrix(ratings)
    # print(ratings)

    num_users, num_items = np.shape(ratings)
    # print(num_items)
    # print(num_users)
    # print(num_items)
    # num_items = ratings.shape[1]

    # POSITIVES
    # test
    testpos = []
    indexes = dataset[dataset.user_id == -1].index
    # print(dataset[dataset.user_id == -1].index)
    for u in range(num_users):
        i = np.random.randint(num_items)
        while ratings[u, i] == 0:
            i = np.random.randint(num_items)
        # print("u,i", u, i, ratings[u, i])
        testpos.append([[u, i, 1]])
        indexes = indexes.append(dataset[(dataset.user_id == u) & (dataset.item_id == i)].index)
        # print(dataset[(dataset.user_id == u) & (dataset.item_id == i)])
    testpos = np.vstack(testpos)
    test = pd.DataFrame(data=testpos, columns=['user_id', 'item_id', 'rating'])
    # print("TEST POS \n", test)
    # train
    # print(indexes)
    dataset.drop(indexes, inplace=True)
    train = dataset
    # print("TRAIN POS\n", train)

    # NEGATIVES
    # test

    testneg = []
    for u in range(num_users):
        for num_neg in range(test_neg):
            i = np.random.randint(num_items)
            while ratings[u, i] > 0:
                i = np.random.randint(num_items)
            ratings[u, i] = 1  # <-------Ne pas reprendre les memes valerurs
            testneg.append([[u, i, 0]])
    testneg = pd.DataFrame(data=np.vstack(testneg), columns=['user_id', 'item_id', 'rating'])
    # print("TEST NEG \n", testneg)
    test = test.append(testneg)  # test positif (0-----942) valeur pos pour chaque item) sera en tete du dataset-test
    # et le negative(test_neg(99)x943=93357) a la fin on aura 0-----942-0---------93356
    # c'est pour ca quon doit drop lmancien index et reset un nouveau sur 100%du dataset
    # print("TEST POS+NEG \n", test)
    # generer aleatoirement 100%=1 d dataset   reset l'index et drop l'ancien
    test = test.sample(frac=1).reset_index(drop=True)
    # print("TEST POS+NEG reset index \n", test)

    # train
    trainneg = []
    # print(train.shape[0])  # train.shape[0]= 99057 c'est le nombre d'interaction positif restant apres - le testset
    for x in range(train.shape[0]):  # X  combien d'interaction neg pour une seule pos
        for num_neg in range(train_neg):

            i = np.random.randint(num_items)
            u = np.random.randint(num_users)
            while ratings[u, i] > 0:
                i = np.random.randint(num_items)
            ratings[u, i] = 1
            trainneg.append([[u, i, 0]])

    if trainneg:  # si la valeur n'est pas 0 de train_neg
        trainneg = pd.DataFrame(data=np.vstack(trainneg), columns=['user_id', 'item_id', 'rating'])
        # print("TRAIN NEG\n",trainneg)
        train = train.append(trainneg)
        # print("TRAIN NEG+POS\n", trainneg)
    train = train.sample(frac=1).reset_index(drop=True)
    # print("TRAIN NEG+POS reset index\n", trainneg)
    train = train.drop(columns=['rating_val'])
    return train, test


if __name__ == '__main__':
    st = time.time()
    # opt = int(input("Enter 1)-MoveLens100k 2)-yelp 3)-film trust : "))
    args = parse_args()
    saving_path = args.path_save
    dataset = args.dataset
    num_neg = args.negs

    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

    path_users, path_items, path_ratings = '', '', ''
    if dataset == 1:
        # ML 1M
        path_users  = os.path.join(script_dir, 'ML-1M/users.dat')
        path_items  = os.path.join(script_dir,'ML-1M/movies.dat')
        path_ratings  = os.path.join(script_dir,'ML-1M/ratings.dat')
        # saving_path = 'C:/Users/LATITUDE/Desktop/Train & Test Save ml-100k/'
    elif dataset == 2:
        # yelp 2013
        path_users  = os.path.join(script_dir,"Y-e-l-p/users.csv")
        path_items  = os.path.join(script_dir,"Y-e-l-p/restaurants.csv")
        path_ratings = os.path.join(script_dir,"Y-e-l-p/reviews.csv")
        # saving_path = 'C:/Users/LATITUDE/Desktop/Train & Test Save yelp/'
    elif dataset == 3:
        # film trust
        path_users = os.path.join(script_dir,"Film Trust/users.csv")
        path_items = os.path.join(script_dir,"Film Trust/items.csv")
        path_ratings = os.path.join(script_dir,"Film Trust/ratings.csv")
        # saving_path = 'C:/Users/LATITUDE/Desktop/Train & Test Save film trust/'

    print('Loading & Processing data...')
    # load_data(path_users, path_items, path_ratings, saving_path, 5, dataset)
    load_data(path_users, path_items, path_ratings, saving_path, num_neg, dataset)
    # num_neg yelp=>10 filmtrust=>5 ML100k=>2
    print('Data loaded and processed.')
    print("----%.2f----" % (time.time() - st))
