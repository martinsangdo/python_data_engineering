# https://www.kaggle.com/code/dansbecker/basic-data-exploration
import pandas as pd
import os

current_directory = os.path.dirname(__file__)

parent_directory = current_directory
for i in range(0, 1):
    parent_directory = os.path.split(parent_directory)[0]


iris_path = parent_directory + '/data/iris.csv';
iris = pd.read_csv(iris_path)
print(iris.head())
print(iris.describe())
