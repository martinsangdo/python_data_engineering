# https://www.kaggle.com/code/dansbecker/basic-data-exploration
import pandas as pd
import os
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor  #use many trees. How many?

import calendar
import time


##################
def getCurrentTimestamp():
    return int(calendar.timegm(time.gmtime()))
##################
def basic_model(inputX, y):
    iris_model = DecisionTreeRegressor(random_state=1)
    iris_model.fit(inputX, y)   #define model
    predicted_home_prices = iris_model.predict(inputX)  #little slow, the output is not always correct with data
    mae = mean_absolute_error(y, predicted_home_prices) #Mean Absolute Error
    print(mae)  #0.06799999999  the average difference is 0.067..
##################
def better_model(inputX, y):
    train_X, val_X, train_y, val_y = train_test_split(inputX, y, random_state = 0)   #split data into training and validation data,
    # if random_state = an integer, it produces the same sets. 42 is perfect?
    # Define model
    # iris_model = DecisionTreeRegressor()
    iris_model = DecisionTreeRegressor(max_leaf_nodes=10, random_state=0)
    #loop many nodes to find out how many nodes is the best fit for your model
    #Overfit: good in train set but poor in validation set (many leaves)
    #Underfit: poor in both train & validation sets (less leaves)
# Fit model
    iris_model.fit(train_X, train_y)
    # get predicted prices on validation data
    val_predictions = iris_model.predict(val_X)
    mae = mean_absolute_error(val_y, val_predictions) #0.330    more errors than basic model
    print(mae)
##################
current_directory = os.path.dirname(__file__)

parent_directory = current_directory
for i in range(0, 1):
    parent_directory = os.path.split(parent_directory)[0]


iris_path = parent_directory + '/data/iris.csv'
iris = pd.read_csv(iris_path)
# print(iris.head())
# print(iris.describe())
# print(iris.columns)   #show list of data
# print(iris.Species)   #get data of this column

#features: input of ML model
iris_features = ['SepalLengthCm', 'SepalWidthCm', 'SepalWidthCm']     #do not include non-numeric columns
inputX = iris[iris_features]
# print(input.describe())
#create a Decision Tree
y = iris['PetalWidthCm']    #output of the model
start_time = getCurrentTimestamp()
# basic_model(inputX, y)
better_model(inputX, y)
print(getCurrentTimestamp() - start_time)
