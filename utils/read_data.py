import pandas as pd
import os
import sys


def read_horse_csv(path):
    df = pd.DataFrame()
    for file in os.listdir(path):
        base, ext = os.path.splitext(file)
        if ext == '.csv' and 'horse' in base:
            df = pd.concat([df, pd.read_csv(path  + file)])
    df = df.astype({'race_id': str})
    df = df.query('not race_id.str.contains("\(", na=False)', engine='python')
    df = df.astype({'race_id': float, 'horse_id': int, 'popular': 'float16', 'burden_weight': 'float16', 'frame_number': 'int8', 'horse_number': 'int8', 'total_horse_number': 'int8', 'rider_id': 'int32', 'tamer_id': 'int32', 'last_time': 'float16'})
    df = df.reset_index(drop=True)
    return df


def read_race_csv(path):
    df = pd.DataFrame()
    for file in os.listdir(path):
        base, ext = os.path.splitext(file)
        if ext == '.csv' and 'race' in base:
            df = pd.concat([df, pd.read_csv(path  + file)])
    df = df.astype({'race_id': str})
    df = df.query('not race_id.str.contains("\(", na=False)', engine='python')
    df = df.astype({'race_id': float, 'total_horse_number': 'int8', 'frame_number_first': 'int8', 'horse_number_first': 'int8', 'frame_number_second': 'int8', 'horse_number_second': 'int8', 'frame_number_third': 'int8', 'horse_number_third': 'int8'})
    df = df.reset_index(drop=True)
    return df


def read_horse_race_csv(path):
    df = pd.DataFrame()
    for file in os.listdir(path):
        base, ext = os.path.splitext(file)
        if ext == '.csv' and 'horse_race' in base:
            print(file)
            df = df.append(pd.read_csv(path  + file))
    df = df.astype({'race_id': float, 'horse_id': int})
    df = df.reset_index(drop=True)
    return df


def read_target_horse_csv(path):
    df = pd.DataFrame()
    for file in os.listdir(path):
        base, ext = os.path.splitext(file)
        if ext == '.csv' and 'horse' in base:
            df = pd.concat([df, pd.read_csv(path  + file)])
    df = df.astype({'race_id': float, 'horse_id': int})
    df = df.reset_index(drop=True)
    return df

def read_target_race_csv(path):
    df = pd.DataFrame()
    for file in os.listdir(path):
        base, ext = os.path.splitext(file)
        if ext == '.csv' and 'race' in base:
            df = pd.concat([df, pd.read_csv(path  + file)])
    df = df.astype({'race_id': float})
    df = df.reset_index(drop=True)
    return df
