import math

import getpass
import matplotlib.pyplot as pl
from matplotlib import gridspec
import pandas as pn
import numpy as np
from keras.models import load_model
import time
import argparse
import os


def parse_args():
    u = getpass.getuser()
    parser = argparse.ArgumentParser(description="Prediction Film Trust.")
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    parser.add_argument('--path_it_et', nargs='?', default=os.path.join(script_dir, "Film Trust/"),
                        help='Path of implicit and explicit trust values.')
    parser.add_argument('--test_path', nargs='?', default='C:/users/' + u + '/Desktop/',
                        help='Path of the test set.')
    parser.add_argument('--model_path', nargs='?', default='C:/users/' + u + '/Desktop/',
                        help='Path of the trained model.')
    parser.add_argument('--users_sample', type=int, default=10,
                        help='sample of users.')
    parser.add_argument('--Alpha_it_et', type=float, default=0.5,
                        help='implicit and explicit trust ratio.')
    parser.add_argument('--Alpha_combi', type=float, default=0.5,
                        help='Combination ratio.')
    parser.add_argument('--k', type=int, default=5,
                        help='Number of top trusted persons.')
    parser.add_argument('--it_et_bool', type=int, default=1,
                        help='boolean to calculate the prediction of SocF.')
    parser.add_argument('--combination_bool', type=int, default=1,
                        help='boolean to combine CF and SocF .')
    return parser.parse_args()


# ------------------------------------------------------[Film Trust]----------------------------------------------------

def imp_exp_Trust_Ratio(it, et, user_id, Alpha):  # Film trust imp exp ratio

    user_it = it.loc[it['user_1'] == user_id].copy()
    user_et = et.loc[et['user_1'] == user_id].copy()
    user_it.loc[:, 'it'] *= (1 - Alpha)
    user_et.loc[:, 'et'] *= Alpha
    for index, row in user_et.iterrows():
        trustee = row['user_2']
        user_it.loc[user_it['user_2'] == int(trustee), 'it'] += row['et']
    user_it.rename(columns={"user_1": "user_id", "user_2": "trustee", "it": "it_exp"},
                   inplace=True)
    result = user_it.copy()
    print('imp_exp_Trust_Ratio', result)

    return result


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


def SocF_prediction(it_et, user_id, k, test, model):  # Film trust combination with MLP (path, Alpha, user_id,
    # item_set):
    it_et.user_id = it_et.user_id.astype(int)
    it_et.trustee = it_et.trustee.astype(int)
    # get top gens de confiance
    it_ex_piv = it_et.pivot(index='user_id', columns='trustee', values='it_exp')
    it_ex_piv = it_ex_piv.replace(0, np.nan)
    it_ex_piv.iloc[0, user_id] = np.nan
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
            if int(row['trustee']) != user_id:
                user_items_DF = items_DF.assign(user_id=int(row['trustee']))
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
    print('SocF_prediction', final_result)
    return final_result


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


def Combi_CF_SocF(prediction_1, prediction_2, a):
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
        final_result = pn.DataFrame(data=result_data, columns=columns)
    else:
        final_result = prediction_1
    print('Combi_CF_SocF', final_result)
    return final_result


def read_data_load_models(path_it_et, test_path, model_path):
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
    model = load_model(model_path + "MODEL MLP.h5")

    user1_user2_it_columns = ['user_1', 'user_2', 'it']
    it = pn.read_csv(path_it_et + 'imp_trust.csv', delimiter='::',
                     names=user1_user2_it_columns, engine='python')
    it.user_1 = it.user_1.astype(int)
    it.user_2 = it.user_2.astype(int)

    user1_user2_et_columns = ['user_1', 'user_2', 'et']
    et = pn.read_csv(path_it_et + 'ex_prop.csv', delimiter='::',
                     names=user1_user2_et_columns, engine='python')
    et.user_1 = et.user_1.astype(int)
    et.user_2 = et.user_2.astype(int)

    return it, et, test, model


def General_result(it, et, test, model, users_sample, k, it_et_bool, combination_bool, Alpha_combi, Alpha_it_et):
    all_diffs, all_hrs, all_ndcgs = {}, {}, {}

    for i in range(users_sample):
        if it_et_bool == 1:
            it_et = imp_exp_Trust_Ratio(it, et, i, Alpha_it_et)
            SocF_result = SocF_prediction(it_et, i, k, test, model)
            if combination_bool == 1:
                CF_result = CF_prediction(test, model, i)
                final_result = Combi_CF_SocF(CF_result, SocF_result, Alpha_combi)
            else:
                final_result = SocF_result
        else:
            CF_result = CF_prediction(test, model, i)
            final_result = CF_result

        # add rating column
        test_set_user = test.loc[test['user_id'] == i]
        final_result = final_result.assign(rating=0)
        final_result = final_result.reset_index(drop=True)
        pos_row = test_set_user.loc[test_set_user['rating'] == 1]
        final_result.loc[final_result['item_id'] == int(pos_row['item_id']), 'rating'] = 1
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
    path_it_et = args.path_it_et
    test_path = args.test_path
    model_path = args.model_path
    users_sample = int(args.users_sample)
    Alpha_it_et = float(args.Alpha_it_et)
    Alpha_combi = float(args.Alpha_combi)
    k = int(args.k)
    it_et_bool = int(args.it_et_bool)
    combination_bool = int(args.combination_bool)
    # read data
    it, et, test, model = read_data_load_models(path_it_et, test_path, model_path)
    diffs, hrs, ndcgs = General_result(it, et, test, model, users_sample, k, it_et_bool, combination_bool, Alpha_combi,
                                       Alpha_it_et)
    # PLOT

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
