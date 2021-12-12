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
target_Y = int(input('target year: '))

df = rd.read_horse_csv(path, target_Y)

# rankとoddsの欠損値補間
df = cj.isdigit_rank(df)

# 型変換 -> DataFrame
df['rank'] = df['rank'].astype(int)
df['rider_id'] = df['rider_id'].astype(int).astype(str)
df['odds'] = df['odds'].astype(float)
df = pd.DataFrame(df)

# uniqueなrider_id取得 & ソート
rider_uni = list(map(int,df['rider_id'].unique()))
rider_uni_str = list(map(str, sorted(rider_uni)))

lmean_rank = []
lmean_odds = []
lcount = []
for i in range(len(rider_uni)):
    # 各要素に合致するindexを抽出
    indexs = df.query('rider_id == "%s"' %rider_uni_str[i]).index.tolist()

    # csvにまとめる用の要約
    lmean_rank.append(Decimal(str(np.mean(df.loc[indexs,'rank']))).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP))
    lmean_odds.append(np.mean(df.loc[indexs,'odds']))
    lcount.append(len(df.loc[indexs,'rank']))

mean_data = pd.DataFrame(
    {
        'rider_id' :rider_uni_str,
        'count'    :lcount,
        'mean_rank':lmean_rank,
        'mean_odds':lmean_odds
    }
)

mean_data.to_csv('/Users/nawajieita/Desktop/競馬予想/horse_racing/csv/mean_rank-odds_'+str(target_Y)+'_rider_id.csv')

# uniqueなrace_id取得
race_uni = list(df['race_id'].unique())
print('uni length= ', len(race_uni))

# horse_raceのdataにmean情報を付与する。
df_mean = cj.make_mean(df,race_uni)

df_mean.to_csv('/Users/nawajieita/Desktop/競馬予想/horse_racing/csv/add_mean_horse_race/add_mean_'+str(target_Y)+'.csv')
print('df_mean', df_mean.shape, 'df', df.shape)
