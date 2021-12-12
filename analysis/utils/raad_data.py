
import pandas as pd
import os

def read_horse_csv(path, target_year):
    df = pd.DataFrame()
    df1 = pd.DataFrame()
    for dire in sorted(os.listdir(path)):
        if dire == '.DS_Store' : continue
        for file in sorted(os.listdir(path + '/' + dire)):
            base, ext = os.path.splitext(file)
            if str(target_year+1) in base: break
            if ext == '.csv' and 'horse' in base:
                print(base+ext)
                df = pd.concat([df, pd.read_csv(path + '/' + dire + '/' + file)])
        if str(target_year+1) in base: break

    df1 = df.loc[:,['race_id','rider_id','rank','odds']]

    return df1.reset_index(drop=True)

def add_horse_csv(path, target_year):
    df = pd.DataFrame()
    df1 = pd.DataFrame()
    for dire in sorted(os.listdir(path)):
        #if not df.empty: break
        if dire == '.DS_Store' : continue
        for file in sorted(os.listdir(path + '/' + dire)):
            base, ext = os.path.splitext(file)
            if ext == '.csv' and ('horse-' + str(target_year)) == base:
                print(base+ext)
                df = pd.concat([df, pd.read_csv(path + '/' + dire + '/' + file)])
                break

    df1 = df.loc[:,['race_id','rider_id','rank','odds']]

    return df1.reset_index(drop=True)
