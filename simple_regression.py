import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

dataset = pd.read_csv("final.csv")
x = dataset["Faulty Element Count"]
y = dataset["fairnessThroughAwareness"]

data = pd.DataFrame({'x': x, 'y': y})

model = ols("x ~ y", data).fit()
print(model.summary())


offset, coef = model._results.params
plt.plot(x, x*coef + offset)
plt.xlabel('Faulty Element Count')
plt.ylabel('Consistency')

plt.show()