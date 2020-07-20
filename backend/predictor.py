from sklearn import datasets, metrics
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing
from keras.preprocessing import image
import pandas as pd
import numpy as np
import pickle
import json


def convert(o):
    if isinstance(o, np.int64): return int(o)  
    raise TypeError


def train():
    data = pd.read_csv('./feature-data.csv')
    x = np.array(data.iloc[:, 4:]) # all features data
    y = np.array(data.iloc[:, 3]) # average rating

    le = preprocessing.LabelEncoder()
    score = le.fit_transform(list(y))
    le_name_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
    print(le_name_mapping)
    le_name_mapping = json.dumps(le_name_mapping, indent=4, separators=(',', ': '), default=convert)
    with open('category_map.json', 'w+') as f:
        f.write(le_name_mapping)

    #TODO: make a json file that match the classname to binary le
    # we're calling that json file after making prediction
    # so that user gets their actual result instead of weird 

    x = list(x)
    y = list(score)

    best = 0
    for _ in range(50):
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)

        model = KNeighborsClassifier(n_neighbors=3)
        model.fit(x_train, y_train)

        acc = model.score(x_test, y_test)
        print("Accuracy: " + str(acc))
  
        # If the current model has a better score, save it
        if acc > best:
            best = acc
            with open("model.pickle", "wb") as f:
                pickle.dump(model, f)


def predict(features: list) -> str:
    pickle_in = open("model.pickle", "rb")
    model = pickle.load(pickle_in)

    features = np.array([features], dtype=object)
    predicted = model.predict(features)

    # match prediction to actual value
    with open('category_map.json', 'r') as f:
        mapper = json.loads(f.read())
        score = list(mapper.keys())[list(mapper.values()).index(predicted[0])]
    return float(score)