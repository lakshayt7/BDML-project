from sklearn.ensemble import IsolationForest
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn import preprocessing

df = pd.read_csv('combined_data.csv')

train, test = train_test_split(df, test_size=0.2, random_state=42)

clf = IsolationForest(max_samples=100, random_state=42, n_estimators = 100, contamination = 0.1)

y_train = train['label']
y_test = test['label']

X_train = train.drop(columns = ['label']).values
X_test = test.drop(columns = ['label']).values

scaler = preprocessing.StandardScaler().fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)


clf.fit(X_train)
pred = clf.predict(X_test)
label = test['label']

pred = [0 if x < 0 else 1 for x in pred]

target_names = ['class 0', 'class 1']

print(classification_report(label, pred, target_names=target_names))


