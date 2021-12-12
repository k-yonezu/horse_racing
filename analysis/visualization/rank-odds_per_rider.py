import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("/Users/nawajieita/Desktop/data.csv")
data = pd.DataFrame(data.iloc[:,1:])

data1 = data

# select: rank, odds, rider
# ror = rank_odds_rider
ror_data = data1.loc[:, ['rank', 'odds', 'rider_id']]

# データ抽出: rankが数値のみのデータを取る
tmp = []
for i in range(len(ror_data.loc[:, 'rank'])):
    tmp.append(int(ror_data.loc[i,'rank'].isdigit()))
Tmp = pd.DataFrame({'T':tmp})
t_only = Tmp.query(' T == 1').index.tolist()
ror = ror_data.iloc[t_only,:]

# NA削除
ror = ror.dropna(how='any')

# 型変換
ror['rank'] = ror['rank'].astype(int)
ror['rider_id'] = ror['rider_id'].astype(int).astype(str)
ror = pd.DataFrame(ror)

# ri=rider_id
ri_uni = list(map(int, ror.loc[:,'rider_id'].unique()))
ri_uni_str = list(map(str, sorted(ri_uni)))

lis_cor = []
counts = []
for j in range(len(ri_uni_str)):
    index = ror.query('rider_id == "%s"' %ri_uni_str[j]).index.tolist()
    rank_odds = ror.loc[index, ['rank', 'odds']]
    ro_cor = rank_odds.corr()
    lis_cor.append(pd.DataFrame(ro_cor).iloc[0,1])
    counts.append(len(rank_odds['odds']))
df_cor = pd.DataFrame(list(zip(lis_cor,counts)), columns = ['cor','counts'], index=ri_uni_str)
df_cor.to_csv("/Users/nawajieita/Desktop/競馬予想/horse_racing/csv/rank-odds_per_rider.csv")
pd.DataFrame(df_cor.describe()).to_csv("/Users/nawajieita/Desktop/競馬予想/horse_racing/csv/rank-odds_per_rider-summary.csv")

#------ 棒グラフ図
 
length = len(ri_uni)
#開始位置を指定
n = 0
#分割する変数の個数を指定
s = 5
#配列を指定した個数で分割していくループ処理
nameid = 0
df_cor['rider_id'] = ri_uni_str
ror_int = df_cor
ror_int['rider_id'] = df_cor['rider_id'].astype(int)
ri_uni = list(map(int, sorted(ri_uni)))
for i in ri_uni:
    target_list = ri_uni[n:n+s:1]
    box_ro = ror_int.query('rider_id == @target_list')
    box_ro['rider_id'] = box_ro['rider_id'].astype(str)

    # 箱ひげ図を描画
    plt.style.use('default')
    sns.set()
    sns.set_style('whitegrid')
    sns.barplot(x='rider_id', y='cor',data=box_ro)
    plt.yticks( np.arange(-1.0, 1.1, 0.1) )
    plt.savefig("/Users/nawajieita/Desktop/競馬予想/horse_racing/figure/barplot/barplot_%s.png" %str(nameid))
    plt.close('all')

    n += s
    nameid += 1
 
    #カウント数が配列の長さを超えたらループ終了
    if n >= length:
        break
