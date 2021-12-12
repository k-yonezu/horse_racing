import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# data.csvは, rbind_data.csvから余計なrbindを除去したもの
data = pd.read_csv("/Users/nawajieita/Desktop/data.csv")
data = pd.DataFrame(data.iloc[:,1:])

data1 = data

# select: odds , odds
odds_rider_data = data1.loc[:, ['odds','rider_id']]

# NA削除
odds_rider = odds_rider_data.dropna(how='any')
odds_rider.shape

# 型変換 -> DataFrame
odds_rider['odds'] = odds_rider['odds'].astype(int)
odds_rider['rider_id'] = odds_rider['rider_id'].astype(int).astype(str)
odds_rider = pd.DataFrame(odds_rider)

# uniqueなrider_id取得 & ソート
ri_uni = list(map(int,odds_rider['rider_id'].unique()))
ri_uni_str = list(map(str, sorted(ri_uni)))

for i in range(len(ri_uni)):
    # 各要素に合致するindexを抽出
    indexs_or = odds_rider.query('rider_id == "%s"' %ri_uni_str[i]).index.tolist()
    
    # csvにまとめる用の要約
    des_or = odds_rider.loc[indexs_or,'odds'].describe()
    if i == 0:
        # 最初の一つ目はdataframe化する。
        df_all_or = pd.DataFrame(pd.Series(des_or, index=des_or.index, name=ri_uni_str[i]))
    else:
        # 2つ目以降はdf_allに列結合させる。
        seri = pd.Series(des_or, index=des_or.index, name=ri_uni_str[i])
        df_all_or = pd.concat([df_all_or, seri], axis=1)

pd.DataFrame(df_all_or).T.to_csv('/Users/nawajieita/Desktop/競馬予想/horse_racing/csv/odds_per_rider_id.csv')

#------ 箱ひげ図

length = len(ri_uni)
#開始位置を指定
n = 0
#分割する変数の個数を指定
s = 5
#配列を指定した個数で分割していくループ処理
nameid = 0
odds_rider_int = odds_rider
odds_rider_int['rider_id'] = odds_rider_int['rider_id'].astype(int)
for i in ri_uni:
    target_list = ri_uni[n:n+s:1]
    box_ro = odds_rider_int.query('rider_id == @target_list')
    box_ro['rider_id'] = box_ro['rider_id'].astype(str)

    # 箱ひげ図を描画
    plt.style.use('default')
    sns.set()
    sns.set_style('whitegrid')
    sns.boxplot(x='rider_id', y='odds', data=box_ro)
    sns.stripplot(x='rider_id', y='odds', data=box_ro, jitter=True, color='black')
    plt.yticks( np.arange(0, 1100, 100) )
    plt.savefig("/Users/nawajieita/Desktop/競馬予想/horse_racing/figure/boxplot/odds_rider/box_plot_%s.png" %str(nameid))
    plt.close('all')

    n += s
    nameid += 1
 
    #カウント数が配列の長さを超えたらループ終了
    if n >= length:
        break