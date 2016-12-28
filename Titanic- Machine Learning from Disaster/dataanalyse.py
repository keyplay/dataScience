#! python2.7


import numpy as np
import pandas as pd
import re as re

train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')
full_data = [train, test]

print train[['Pclass', 'Survived']].groupby(['Pclass'], as_index=False).mean()

print train[["Sex", "Survived"]].groupby(['Sex'], as_index=False).mean()

for dataset in full_data:
    dataset['FamilySize'] = dataset['SibSp'] + dataset['Parch'] + 1
print train[['FamilySize', 'Survived']].groupby(['FamilySize'], as_index=False).mean()

for dataset in full_data:
    dataset['IsAlone'] = 0
    dataset.loc[dataset['FamilySize'] == 1, 'IsAlone'] = 1
print train[['IsAlone', 'Survived']].groupby(['IsAlone'], as_index=False).mean()

for dataset in full_data:
    dataset['IsAlone'] = 0
    dataset.loc[dataset['FamilySize'] == 1, 'IsAlone'] = 1
print train[['IsAlone', 'Survived']].groupby(['IsAlone'], as_index=False).mean()

for dataset in full_data:
    dataset['Embarked'] = dataset['Embarked'].fillna('S')
print train[['Embarked', 'Survived']].groupby(['Embarked'], as_index=False).mean()
