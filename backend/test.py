"""
This file just calls on existing data, do some analysis and put to csv file
"""

from face import get_features
import pandas as pd
import numpy as np
import csv
import sklearn
from sklearn import linear_model, preprocessing
from sklearn.neighbors import KNeighborsClassifier
import pickle

def write_to_csv():
    data = pd.read_csv('./data.csv')
    url_list = np.array(data['image_url'])
    rating_list = np.array(data['avg_rating'])

    f = open('feature-data.csv', 'w')
    writer = csv.writer(f)

    for i in range(0, len(url_list)):
        feature_list = get_features(url_list[i])
        if feature_list == []:
            continue
        feature_list.append(round(rating_list[i] * 2) / 2)
        writer.writerow(feature_list)


def train():
    data = pd.read_csv('./feature-data.csv')
    x = np.array(data.iloc[:, :7])
    y = np.array(data.iloc[:, 7])

    le = preprocessing.LabelEncoder()
    score = le.fit_transform(list(y))

    x = list(x)
    y = list(score)

    best = 0
    for _ in range(20):
        x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)

        model = KNeighborsClassifier(n_neighbors=5)
        model.fit(x_train, y_train)

        acc = model.score(x_test, y_test)
        print("Accuracy: " + str(acc))
        
        # step 4: saving model
        # -----------------------------------------------
        # If the current model has a better score than one we've already trained then save it
        if acc > best:
            best = acc
            with open("model2.pickle", "wb") as f:
                pickle.dump(model, f)

    # step 5: load the best model
    pickle_in = open("model2.pickle", "rb")
    model = pickle.load(pickle_in)

    predicted = model.predict(x_test)
    for x in range(len(predicted)):
        print(predicted[x], y_test[x])

train()