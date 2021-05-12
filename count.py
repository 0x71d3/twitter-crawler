import csv
from collections import Counter

# import numpy as np
# from sklearn import linear_model
import matplotlib.pyplot as plt

c_len = Counter()

with open('cleaned.tsv', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
    for row in reader:
        c_len[len(row)] += 1

print(c_len)

fig, ax = plt.subplots()

ax.bar(c_len.keys(), c_len.values())

plt.show()

# reg = linear_model.LinearRegression()

# X = np.expand_dims(list(c_len.keys()), axis=1)
# y = np.log(list(c_len.values()))

# reg.fit(X, y)

# fig, ax = plt.subplots()

# ax.plot(X, y, 'o')
# ax.plot(X, reg.predict(X), 'o')

# plt.show()
