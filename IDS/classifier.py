# -*- coding: utf-8 -*-
  
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.externals import joblib
from sklearn.model_selection import GridSearchCV
import os
import xlrd
from imblearn.over_sampling import RandomOverSampler
from sklearn.cross_validation import train_test_split
from sklearn.externals import joblib


import warnings
from sklearn.model_selection import cross_val_score,cross_val_predict

extraKeys = ['clientPort', 'recList', 'sendList', 'clientIP','serverIP','label','serverPort','sendPlayload','recPlayload','timestmp','sendPort','recPort']

def train():
    black_df = pd.read_csv('scanner.csv')
    black_df['label'] = 'Black'
    http_attack = pd.read_csv('http_attack.csv')
    http_attack['label'] = 'Black'
    white_df = pd.read_csv('white.csv')
    white_df['label'] = 'White'
    data = pd.concat([black_df,white_df])
    X,y = loadTrain(data)
    return X,y

def loadTrain(data):
    data.dropna(inplace=True)    
    all_keys = data.columns
    feature_keys = list(set(all_keys)-set(extraKeys))    
    label = data['label']
    return data[feature_keys],label

def loadExtra():
    df = pd.read_csv('pku.csv')
    all_keys = df.columns
    feature_keys = list(set(all_keys) & set(extraKeys))    
    return df[feature_keys]

def loadReal():
    # df = pd.read_csv('http.csv')
    df = pd.read_csv('pku.csv')
    df['label'] = 'White'
    return loadTrain(df)

x,y = train()
train_X, test_X, train_y, test_y = train_test_split(x,y,test_size=0.3,random_state=0)
rf = RandomForestClassifier()
rf.fit(train_X,train_y)
predicted = rf.predict(test_X)
print(metrics.accuracy_score(test_y, predicted))
print(metrics.confusion_matrix(test_y, predicted))
joblib.dump(rf, "rf.model")
# rf = joblib.load("rf.model")
test_X,test_y = loadReal()
extra = loadExtra()
predicted = rf.predict_proba(test_X)
# predicted = rf.predict(test_X)
# print(metrics.confusion_matrix(test_y, predicted))
print(predicted[0])
for i in range(len(extra)):
    # if predicted[i]=='Black':
        # print(extra.iloc[i, :])
    if predicted[i][0]>0.8:
        print(extra.iloc[i,:])

