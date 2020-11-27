import pandas as pd
import os

def read_horse_csv(path):
    df = pd.DataFrame()
    for file in os.listdir(path):
        base, ext = os.path.splitext(file)
        if ext == '.csv' and 'horse' in base:
            df = pd.concat([df, pd.read_csv(path  + file)])
    df['race_id'] = df['race_id'].astype(str)
    df = df.query('not race_id.str.contains("\(", na=False)', engine='python')
    df['race_id'] = df['race_id'].astype(int)
    df = df.reset_index(drop=True)
    return df


def read_race_csv(path):
    df = pd.DataFrame()
    for file in os.listdir(path):
        base, ext = os.path.splitext(file)
        if ext == '.csv' and 'race' in base:
            df = pd.concat([df, pd.read_csv(path  + file)])
    df['race_id'] = df['race_id'].astype(str)
    df = df.query('not race_id.str.contains("\(", na=False)', engine='python')
    df['race_id'] = df['race_id'].astype(int)
    df = df.reset_index(drop=True)
    return df
