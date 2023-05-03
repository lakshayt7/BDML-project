from sklearn.ensemble import IsolationForest
import numpy as np
import pandas as pd

from sklearn.svm import SVC

import xgboost as xgb

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn import preprocessing

from sklearn.manifold import TSNE

df = pd.read_csv('combined_data.csv')

train, test = train_test_split(df, test_size=0.4, random_state=42)


y_train = train['label']
y_test = test['label']

X_train = train.drop(columns = ['label']).values
X_test = test.drop(columns = ['label']).values

print(X_train[0])

scaler = preprocessing.StandardScaler().fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

scale_pos_weight = sum(y_train == 0) / sum(y_train == 1)
scale_pos_weight=scale_pos_weight

xgb_cl = xgb.XGBClassifier(scale_pos_weight = scale_pos_weight)

xgb_cl.fit(X_train, y_train)
pred = xgb_cl.predict(X_test)
label = test['label']

target_names = ['class 0', 'class 1']

print(classification_report(label, pred, target_names=target_names))

clf = SVC(kernel = 'rbf')
clf.fit(X_train, y_train)
pred = clf.predict(X_test)
label = test['label']

target_names = ['class 0', 'class 1']

print(classification_report(label, pred, target_names=target_names))


import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from matplotlib.colors import ListedColormap



# Fit PCA to the training data and transform the data to 2 dimensions
pca = PCA(n_components=2)
X_train_pca = pca.fit_transform(X_train)

fig, ax = plt.subplots()

X_embedded = TSNE(n_components=2, learning_rate='auto', init='random', perplexity=3).fit_transform(X_train)


scatter = plt.scatter(X_train_pca[:,0], X_train_pca[:,1], c=1-y_train, cmap='coolwarm')



plt.legend(handles=scatter.legend_elements()[0], labels= ['Regular data', 'Anomaly'])


# Set the x and y axis labels
plt.xlabel('projected_X')
plt.ylabel('peojected_Y')

plt.title('PCA plot of data for two principle components')

# Show the plot

plt.savefig("/Users/lakshay/Desktop/myimg.svg")
plt.show()





plt.scatter(X_embedded[:,0], X_embedded[:,1], c=y_train, cmap='coolwarm')
plt.colorbar()

# Set the x and y axis labels
plt.xlabel('X')
plt.ylabel('Y')



# Show the plot
#plt.show()
