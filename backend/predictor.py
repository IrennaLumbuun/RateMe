from sklearn import datasets, metrics, linear_model
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, BayesianRidge
from sklearn import preprocessing
from keras.preprocessing import image
import pandas as pd
import numpy as np
import pickle

def train():
    data = pd.read_csv('./feature-data.csv')
    x = np.array(data.iloc[:, 4:]) # all features data
    y = np.array(data.iloc[:, 3]) # average rating

    le = preprocessing.LabelEncoder()
    score = le.fit_transform(list(y))

    #TODO: make a json file that match the classname to binary le
    # we're calling that json file after making prediction
    # so that user gets their actual result instead of weird 

    x = list(x)
    y = list(score)

    best = 0
    for _ in range(20):
        x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)

        model = KNeighborsClassifier(n_neighbors=5)
        model.fit(x_train, y_train)

        acc = model.score(x_test, y_test)
        print("Accuracy: " + str(acc))
        
        # If the current model has a better score, save it
        if acc > best:
            best = acc
            with open("model.pickle", "wb") as f:
                pickle.dump(model, f)

#train()
def predict(features:list) -> str:
    pickle_in = open("model.pickle", "rb")
    model = pickle.load(pickle_in)

    features = np.array([features], dtype=object)
    predicted = model.predict(features)
    return predicted[0]
