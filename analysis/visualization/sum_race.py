import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# data.csvは, rbind_data.csvから余計なrbindを除去したもの
data = pd.read_csv("/Users/nawajieita/Desktop/data.csv")
data = pd.DataFrame(data.iloc[:,1:])

# horse_idのみ抽出
horse_id = pd.DataFrame({'horse_id':data.loc[:,'horse_id'].astype(int).astype(str)})
print(horse_id)

# 馬固有のidを取得
horse_name = horse_id['horse_id'].unique()

indexs = horse_id.query('horse_id == "%s"' %horse_name[0]).index.tolist()

# 馬毎のレース数を取得
for i in range(len(horse_name)):
    # 各要素に合致するindexを抽出
    indexs = horse_id.query('horse_id == "%s"' %horse_name[i]).index.tolist()
    if i % 5000 == 0:
        print("Now i= %s   Total=%s" %(i,len(horse_name)))
    
    # csvにまとめる用の要約
    des = horse_id.loc[indexs,'horse_id'].describe()
    if i == 0:
        # 最初の一つ目はdataframe化する。
        df_all = pd.DataFrame(pd.Series(des, index=des.index, name=horse_name[i]))
    else:
        # 2つ目以降はdf_allに列結合させる。
        seri = pd.Series(des, index=des.index, name=horse_name[i])
        df_all = pd.concat([df_all, seri], axis=1)

# 馬毎のレース数をcsvで書き出す.
sum_race = pd.DataFrame(df_all).T
sum_race = pd.DataFrame(sum_race.loc[:,'count'])
sum_race.to_csv('/Users/nawajieita/Desktop/競馬予想/horse_racing/csv/sum_race.csv')

# 馬全体のレース数のまとめをcsvで書き出す.
des = pd.DataFrame(sum_race.loc[:,'count'].astype(int).describe())
des.to_csv('/Users/nawajieita/Desktop/競馬予想/horse_racing/csv/sum_race_des.csv')
