from sklearn import datasets, metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
from keras.preprocessing import image
import pandas as pd
import numpy as np
import pickle

train = pd.read_csv('./data.csv')
train_image = []
for i in range(train.shape[0]):
    img = image.load_img(train['image_address'][i])
    img = image.img_to_array(img)
    img = img / 255
    img = np.asarray(img).reshape(-1)
    train_image.append(img)

x = np.array(train_image, dtype=object)
print(x[0].shape)
y = np.array(train['avg_rating'])
print(y.shape)

# get the best linear regression model
best = 0
for _ in range(20):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    linear = LinearRegression()
    linear.fit(x_train, y_train)
    acc = linear.score(x_test, y_test)
    print("Accuracy: " + str(acc))
    
    # step 4: saving model
    # -----------------------------------------------
    # If the current model has a better score than one we've already trained then save it
    if acc > best:
        best = acc
        with open("model.pickle", "wb") as f:
            pickle.dump(linear, f)

# step 5: load the best model
pickle_in = open("model.pickle", "rb")
linear = pickle.load(pickle_in)

predicted= linear.predict(x_test)
for x in range(len(predicted)):
    print(predicted[x], x_test[x], y_test[x])
