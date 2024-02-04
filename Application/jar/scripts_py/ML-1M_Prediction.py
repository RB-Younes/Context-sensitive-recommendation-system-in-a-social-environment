import math
import pandas as pn
import matplotlib.pyplot as pl
from matplotlib import gridspec
from keras.models import load_model
import time
import argparse
import getpass
import os


def parse_args():
    u = getpass.getuser()
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    parser = argparse.ArgumentParser(description="Prediction ML-1M.")
    parser.add_argument('--path_season', nargs='?', default=os.path.join(script_dir, "ML-1M/"),
                        help='Path of the file containing the item and its season .')
    parser.add_argument('--path_test', nargs='?', default='C:/users/' + u + '/Desktop/',
                        help='Path of the test set.')
    parser.add_argument('--model_path', nargs='?', default='C:/users/' + u + '/Desktop/',
                        help='Path of the trained model.')
    parser.add_argument('--users_sample', type=int, default=10,
                        help='sample of users.')
    parser.add_argument('--Choice_model', type=int, default=2,
                        help='Model choice : 1)-HybMLP 2)-MLP.')
    parser.add_argument('--Context_choice', type=int, default=-1,
                        help='Context_choice: "1")- with context "-1")-without context')
    return parser.parse_args()


# -------------------------------------------------------[ML-1M]--------------------------------------------------------

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


def Context_season(pertinent_item, item_season, result):
    season = item_season.loc[item_season['item_id'] == pertinent_item, 'season'].values[0]
    predicted_filtered = result
    for index, row in result.iterrows():
        id = row['item_id']
        res_season = item_season.loc[item_season['item_id'] == id, 'season'].values[0]
        if season != res_season:
            predicted_filtered = predicted_filtered[predicted_filtered['item_id'] != id]
    return predicted_filtered


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

    pertinent_item = int(final_result.loc[final_result['rating'] == 1, 'item_id'])
    print(pertinent_item)
    print('CF_prediction', final_result)
    return final_result, pertinent_item


def CCF_prediction(test, model, user_id):
    test_un_ID = test[test['user_id'] == user_id]
    test_un_ID = test_un_ID.reset_index(drop=True)

    test_userID = test_un_ID['user_id']
    test_userDATA = test_un_ID[['sexe', 'age', 'occupation']]

    test_itemID = test_un_ID['item_id']
    test_itemDATA = test_un_ID[
        ['Action',
         'Adventure', 'Animation', 'Children\'s', 'Comedy', 'Crime',
         'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical',
         'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']]
    predictions = model.predict([test_userID, test_userDATA, test_itemID, test_itemDATA],
                                verbose=2)
    predictions = pn.DataFrame(data=predictions, columns=['predicted'])
    predictions = pn.concat([test_un_ID, predictions], axis=1)
    final_result = predictions.sort_values(by=['predicted'], ascending=False)

    # add rating column
    test_set_user = test.loc[test['user_id'] == user_id]
    final_result = final_result.assign(rating=0)
    final_result = final_result.reset_index(drop=True)
    pos_row = test_set_user.loc[test_set_user['rating'] == 1]
    final_result.loc[final_result['item_id'] == int(pos_row['item_id']), 'rating'] = 1

    pertinent_item = int(pos_row['item_id'])
    print(pertinent_item)
    print('CCF_prediction', final_result)
    return final_result, pertinent_item


def read_data_load_models(path_test, path_season, model_path, Choice_model):
    if Choice_model == 1:
        model = load_model(model_path + "MODEL HybMLP.h5")
    else:
        model = load_model(model_path + "MODEL MLP.h5")

    movielens_columns = ['user_id', 'item_id', 'rating', 'sexe', 'age', 'occupation', 'Action',
                         'Adventure', 'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama',
                         'Fantasy', 'Film-Noir',
                         'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

    test = pn.read_csv(path_test + 'test.csv', delimiter='::',
                       names=movielens_columns, engine='python')

    item_season_columns = ['item_id', 'season']
    item_season = pn.read_csv(path_season + 'item_season.csv', delimiter='::', encoding='cp1252',
                              names=item_season_columns, engine='python')

    return item_season, test, model


def General_result(test, model, users_sample, item_season, Context_choice):
    all_diffs, all_hrs, all_ndcgs = {}, {}, {}

    for i in range(users_sample):
        if Choice_model == 1:
            final_result, pertinent_item = CCF_prediction(test, model, i)
            if Context_choice == 1:
                result = Context_season(pertinent_item, item_season, final_result)
            else:
                result = final_result
        else:
            final_result, pertinent_item = CF_prediction(test, model, i)
            if Context_choice == 1:
                result = Context_season(pertinent_item, item_season, final_result)
            else:
                result = final_result

        # add rating column
        test_set_user = test.loc[test['user_id'] == i]
        result = result.assign(rating=0)
        result = result.reset_index(drop=True)
        pos_row = test_set_user.loc[test_set_user['rating'] == 1]
        result.loc[result['item_id'] == int(pos_row['item_id']), 'rating'] = 1
        # hit@10 NDCG@10
        r = result.loc[:, 'rating'].head(10)
        hr, ndcg = evaluate_(r)
        # Ecart
        diff = result.loc[result['item_id'] == int(pos_row['item_id']), 'rating'] - result.loc[
            result['item_id'] == int(pos_row['item_id']), 'predicted']

        all_diffs[i], all_hrs[i], all_ndcgs[i] = diff.values[0], hr, ndcg

    return all_diffs, all_hrs, all_ndcgs


if __name__ == '__main__':
    st = time.time()

    args = parse_args()
    path_test = args.path_test
    model_path = args.model_path
    path_season = args.path_season
    users_sample = int(args.users_sample)
    Choice_model = int(args.Choice_model)
    Context_choice = int(args.Context_choice)

    # read data
    item_season, test, model = read_data_load_models(path_test, path_season, model_path, Choice_model)
    diffs, hrs, ndcgs = General_result(test, model, users_sample, item_season, Context_choice)

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

    # manager = pl.get_current_fig_manager()
    # manager.resize(*manager.window.maxsize())
    # script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    # pl.savefig(os.path.join(script_dir, 'P-r-e-s/result.png'))
    pl.show()

    print("----%.2f----" % (time.time() - st))
