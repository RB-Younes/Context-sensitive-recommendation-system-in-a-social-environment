import math
import time
import pandas as pn
from keras.models import load_model
from geopy.distance import geodesic


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


# collaborative filtering
def CF_CONTEXTE_ML(test_path, model_ML1M_path, path_season):
    model = load_model(model_ML1M_path + "MODEL MLP.h5")

    movielens_columns = ['user_id', 'item_id', 'rating', 'sexe', 'age', 'occupation', 'Action',
                         'Adventure', 'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama',
                         'Fantasy', 'Film-Noir',
                         'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

    testset = pn.read_csv(test_path + 'test.csv', delimiter='::',
                          names=movielens_columns, engine='python')

    item_season = pn.read_csv(path_season + 'item_season.csv', delimiter='::', encoding='cp1252',
                              names=['item_id', 'season'], engine='python')
    number_users = len(testset['user_id'].unique())

    ndcgs = 0
    pos = 0
    neg = 0
    hrs = 0

    for i in range(number_users):
        test_un_ID = testset[testset['user_id'] == i]
        test_un_ID = test_un_ID.reset_index(drop=True)
        test_userID = test_un_ID['user_id']
        test_itemID = test_un_ID['item_id']
        predictions = model.predict([test_userID, test_itemID], verbose=2)
        predictions = pn.DataFrame(data=predictions, columns=['predicted'])
        predictions = pn.concat([test_un_ID, predictions], axis=1)
        predictions = predictions.sort_values(by=['predicted'], ascending=False)

        # add rating column
        test_set_user = testset.loc[testset['user_id'] == i]
        final_result = predictions.assign(rating=0)
        final_result = final_result.reset_index(drop=True)
        pos_row = test_set_user.loc[test_set_user['rating'] == 1]
        final_result.loc[final_result['item_id'] == int(pos_row['item_id']), 'rating'] = 1

        item = pos_row["item_id"].values[0]
        season = item_season.loc[item_season['item_id'] == item, 'season'].values[0]
        predicted_filtered = final_result
        for index, row in final_result.iterrows():
            id = row['item_id']
            res_season = item_season.loc[item_season['item_id'] == id, 'season'].values[0]
            if season != res_season:
                predicted_filtered = predicted_filtered[predicted_filtered['item_id'] != id]
        nbr_items_pos = len(predicted_filtered)
        nbr_items_neg = 100 - nbr_items_pos
        r = predicted_filtered.loc[:, 'rating'].head(10)
        hr, ndcg = evaluate_(r)
        hrs = hrs + hr
        ndcgs = ndcgs + ndcg
        pos = pos + nbr_items_pos
        neg = neg + nbr_items_neg
    mean_pos = pos / number_users
    print('MEAN POS:', mean_pos)
    mean_neg = neg / number_users
    print('MEAN NEG:', mean_neg)
    mean_hr = hrs / number_users
    print('MEAN HR:', mean_hr)
    mean_ndcg = ndcgs / number_users
    print('MEAN NDCG:', mean_ndcg)

    return predicted_filtered, mean_hr, mean_ndcg, mean_pos, mean_neg


def CF_CONTEXTE_YELP(test_path, model_YELP_path, distance):
    model = load_model(model_YELP_path + "MODEL MLP.h5")
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
    testset = pn.read_csv(test_path + 'test.csv', delimiter='::',
                          names=yelp_columns, engine='python')

    number_users = len(testset['user_id'].unique())

    ndcgs = 0
    pos = 0
    neg = 0
    hrs = 0

    for i in range(number_users):
        test_un_ID = testset[testset['user_id'] == i]
        test_un_ID = test_un_ID.reset_index(drop=True)
        test_userID = test_un_ID['user_id']
        test_itemID = test_un_ID['item_id']
        predictions = model.predict([test_userID, test_itemID], verbose=2)
        predictions = pn.DataFrame(data=predictions, columns=['predicted'])
        predictions = pn.concat([test_un_ID, predictions], axis=1)
        predictions = predictions.sort_values(by=['predicted'], ascending=False)

        # add rating column
        test_set_user = testset.loc[testset['user_id'] == i]
        final_result = predictions.assign(rating=0)
        final_result = final_result.reset_index(drop=True)
        pos_row = test_set_user.loc[test_set_user['rating'] == 1]
        final_result.loc[final_result['item_id'] == int(pos_row['item_id']), 'rating'] = 1
        print(final_result)

        item_longitude = pos_row["longitude"].values[0]
        item_latitude = pos_row["latitude"].values[0]
        predicted_filtered = Context_dis(final_result, test_set_user, item_latitude, item_longitude, distance)
        print(predicted_filtered)

        nbr_items_pos = len(predicted_filtered)
        nbr_items_neg = 100 - nbr_items_pos
        r = predicted_filtered.loc[:, 'rating'].head(10)
        hr, ndcg = evaluate_(r)
        hrs = hrs + hr
        ndcgs = ndcgs + ndcg
        pos = pos + nbr_items_pos
        neg = neg + nbr_items_neg
    mean_pos = pos / number_users
    print('MEAN POS:', mean_pos)
    mean_neg = neg / number_users
    print('MEAN NEG:', mean_neg)
    mean_hr = hrs / number_users
    print('MEAN HR:', mean_hr)
    mean_ndcg = ndcgs / number_users
    print('MEAN NDCG:', mean_ndcg)

    return predicted_filtered, mean_hr, mean_ndcg, mean_pos, mean_neg


# content-based collaborative filtering
def CCF_CONTEXTE_ML(path, model_ML1M_path, path_season):
    model_hybMLP = load_model(model_ML1M_path + "MODEL HybMLP.h5")

    movielens_columns = ['user_id', 'item_id', 'rating', 'sexe', 'age', 'occupation', 'Action',
                         'Adventure', 'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama',
                         'Fantasy', 'Film-Noir',
                         'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

    testset = pn.read_csv(path + 'test.csv', delimiter='::',
                          names=movielens_columns, engine='python')

    item_season_columns = ['item_id', 'season']
    item_season = pn.read_csv(path_season + 'item_season.csv', delimiter='::', encoding='cp1252',
                              names=item_season_columns, engine='python')
    number_users = len(testset['user_id'].unique())
    ndcgs = 0
    pos = 0
    neg = 0
    hrs = 0

    for i in range(number_users):
        test_un_ID = testset[testset['user_id'] == i]
        test_un_ID = test_un_ID.reset_index(drop=True)

        test_userID = test_un_ID['user_id']
        test_userDATA = test_un_ID[['sexe', 'age', 'occupation']]

        test_itemID = test_un_ID['item_id']
        test_itemDATA = test_un_ID[
            ['Action',
             'Adventure', 'Animation', 'Children\'s', 'Comedy', 'Crime',
             'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical',
             'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']]
        predictions = model_hybMLP.predict([test_userID, test_userDATA, test_itemID, test_itemDATA],
                                           verbose=2)
        predictions = pn.DataFrame(data=predictions, columns=['predicted'])
        predictions = pn.concat([test_un_ID, predictions], axis=1)
        predictions = predictions.sort_values(by=['predicted'], ascending=False)

        # add rating column
        test_set_user = testset.loc[testset['user_id'] == i]
        final_result = predictions.assign(rating=0)
        final_result = final_result.reset_index(drop=True)
        pos_row = test_set_user.loc[test_set_user['rating'] == 1]
        final_result.loc[final_result['item_id'] == int(pos_row['item_id']), 'rating'] = 1

        item = pos_row["item_id"].values[0]
        season = item_season.loc[item_season['item_id'] == item, 'season'].values[0]
        predicted_filtered = final_result
        for index, row in final_result.iterrows():
            id = row['item_id']
            res_season = item_season.loc[item_season['item_id'] == id, 'season'].values[0]
            if season != res_season:
                predicted_filtered = predicted_filtered[predicted_filtered['item_id'] != id]

        nbr_items_pos = len(predicted_filtered)
        nbr_items_neg = 100 - nbr_items_pos
        r = predicted_filtered.loc[:, 'rating'].head(10)
        hr, ndcg = evaluate_(r)
        hrs = hrs + hr
        ndcgs = ndcgs + ndcg
        pos = pos + nbr_items_pos
        neg = neg + nbr_items_neg
    mean_pos = pos / number_users
    print('MEAN POS:', mean_pos)
    mean_neg = neg / number_users
    print('MEAN NEG:', mean_neg)
    mean_hr = hrs / number_users
    print('MEAN HR:', mean_hr)
    mean_ndcg = ndcgs / number_users
    print('MEAN NDCG:', mean_ndcg)

    return predicted_filtered, mean_hr, mean_ndcg, mean_pos, mean_neg


def CCF_CONTEXTE_YELP(path, model_YELP_path, distance):
    model_hybMLP = load_model(model_YELP_path + "MODEL HybMLP.h5")
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
    testset = pn.read_csv(path + 'test.csv', delimiter='::',
                          names=yelp_columns, engine='python')

    number_users = len(testset['user_id'].unique())

    ndcgs = 0
    pos = 0
    neg = 0
    hrs = 0

    for i in range(number_users):
        test_un_ID = testset[testset['user_id'] == i]
        test_un_ID = test_un_ID.reset_index(drop=True)

        test_userID = test_un_ID['user_id']
        test_userDATA = test_un_ID[
            ['fans', 'average_stars', 'friends', 'vote_funny', 'useful', 'vote_cool', 'hot', 'more',
             'profile', 'cute', 'list', 'note', 'plain', 'cool', 'funny', 'writer', 'photos']]

        test_itemID = test_un_ID['item_id']
        test_itemDATA = test_un_ID[
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
        predictions = pn.concat([test_un_ID, predictions], axis=1)
        predictions = predictions.sort_values(by=['predicted'], ascending=False)

        # add rating column
        test_set_user = testset.loc[testset['user_id'] == i]
        final_result = predictions.assign(rating=0)
        final_result = final_result.reset_index(drop=True)
        pos_row = test_set_user.loc[test_set_user['rating'] == 1]
        final_result.loc[final_result['item_id'] == int(pos_row['item_id']), 'rating'] = 1
        print(final_result)

        item_longitude = pos_row["longitude"].values[0]
        item_latitude = pos_row["latitude"].values[0]
        predicted_filtered = Context_dis(final_result, test_set_user, item_latitude, item_longitude, distance)
        print(predicted_filtered)

        nbr_items_pos = len(predicted_filtered)
        nbr_items_neg = 100 - nbr_items_pos
        r = predicted_filtered.loc[:, 'rating'].head(10)
        hr, ndcg = evaluate_(r)
        hrs = hrs + hr
        ndcgs = ndcgs + ndcg
        pos = pos + nbr_items_pos
        neg = neg + nbr_items_neg
    mean_pos = pos / number_users
    print('MEAN POS:', mean_pos)
    mean_neg = neg / number_users
    print('MEAN NEG:', mean_neg)
    mean_hr = hrs / number_users
    print('MEAN HR:', mean_hr)
    mean_ndcg = ndcgs / number_users
    print('MEAN NDCG:', mean_ndcg)

    return predicted_filtered, mean_hr, mean_ndcg, mean_pos, mean_neg


if __name__ == '__main__':
    dataset = int(input("Train/test Enter 1)-MoveLens1M 2)-yelp: "))
    print('Loading & Processing data...')
    st = time.time()

    if dataset == 1:
        # ML 1M
        MODEL = int(input("Train/test Enter 1)-MLP 2)-HybMLP: "))
        test_path = 'C:/Users/LATITUDE/Desktop/Train & Test Save ml-1M/'
        model_ML1M_path = 'C:/Users/LATITUDE/Desktop/Train & Test Save ml-1M/'
        path_season = 'C:/Users/LATITUDE/Desktop/Datasets/ml-1m/'
        if MODEL == 1:
            CF_CONTEXTE_ML(test_path, model_ML1M_path, path_season)
        if MODEL == 2:
            CCF_CONTEXTE_ML(test_path, model_ML1M_path, path_season)
    elif dataset == 2:
        # yelp
        MODEL = int(input("Train/test Enter 1)-MLP 2)-HybMLP: "))
        test_path = 'C:/Users/LATITUDE/Desktop/Train & Test Save yelp/'
        model_YELP_path = 'C:/Users/LATITUDE/Desktop/Train & Test Save yelp/'
        if MODEL == 1:
            CF_CONTEXTE_YELP(test_path, model_YELP_path, 20)
        if MODEL == 2:
            CCF_CONTEXTE_YELP(test_path, model_YELP_path, 60)

    print('Data loaded and processed.')
    print("----%.2f----" % (time.time() - st))
