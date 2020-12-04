import pandas as pd
import tensorflow as tf
import numpy as np

import read_data as rd

def add_n_race_data(df_race, df_horse, n_race=1):
    horse_ids = list(set(df_horse['horse_id']))
    for horse_id in horse_ids:
        df_horse_tmp = df_horse.query('horse_id == @horse_id')
        race_ids = list(set(df_horse_tmp['race_id']))
        for race_id in race_ids:
            df_race_tmp = df_horse_tmp.query('race_id == @race_id')



    df_race_horse = df_race_horse.reset_index(drop=True)
    race_id = df_race_horse.iloc[0, 0]
    df_horse.sort_values("race_id", inplace=True)
    df_hourse = df_horse.query('race_id < @race_id')
    columns = df_horse.columns
    for n in range(1, n_race+1):
        add_columns = list(map(lambda c: c+f"_{n}", columns))
        add_race = df_horse.iloc[-1-n:-n, :].reset_index(drop=True)
        add_race.columns = add_columns
        df_race_horse = pd.concat([df_race_horse, add_race], axis=1)
    return df_race_horse

