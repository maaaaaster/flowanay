import os
import lightgbm as lgb
import pandas as pd

def checkData():
    testData = pd.read_csv('ssl_20180827_test.csv')
    filterColumns = ['ConnectKeyID','certHash','serverIP','clientIP','serverName']
    featureColumns = list(set(testData.columns) - set(filterColumns))
    basic = testData[filterColumns]
    features = testData[featureColumns]
    lgbm = lgb.Booster(model_file='model.txt')
    y = lgbm.predict(features)
    for i in range(len(y)):
        print(y[i])
        if y[i] > 0.0005:
            print(basic.iloc[i,:])


if __name__=='__main__':
    checkData()