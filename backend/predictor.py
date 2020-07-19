from sklearn import datasets, metrics, linear_model
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, BayesianRidge
from sklearn import preprocessing
from keras.preprocessing import image
import pandas as pd
import numpy as np
import pickle

def image_to_array(img):
    img = image.img_to_array(img)
    img = img / 255
    img = np.asarray(img)
    img = img[:, :, 0] #reduce to a 2D greyscale image
    img = img.reshape(-1)
    return img

def train():
    train = pd.read_csv('./data.csv')
    train_image = []
    for i in range(train.shape[0]):
        img = image.load_img(train['image_address'][i])
        img = image_to_array(img)
        train_image.append(img)

    x = np.array(train_image, dtype=object)
    y = np.array(train['avg_rating'])

    # get the best linear regression model
    best = 0
    for _ in range(20):
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
        # Ridge(alpha-.5) -> -0.2 ish
        # RidgeCV(alphas=np.logspace(-6, 6, 13)) -> 0.06 top
        # LassoLars -> -0.001
        linear = linear_model.LogisticRegression()
        linear.fit(x_train, y_train)
        acc = linear.score(x_test, y_test)
        print("Accuracy: " + str(acc))
        
        # If the current model has a better score than one we've already trained then save it
        if acc > best:
            best = acc
            with open("model.pickle", "wb") as f:
                pickle.dump(linear, f)
#train()
def predict(img):
    # step 5: load the best model
    pickle_in = open("model.pickle", "rb")
    linear = pickle.load(pickle_in)

    img = image_to_array(img)
    img = np.array([img], dtype=object)
    predicted = linear.predict(img)
    return predicted[0]
