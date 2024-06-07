#https://www.w3schools.com/python/python_ml_mean_median_mode.asp
# Mean - The average value
# Median - The mid point value: The median value is the value in the middle, after you have sorted all the values.If there are two numbers in the middle, divide the sum of those numbers by two.
# Mode - The most common value

import numpy
from scipy import stats

def test():
    speed = [99,86,87,88,111,86,103,87,94,78,77,85,86]
    # x = numpy.mean(speed) #89.76923076923077
    # x = numpy.median(speed) #87.0
    x = stats.mode(speed)   #ModeResult(mode=86, count=3)
    print(x)


test()
