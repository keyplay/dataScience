#! python2.7
# -*- coding: utf-8 -*-
# dataAnalyse.py - analyse the data to know which feature should be used in model.

import numpy as np
import pandas as pd
import re as re

# read data from files
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')
full_data = [train, test]

# get relationship between Pclass and Survived
print train[['Pclass', 'Survived']].groupby(['Pclass'], as_index=False).mean()

# get relationship between Sex and Survived
print train[["Sex", "Survived"]].groupby(['Sex'], as_index=False).mean()

# get relationship between FamilySize and Survived
for dataset in full_data:
    # FamilySize is equal to sum of number of siblings/spouses and number of parents/children
    dataset['FamilySize'] = dataset['SibSp'] + dataset['Parch'] + 1
print train[['FamilySize', 'Survived']].groupby(['FamilySize'], as_index=False).mean()

# get relationship between IsAlone and Survived
for dataset in full_data:
    dataset['IsAlone'] = 0
    # if FamilySize is 1, then the passenger is alone
    dataset.loc[dataset['FamilySize'] == 1, 'IsAlone'] = 1
print train[['IsAlone', 'Survived']].groupby(['IsAlone'], as_index=False).mean()

# get relationship between Embarked and Survived
for dataset in full_data:
    dataset['Embarked'] = dataset['Embarked'].fillna('S')
print train[['Embarked', 'Survived']].groupby(['Embarked'], as_index=False).mean()

# get relationship between Fare and Survived
for dataset in full_data:
    # there are some missing data of Fare, so fill them with median number of the whole data
    dataset['Fare'] = dataset['Fare'].fillna(train['Fare'].median())
# classify Fare into 4 range
train['CategoricalFare'] = pd.qcut(train['Fare'], 4)
print train[['CategoricalFare', 'Survived']].groupby(['CategoricalFare'], as_index=False).mean()

# get relationship between Age and Survived
for dataset in full_data:
    # there are missing values in age feature
    # generate random numbers between (mean - std) and (mean + std) 
    age_avg 	   = dataset['Age'].mean()
    age_std 	   = dataset['Age'].std()
    age_null_count = dataset['Age'].isnull().sum()
    
    age_null_random_list = np.random.randint(age_avg - age_std, age_avg + age_std, size=age_null_count)
    dataset['Age'][np.isnan(dataset['Age'])] = age_null_random_list
    dataset['Age'] = dataset['Age'].astype(int)
# categorize age into 5 range   
train['CategoricalAge'] = pd.cut(train['Age'], 5)

print train[['CategoricalAge', 'Survived']].groupby(['CategoricalAge'], as_index=False).mean()

# get title from name
def get_title(name):
    title = re.search('([A-Za-z]+)\.', name)
    if title:
        return title.group(1)
    return ''

# get the distribution of title    
for dataset in full_data:
    dataset['Title'] = dataset['Name'].apply(get_title)
    
print pd.crosstab(train['Title'], train['Sex'])

# get relationship between Title and Survived
for dataset in full_data:
    dataset['Title'] = dataset['Title'].replace(['Lady', 'Countess','Capt', 'Col',\
 	'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')

    dataset['Title'] = dataset['Title'].replace('Mlle', 'Miss')
    dataset['Title'] = dataset['Title'].replace('Ms', 'Miss')
    dataset['Title'] = dataset['Title'].replace('Mme', 'Mrs')

print train[['Title', 'Survived']].groupby(['Title'], as_index=False).mean()
