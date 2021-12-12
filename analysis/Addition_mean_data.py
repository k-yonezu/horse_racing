import numpy as np
import pandas as pd
import os
from os.path import join
from dotenv import load_dotenv
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP

import utils.read_data as rd
import utils.calculation_mean_for_jockey as cj

load_dotenv(verbose=True)
dotenv_path = join(Path().resolve(), '.env')
load_dotenv(dotenv_path)
GOOGLE_DRIVE_PATH = os.environ.get("GOOGLE_DRIVE_PATH")

path = GOOGLE_DRIVE_PATH + '/scraping'
target_Y = int(input('Addition year: '))

# 統合する元のデータを読み込む
df = pd.read_csv(GOOGLE_DRIVE_PATH + '/horse_racing/csv/add_mean_horse_race/' + 'add_mean_' + str(target_Y - 1) + '.csv')
df = df.iloc[:,1:]
# 型変換 -> DataFrame
df['rank'] = df['rank'].astype(int)
df['rider_id'] = df['rider_id'].astype(int).astype(str)
df['odds'] = df['odds'].astype(float)
df = pd.DataFrame(df)

# 対象のデータを読み込む
add_df = rd.add_horse_csv(path, target_Y)

# rankとoddsの欠損値補間
add_df = cj.isdigit_rank(add_df)

# 型変換 -> DataFrame
add_df['rank'] = add_df['rank'].astype(int)
add_df['rider_id'] = add_df['rider_id'].astype(int).astype(str)
add_df['odds'] = add_df['odds'].astype(float)
add_df = pd.DataFrame(add_df)

# uniqueなrider_id取得 & ソート
rider_uni = list(map(int,add_df['rider_id'].unique()))
rider_uni_str = list(map(str, sorted(rider_uni)))

# uniqueなrace_id取得
race_uni = list(add_df['race_id'].unique())
print('uni length= ', len(race_uni))

# horse_raceのdataにmean情報を付与する。
concat_df = cj.add_mean(df, add_df, race_uni)
concat_df.to_csv('/Users/nawajieita/Desktop/競馬予想/horse_racing/csv/add_mean_horse_race/add_mean_'+str(target_Y)+'.csv')
print('concat_df= ',concat_df.shape)
