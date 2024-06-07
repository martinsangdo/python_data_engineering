#https://www.w3schools.com/python/python_ml_mean_median_mode.asp
# Mean - The average value
# Median - The mid point value: The median value is the value in the middle, after you have sorted all the values.If there are two numbers in the middle, divide the sum of those numbers by two.
# Mode - The most common value

import numpy
from scipy import stats
import matplotlib.pyplot as plt

def test():
    speed = [99,86,87,88,111,86,103,87,94,78,77,85,86]
    # x = numpy.mean(speed) #89.76923076923077
    # x = numpy.median(speed) #87.0
    # x = stats.mode(speed)   #ModeResult(mode=86, count=3)

    x = numpy.std(speed)    #
    print(x)

def deviation():
    #Standard deviation is a number that describes how spread out the values are.
    # A low standard deviation means that most of the numbers are close to the mean (average) value.
    # A high standard deviation means that the values are spread out over a wider range.
    speed = [86,87,88,86,87,85,86]
    x = numpy.std(speed)
    print(x)    #0.9035079029052513 most of the values are within the range of 0.9 from the mean value, which is 86.4.

#a number that describes the value that a given percent of the values are lower than
def percentile():
    ages = [5,31,43,48,50,41,7,11,15,39,80,82,32,2,8,6,25,36,27,61,31]
    # x = numpy.percentile(ages, 75)  #The answer is 43, meaning that 75% of the people are 43 or younger.
    x = numpy.percentile(ages, 90)  #61, 90% of the people are 90 or younger
    print(x)

def generate_random():
    x = numpy.random.uniform(0.0, 5.0, 250) #Create an array containing 250 random floats between 0 and 5:
    # print(x)
    plt.hist(x, 5)  #draw 5 bars
    plt.show()
    #The first bar represents how many values in the array are between 0 and 1.
    #The second bar represents how many values are between 1 and 2.

#normal data distribution = Gaussian data distribution (the values are concentrated around a given value)
def normal_data_distribution():
    x = numpy.random.normal(5.0, 1.0, 100000)   #the values should be concentrated around 5.0, and rarely further away than 1.0 from the mean
    plt.hist(x, 100)
    plt.show()

def scatter():
    x = [5,7,8,7,2,17,2,9,4,11,12,9,6]
    y = [99,86,87,88,111,86,103,87,94,78,77,85,86]
    plt.scatter(x, y)   #it needs two arrays of the same length
    plt.show()

scatter()
