import time
import pandas as pd
import math
from keras.layers.core import Flatten
from keras.layers import Embedding, Dense, Input
from keras.models import Model
from keras.layers.merge import concatenate
import pickle
import argparse
import getpass
import matplotlib.pyplot as pl
import os

getpass.getuser()


def parse_args():
    u = getpass.getuser()
    parser = argparse.ArgumentParser(description="Training the model.")
    parser.add_argument('--path_save', nargs='?', default='C:/users/' + u + '/Desktop/',
                        help='Path to save the results.')
    parser.add_argument('--model', type=int, default=2,
                        help='Model to train : 1)HybMLP   2)MLP.')
    parser.add_argument('--epochs', type=int, default=1,
                        help='Number of epochs.')
    parser.add_argument('--optimizer_subs', nargs='?', default='adam',
                        help='Specify an optimizer for the submodules : adam, sgd.')
    parser.add_argument('--batch_size', type=int, default=100,
                        help='Batch size.')
    parser.add_argument('--num_layers', type=int, default=5,
                        help='HybMLP number of layers.')
    parser.add_argument('--emb_size_hybmlp', type=int, default=32,
                        help='HybMLP embedding size.')
    parser.add_argument('--emb_size_mlp', type=int, default=32,
                        help='MLP embedding size.')
    parser.add_argument('--num_factors', type=int, default=16,
                        help='Number of predictive factors .')
    parser.add_argument('--num_neg', type=int, default=1,
                        help='Number of negative instances to pair with a positive instance.')
    parser.add_argument('--estop', type=int, default=-1,
                        help='Early Stopping : Enable 1 or plus, Disable -1.')
    parser.add_argument('--path_data', nargs='?', default='C:/users/' + u + '/Desktop/',
                        help='Input trainset and testset folder path.')
    parser.add_argument('--dataset', type=int, default=3,
                        help='Choose a dataset:\n 1)MovieLens 1M    2)Yelp  3)Film Trust.')
    return parser.parse_args()


