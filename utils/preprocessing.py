import pandas as pd
import tensorflow as tf
import numpy as np
from tqdm import tqdm

def add_n_race_data(df_race, df_horse, n_race=1):
    res = pd.DataFrame()
    horse_ids = list(set(df_horse['horse_id']))
    df = pd.merge(df_horse, df_race, on='race_id', how='left')
    for horse_id in tqdm(horse_ids):
        df_horse_tmp = df.query('horse_id == @horse_id')
        df_horse_tmp = df_horse_tmp.sort_values("race_id")
        race_ids = list(set(df_horse_tmp['race_id']))
        for race_id in race_ids:
            df_race_tmp = df_horse_tmp.query('race_id == @race_id').reset_index(drop=True)
            df_horse_low_race_id = df_horse_tmp.query('race_id <= @race_id')
            columns = df_horse_low_race_id.columns
            for n in range(1, n_race+1):
                add_columns = list(map(lambda c: c+f"-{n}", columns))
                add_race = df_horse_low_race_id.iloc[-1-n:-n, :].reset_index(drop=True)
                add_race.columns = add_columns
                df_race_tmp = pd.concat([df_race_tmp, add_race], axis=1)
                    
            res = pd.concat([res, df_race_tmp])

    return res


def add_n_race_data_para(df):
    res = pd.DataFrame()
    n_race = 15
    df = df.sort_values("race_id")
    race_ids = list(set(df['race_id']))
    for race_id in race_ids:
        df_race_tmp = df.query('race_id == @race_id').reset_index(drop=True)
        df_horse_low_race_id = df.query('race_id <= @race_id')
        columns = df_horse_low_race_id.columns
        for n in range(1, n_race+1):
            add_columns = list(map(lambda c: c+f"-{n}", columns))
            add_race = df_horse_low_race_id.iloc[-1-n:-n, :].reset_index(drop=True)
            add_race.columns = add_columns
            df_race_tmp = pd.concat([df_race_tmp, add_race], axis=1)

        res = pd.concat([res, df_race_tmp])

    return res
