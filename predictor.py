from sklearn import datasets, metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
from ast import literal_eval
import pandas as pd
import numpy as np
import pickle

col_types = {'retrieved_date': str, 'image_url': str, 'image_encoding': object, 'count_rating': float, 'avg_rating': float}
data = pd.read_csv('data.csv', dtype=col_types)
data = data[['image_encoding', 'avg_rating']]


x = data['image_encoding']


ndarr = []
for arr in x:
    print(arr)
    arr = np.fromstring(arr[1:-1], sep=['\w', '\n'])
    arr = literal_eval(arr)
    print(type(arr))
    ndarr.append(arr)
print(ndarr)

x = np.asarray(ndarr)
print(x.shape)

y = np.array(data['avg_rating'])
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
pickle_in = open("studentgrades.pickle", "rb")
linear = pickle.load(pickle_in)