#! python2.7
# -*- coding: utf-8 -*-
# datamodel.py - clean the data and train the model.

import pandas as pd
from sklearn.svm import SVC
# read data from files
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')
full_data = [train, test]

type_mapping = {'Ghost': 0, 'Goblin': 1, 'Ghoul': 2}
train['type'] = train['type'].map(type_mapping)    

# find that type is not related to color 
print train[['color', 'type']].groupby(['color'], as_index=False).mean()

id = test['id'].values
train = train.drop(['id', 'color'], axis = 1)
test = test.drop(['id', 'color'], axis = 1)

train.to_csv('trainclean.csv', index=False)
test.to_csv('testclean.csv', index=False)

train = train.values
test  = test.values

X = train[0::, 0:-1]
y = train[0::, -1]

clf = SVC()
clf.fit(X, y)     # training the model

print 'done'

# predict the test data
test_predictions = clf.predict(test)
test_predictions = pd.DataFrame(test_predictions, columns=['type'])

type_mapping = {0: 'Ghost', 1: 'Goblin', 2: 'Ghoul'}
test_predictions['type'] = test_predictions['type'].map(type_mapping)

test_predictions.insert(0, 'id', id)
test_predictions.to_csv('test_predictions.csv', index=False)
