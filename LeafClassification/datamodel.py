#! python2.7
# -*- coding: utf-8 -*-
# datamodel.py - clean the data and train the model.

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV as cc

# read data from files
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')
full_data = [train, test]

# map the species name to numbers
type_mapping = {}
species = train['species'].unique()  # get the list of unique species name
num = 0
for type in species:
    type_mapping[type] = num
    num += 1

train['species'] = train['species'].map(type_mapping).astype(int)    

train.to_csv('trainclean.csv', index=False)
test.to_csv('testclean.csv', index=False)

id = test['id'].values
train = train.drop(['id'], axis = 1)
test = test.drop(['id'], axis = 1)

train = train.values
test  = test.values

# get the training data and label 
X = train[0::, 1::]
y = train[0::, 0]

clf=RandomForestClassifier(n_estimators=1000)
clf = cc(clf, cv=3, method='isotonic')
clf.fit(X, y)  # training the model

print 'done'

# predict the test data
test_predictions = clf.predict_proba(test)   # get the probability of all species
test_predictions = pd.DataFrame(test_predictions)

# map the numbers to species name
type_mapping_inverse = {}
for key, value in type_mapping.items():
    type_mapping_inverse[value] = key
test_predictions.rename(columns=type_mapping_inverse, inplace=True)

test_predictions.sort_index(axis=1, inplace=True)   # sort columns by column name

test_predictions.insert(0, 'id', id)
test_predictions.to_csv('test_predictions.csv', index=False)