def load_data(path, dataset):
    if dataset == 1:  # ML_1M
        movielens_columns = ['user_id', 'item_id', 'rating', 'sexe', 'age', 'occupation', 'Action',
                             'Adventure', 'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama',
                             'Fantasy', 'Film-Noir',
                             'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

        trainset = pd.read_csv(path + 'train.csv', delimiter='::',
                               names=movielens_columns, engine='python')

        testset = pd.read_csv(path + 'test.csv', delimiter='::',
                              names=movielens_columns, engine='python')

    elif dataset == 2:  # yelp
        yelp_columns = ['user_id', 'item_id', 'rating', 'fans', 'average_stars', 'friends', 'vote_funny',
                        'useful',
                        'vote_cool', 'hot', 'more',
                        'profile', 'cute', 'list', 'note', 'plain', 'cool', 'funny', 'writer', 'photos',
                        'latitude', 'longitude', 'Breakfast & Brunch', 'American (Traditional)', 'Burgers', 'Fast Food',
                        'American (New)', 'Chinese', 'Pizza', 'Italian', 'Sandwiches', 'Sushi Bars', 'Japanese',
                        'Indian', 'Mexican', 'Vietnamese', 'Thai', 'Asian Fusion', 'Take-out', 'Wi-Fi',
                        'dessert', 'latenight', 'lunch', 'dinner', 'breakfast', 'brunch', 'Caters',
                        'Noise Level', 'Takes Reservations', 'Delivery', 'romantic', 'intimate', 'touristy',
                        'hipster', 'divey', 'classy', 'trendy', 'upscale', 'casual',
                        'Parking', 'Has TV', 'Outdoor Seating', 'Attire', 'Alcohol', 'Waiter Service',
                        'Accepts Credit Cards', 'Good for Kids', 'Good For Groups',
                        'Price Range', 'Wheelchair Accessible']

        trainset = pd.read_csv(path + 'train.csv', delimiter='::',
                               names=yelp_columns, engine='python')
        testset = pd.read_csv(path + 'test.csv', delimiter='::',
                              names=yelp_columns, engine='python')
    elif dataset == 3:  # film trust
        yelp_columns = ['user_id', 'item_id', 'rating']

        trainset = pd.read_csv(path + 'train.csv', delimiter='::',
                               names=yelp_columns, engine='python')

        testset = pd.read_csv(path + 'test.csv', delimiter='::',
                              names=yelp_columns, engine='python')

    num_users = int(max(testset.user_id.max() + 1, trainset.user_id.max() + 1))
    num_items = int(max(testset.item_id.max() + 1, trainset.item_id.max() + 1))

    return trainset, testset, num_users, num_items


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


def save_obj(obj, path):
    with open(path + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def evaluate_model(model, model_name, test, k, dataset):  # k =>number of top items
    if dataset == 2:
        # Yelp
        test_userID = test['user_id']
        test_userDATA = test[['fans', 'average_stars', 'friends', 'vote_funny', 'useful', 'vote_cool', 'hot', 'more',
                              'profile', 'cute', 'list', 'note', 'plain', 'cool', 'funny', 'writer', 'photos']]

        test_itemID = test['item_id']
        test_itemDATA = test.iloc[:, -50:]
    elif dataset == 1:
        # ML-1M
        test_userID = test['user_id']
        test_userDATA = test[['sexe', 'age', 'occupation']]

        test_itemID = test['item_id']
        test_itemDATA = test.iloc[:, -18:]
    else:
        # Film Trust
        test_userID = test['user_id']
        test_userDATA = []

        test_itemID = test['item_id']
        test_itemDATA = []

    if model_name in ['MLP']:
        predictions = model.predict([test_userID, test_itemID], verbose=2)
    else:
        predictions = model.predict([test_userID, test_userDATA, test_itemID, test_itemDATA], verbose=2)

    predictions = pd.DataFrame(data=predictions, columns=['predicted'])
    predictions = pd.concat([test, predictions], axis=1)
    predictions = predictions.sort_values(by=['predicted'], ascending=False)

    users = test.user_id.unique()

    hrs, ndcgs = 0, 0
    for u in users:
        p = predictions[predictions['user_id'] == u].loc[:, 'rating'].head(k)
        hr, ndcg = evaluate_(p)
        hrs = hrs + hr
        ndcgs = ndcgs + ndcg

    mean_hr = hrs / len(users)
    mean_ndcg = ndcgs / len(users)

    return mean_hr, mean_ndcg


def train(model, model_name, train, test, num_epochs, batch, path, dataset,):
    if dataset == 2:
        # Yelp
        train_userID = train['user_id']
        train_userDATA = train[['fans', 'average_stars', 'friends', 'vote_funny', 'useful',
                                'vote_cool', 'hot', 'more', 'profile', 'cute', 'list', 'note', 'plain',
                                'cool', 'funny', 'writer', 'photos']]

        train_itemID = train['item_id']
        train_itemDATA = train[['latitude', 'longitude', 'Breakfast & Brunch',
                                'American (Traditional)', 'Burgers', 'Fast Food', 'American (New)',
                                'Chinese', 'Pizza', 'Italian', 'Sandwiches', 'Sushi Bars', 'Japanese',
                                'Indian', 'Mexican', 'Vietnamese', 'Thai', 'Asian Fusion', 'Take-out',
                                'Wi-Fi', 'dessert', 'latenight', 'lunch', 'dinner', 'breakfast',
                                'brunch', 'Caters', 'Noise Level', 'Takes Reservations', 'Delivery',
                                'romantic', 'intimate', 'touristy', 'hipster', 'divey', 'classy',
                                'trendy', 'upscale', 'casual', 'Parking', 'Has TV', 'Outdoor Seating',
                                'Attire', 'Alcohol', 'Waiter Service', 'Accepts Credit Cards',
                                'Good for Kids', 'Good For Groups', 'Price Range',
                                'Wheelchair Accessible']]

        train_y = train['rating']
    elif dataset == 1:
        # MovieLens
        train_userID = train['user_id']
        train_userDATA = train[['sexe', 'age', 'occupation']]

        train_itemID = train['item_id']
        train_itemDATA = train.iloc[:, -18:]

        train_y = train['rating']
    else:
        train_userID = train['user_id']

        train_itemID = train['item_id']

        train_y = train['rating']

    # intitialisation
    best_hr, best_ndcg = evaluate_model(model, model_name, test, 10, dataset)  # without training
    best_iteration = 0
    all_hrs, all_ndcgs = {}, {}
    all_hrs[0], all_ndcgs[0] = best_hr, best_ndcg
    model.save_weights(path + ' MLP Weights.h5', overwrite=True)
    bad_epochs = 0

    print('\n[----------ENTRAINEMENT' + model_name + ' ----------]\n')
    for epoch in range(1, num_epochs + 1):
        t1 = time.time()
        if model_name in ['MLP']:
            history = model.fit([train_userID, train_itemID], train_y, batch_size=batch, epochs=1, verbose=0,
                                shuffle=True)
        else:
            history = model.fit([train_userID, train_userDATA, train_itemID, train_itemDATA], train_y, batch_size=batch,
                                epochs=1, verbose=0, shuffle=True)

        hr, ndcg = evaluate_model(model, model_name, test, 10, dataset)
        all_hrs[epoch], all_ndcgs[epoch] = hr, ndcg

        if ndcg > best_ndcg:
            best_hr, best_ndcg, best_iteration = hr, ndcg, epoch
            model.save_weights(path + model_name + 'Weights.h5', overwrite=True)
            model.save(path + "MODEL " + model_name + ".h5")
            bad_epochs = 0
        else:
            bad_epochs = bad_epochs + 1
            if bad_epochs == early_stopping:
                break

        t2 = time.time()
        print('Iteration %d [%.2f s]: loss = %.4f, HitR = %.4f, NDCG = %.4f' % (
            epoch, t2 - t1, history.history['loss'][0], hr, ndcg))

    print("Meilleur iteration %d, Meilleur HR = %.4f, Meilleur NDCG = %.4f" % (best_iteration, best_hr, best_ndcg))
    save_obj(all_hrs, path + '  ' + model_name + '  HRs')
    save_obj(all_ndcgs, path + '  ' + model_name + '  NDCGs')

    return all_hrs, all_ndcgs


# create MLP model
def build_MLP_model(emb_size, predictive_factors, num_layers):
    input_userID = Input(shape=[1], name='user_ID')
    input_itemID = Input(shape=[1], name='item_ID')

    user_latent_factors_MLP = emb_size
    item_latent_factors_MLP = emb_size

    user_emb_MLP = Embedding(num_users, user_latent_factors_MLP, name='user_emb_MLP')(input_userID)
    item_emb_MLP = Embedding(num_items, item_latent_factors_MLP, name='item_emb_MLP')(input_itemID)

    flat_u_MLP = Flatten()(user_emb_MLP)
    flat_i_MLP = Flatten()(item_emb_MLP)

    concat_MLP = concatenate([flat_u_MLP, flat_i_MLP])
    layer = concat_MLP
    for l in range(num_layers, 0, -1):
        layer = Dense(predictive_factors * (2 ** (l - 1)), activation='relu', name='layer%d' % (num_layers - l + 1))(
            layer)

    out = Dense(1, activation='sigmoid', name='output')(layer)

    MLP_model = Model([input_userID, input_itemID], out)

    return MLP_model


# create HybMLP model
def build_HybMLP_model(emb_size, predictive_factors, num_layers, dataset):
    input_userID = Input(shape=[1], name='user_ID')
    input_itemID = Input(shape=[1], name='item_ID')

    if dataset == 1:
        # MovieLens
        input_userDATA = Input(shape=[3], name='user_data')
        input_itemDATA = Input(shape=[18], name='item_data')

    elif dataset == 2:
        # Yelp
        input_userDATA = Input(shape=[17], name='user_data')  # de base c 18 columns mais sans l'id c 17
        input_itemDATA = Input(shape=[50], name='item_data')  # de meme 51 columns mais sans l'id c 50

    user_emb_hMLP = Embedding(num_users, emb_size, name='user_emb_hMLP')(input_userID)
    item_emb_hMLP = Embedding(num_items, emb_size, name='item_emb_hMLP')(input_itemID)

    flat_u_hMLP = Flatten()(user_emb_hMLP)
    flat_i_hMLP = Flatten()(item_emb_hMLP)

    concat_hMLP = concatenate([flat_u_hMLP, flat_i_hMLP, input_userDATA, input_itemDATA])
    layer = concat_hMLP
    for l in range(num_layers, 0, -1):
        layer = Dense(predictive_factors * (2 ** (l - 1)), activation='relu', name='layer%d' % (num_layers - l + 1))(
            layer)

    out = Dense(1, activation='sigmoid', name='output')(layer)

    HybMLP_model = Model([input_userID, input_userDATA, input_itemID, input_itemDATA], out)

    return HybMLP_model


if __name__ == "__main__":
    st = time.time()

    args = parse_args()
    path_save = args.path_save
    dataset = args.dataset
    model_to_train = int(args.model)
    # pretrain = int(args.pretrain)
    epochs = args.epochs
    optimizer_subs = args.optimizer_subs.lower()
    emb_size_hmlp = int(args.emb_size_hybmlp)
    emb_size_mlp = args.emb_size_mlp  # check cast
    pred_facts = int(args.num_factors)
    num_neg = int(args.num_neg)
    num_layers = int(args.num_layers)
    early_stopping = int(args.estop)
    path_data = args.path_data
    batch = int(args.batch_size)

    # load data
    trainset, testset, num_users, num_items = load_data(path_data, dataset)
    if model_to_train == 1:
        # train HybMLP
        hMLP = build_HybMLP_model(emb_size_hmlp, pred_facts, num_layers, dataset)
        hMLP.compile(optimizer=optimizer_subs, loss='binary_crossentropy')
        hrs, ndcgs = train(hMLP, 'HybMLP', trainset, testset, epochs, batch, path_save, dataset)
    elif model_to_train == 2:
        # train MLP
        MLP = build_MLP_model(emb_size_mlp, pred_facts, num_layers)
        MLP.compile(optimizer=optimizer_subs, loss='binary_crossentropy')
        hrs, ndcgs = train(MLP, 'MLP', trainset, testset, epochs, batch, path_save, dataset)

        # PLOT

    x1, y1 = zip(*(hrs.items()))
    x2, y2 = zip(*(ndcgs.items()))
    pl.plot(x1, y1, 'ro', linestyle='dashed')

    pl.subplot(211)
    pl.plot(x1, y1, 'ro--', linestyle='dashed')
    pl.title('The results of the training')
    pl.ylabel('HR@10')
    pl.subplot(212)
    pl.plot(x2, y2, 'bd--', linestyle='dashed')
    pl.ylabel('NDCG@10')
    pl.xlabel('Epochs')

    pl.show()

    print("----%.2f----" % (time.time() - st))
