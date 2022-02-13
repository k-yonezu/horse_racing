import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# data.csvは, rbind_data.csvから余計なrbindを除去したもの
data = pd.read_csv("/Users/nawajieita/Desktop/data.csv")
data = pd.DataFrame(data.iloc[:,1:])

data1 = data

# select: rank , odds
rank_rider_data = data1.loc[:, ['rank','rider_id']]

# isdigit trueの行番号を抽出
tmp = []
for i in range(len(rank_rider_data.loc[:,'rank'])):
        tmp.append(int(rank_rider_data.loc[i,'rank'].isdigit()))
Tmp = pd.DataFrame({'T':tmp})
t_only = Tmp.query(' T == 1').index.tolist()
rank_rider = rank_rider_data.iloc[t_only,:]

# NA削除
rank_rider = rank_rider.dropna(how='any')

# 型変換 -> DataFrame
rank_rider['rank'] = rank_rider['rank'].astype(int)
rank_rider['rider_id'] = rank_rider['rider_id'].astype(int).astype(str)
rank_rider = pd.DataFrame(rank_rider)

# uniqueなrider_id取得 & ソート
rider_id_uni = list(map(int,rank_rider['rider_id'].unique()))
rider_id_uni = list(map(str, sorted(rider_id_uni)))

for i in range(len(rider_id_uni)):
    # 各要素に合致するindexを抽出
    indexs_rr = rank_rider.query('rider_id == "%s"' %rider_id_uni[i]).index.tolist()

    # csvにまとめる用の要約
    des_rr = rank_rider.loc[indexs_rr,'rank'].describe()
    if i == 0:
        # 最初の一つ目はdataframe化する。
        df_all_rr = pd.DataFrame(pd.Series(des_rr, index=des_rr.index, name=rider_id_uni[i]))
    else:
        # 2つ目以降はdf_allに列結合させる。
        seri = pd.Series(des_rr, index=des_rr.index, name=rider_id_uni[i])
        df_all_rr = pd.concat([df_all_rr, seri], axis=1)

pd.DataFrame(df_all_rr).T.to_csv('/Users/nawajieita/Desktop/競馬予想/horse_racing/csv/rank_par_rider_id.csv')

#------ 箱ひげ図

rider_id_uni = list(map(int,rider_id_uni))
length = len(rider_id_uni)
#開始位置を指定
n = 0
#分割する変数の個数を指定
s = 5
#配列を指定した個数で分割していくループ処理
nameid = 0
rank_rider_int = rank_rider
rank_rider_int['rider_id'] = rank_rider_int['rider_id'].astype(int)
for i in rider_id_uni:
    target_list = rider_id_uni[n:n+s:1]
    box_ro = rank_rider_int.query('rider_id == @target_list')
    box_ro['rider_id'] = box_ro['rider_id'].astype(str)

    # 箱ひげ図を描画
    plt.style.use('default')
    sns.set()
    sns.set_style('whitegrid')
    sns.boxplot(x='rider_id', y='rank', data=box_ro)
    sns.stripplot(x='rider_id', y='rank', data=box_ro, jitter=True, color='black')
    plt.yticks( np.arange(0, 20, 1) )
    plt.gca().invert_yaxis()
    plt.savefig("/Users/nawajieita/Desktop/競馬予想/horse_racing/figure/boxplot/rank_rider/box_plot_%s.png" %str(nameid))
    plt.close('all')

    n += s
    nameid += 1

    #カウント数が配列の長さを超えたらループ終了
    if n >= length:
        break
