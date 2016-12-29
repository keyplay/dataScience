#! python2.7
# -*- coding: utf-8 -*-
# datamodel.py - train the model and predict the test

import pandas as pd
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# read data from files
train = pd.read_csv('trainclean.csv')
test = pd.read_csv('testclean.csv')
train = train.values
test  = test.values

X = train[0::, 1::]
y = train[0::, 0]

clf = SVC()
# train the svc classifier
clf.fit(X, y)
test_predictions = clf.predict(test)
test_predictions = pd.DataFrame(test_predictions, columns=['Survived'])
PassengerId = list(range(892, 892+len(test), 1))

test_predictions.insert(0, 'PassengerId', PassengerId)
test_predictions.to_csv('test_predictions.csv', index=False)
