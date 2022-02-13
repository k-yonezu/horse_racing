
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

def read_jockey_csv(path):
    for file in sorted(os.listdir(path), reverse=True):
        if file == '.DS_Store' : continue
        df = pd.read_csv(path + '/' + file)
        break
    return df.loc[:, ['race_id', 'rider_id', 'mean_rank', 'mean_odds', 'counts']]

def isdigit_race(data):
    tmp = []
    for _, race in enumerate(data['race_id']):
        tmp.append(str(race).isdigit())
    Tmp = pd.DataFrame({'T': tmp})
    t_only = Tmp.query(' T == 1 ').index.tolist()

    return data.iloc[t_only,:]

def read_horse_csv_for_jockey(path, target_year):
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
