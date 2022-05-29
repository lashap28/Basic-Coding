import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import datasets
from matplotlib.colors import ListedColormap
import risk_knn as rk

cmap = ListedColormap(['#FF0000', '#00FF00', '0000FF'])
iris = datasets.load_iris()
X, y = iris.data, iris.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=0)


clf = rk.KNN()

clf.fit(X_train, y_train)
pred = clf.predict(X_test)

acc = np.sum(pred == y_test) / len(y_test)

figure, axis = plt.subplots(2, 1)
axis[0].scatter(X_train[:, 0], X_train[:, 1], c=y_train)
axis[0].scatter(X_test[:, 0], X_test[:, 1], marker='^', s=200)
axis[0].set_title("Actual")

axis[1].scatter(X_test[:, 0], X_test[:, 1], c=pred, marker='^',s=200)
axis[1].scatter(X_train[:, 0], X_train[:, 1], c=y_train)
axis[1].set_title("Predicted")
plt.show()
