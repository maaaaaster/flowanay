import pandas as pd

def loadFromFile(csv_file):
    df = pd.read_csv(csv_file)
    print(df.groupby('clientIP').size())


if __name__=='__main__':
    loadFromFile('pku.csv')