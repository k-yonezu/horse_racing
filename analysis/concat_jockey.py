import pandas as pd
import os
from analysis.utils import read_data as ur

# JOCKEY_PATH用のpassを定義する。
def concat_jockey(raw_df, JOCKEY_PATH):
  # race_idとrider_idを連結してユニークキーを作成
  rider_race_raws = []
  for race, rider in zip(raw_df['race_id'], raw_df['rider_id']):
    tmp = str(int(race)) + '_' + str(rider)
    rider_race_raws.append(tmp)
  raw_df['race_rider'] = rider_race_raws


  mean_df = ur.read_jockey_csv(JOCKEY_PATH)
  mean_df = ur.isdigit_race(mean_df)
  # race_idとrider_idを連結してユニークキーを作成
  rider_race_mean = []
  for race, rider in zip(mean_df['race_id'], mean_df['rider_id']):
    tmp = str(int(race)) + '_' + str(rider)
    rider_race_mean.append(tmp)
  mean_df['race_rider'] = rider_race_mean
  mean_df = mean_df.loc[:,['race_rider','mean_rank','mean_odds','counts']]
  print(mean_df)

  df = pd.merge(raw_df, mean_df, on='race_rider', how='left')

  return df
