import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.formula.api import ols


def covariance(x, y):
    # Finding the mean of the series x and y
    mean_x = sum(x)/float(len(x))
    mean_y = sum(y)/float(len(y))
    # Subtracting mean from the individual elements
    sub_x = [i - mean_x for i in x]
    sub_y = [i - mean_y for i in y]
    numerator = sum([sub_x[i]*sub_y[i] for i in range(len(sub_x))])
    denominator = len(x)-1
    cov = numerator/denominator
    return cov

def correlation(x, y):
    # Finding the mean of the series x and y
    mean_x = sum(x)/float(len(x))
    mean_y = sum(y)/float(len(y))
    # Subtracting mean from the individual elements
    sub_x = [i-mean_x for i in x]
    sub_y = [i-mean_y for i in y]
    # covariance for x and y
    numerator = sum([sub_x[i]*sub_y[i] for i in range(len(sub_x))])
    # Standard Deviation of x and y
    std_deviation_x = sum([sub_x[i]**2.0 for i in range(len(sub_x))])
    std_deviation_y = sum([sub_y[i]**2.0 for i in range(len(sub_y))])
    # squaring by 0.5 to find the square root
    denominator = (std_deviation_x*std_deviation_y)**0.5 # short but equivalent to (std_deviation_x**0.5) * (std_deviation_y**0.5)
    cor = numerator/denominator
    return cor


dataset = pd.read_csv("final.csv")
x = dataset.loc[dataset["Data Smell Type"] == "Extreme Value Smell", "Faulty Element Count"]
y = dataset["statisticalParity"]

print("covariance = " + str(covariance(x, y)))
print("coorelation = " + str(correlation(x, y)))


data = pd.DataFrame({'x': x, 'y': y})

model = ols("x ~ y", data).fit()
print(model.summary2())


offset, coef = model._results.params
plt.plot(x, x*coef + offset)
plt.xlabel('Faulty Element Count Extreme Value Smell')
plt.ylabel('Statistical Parity')

plt.show()

