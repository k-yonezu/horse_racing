import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# data.csvは, rbind_data.csvから余計なrbindを除去したもの
data = pd.read_csv("/Users/nawajieita/Desktop/data.csv")
data = pd.DataFrame(data.iloc[:,1:])

### rank と oddsの散布図と相関
rank_odds_data = data.iloc[:,[1,12]]

# isdigit trueの行番号を抽出
for i in range(len(rank_odds_data.loc[:,'rank'])):
    if i == 0:
        Tisdigit = int(rank_odds_data.loc[i,'rank'].isdigit())
        Tisdigit = list([Tisdigit,Tisdigit])
    else:
        Tisdigit.append(int(rank_odds_data.loc[i,'rank'].isdigit()))
    
Tisdigit = Tisdigit[1:]
Digit = pd.DataFrame({'digit': Tisdigit})
digit_list = Digit.query(' digit == 1').index.tolist()

# データ抽出
rank_odds = rank_odds_data.iloc[digit_list,:]

# NA削除
rank_odds = rank_odds.dropna(how='any')
rank_odds.shape

# 型変換
rank_odds['rank'] = rank_odds.astype(int)

#----- 散布図
plt.figure(facecolor="white", edgecolor="white")
rank_odds.plot.scatter(title='rank-odds scatter plot', x='rank', y='odds')
plt.savefig("/Users/nawajieita/Desktop/競馬予想/horse_racing/figure/scatter_plot/rank-odds.png")
plt.close('all')

#----- 相関係数
ro_cor = pd.DataFrame(rank_odds.corr())
ro_cor.to_csv('/Users/nawajieita/Desktop/競馬予想/horse_racing/csv/rank-odds_cor.csv')

### rank毎のデータ

#----- describe
rank_num = rank_odds.loc[:,'rank'].unique()
rank_num.sort()

for i in range(len(rank_num)):
    # 各要素に合致するindexを抽出
    indexs_ro = rank_odds.query('rank == "%s"' %rank_num[i]).index.tolist()
    
    # csvにまとめる用の要約
    des_ro = rank_odds.loc[indexs_ro,'odds'].describe()
    if i == 0:
        # 最初の一つ目はdataframe化する。
        df_all_ro = pd.DataFrame(pd.Series(des_ro, index=des_ro.index, name=rank_num[i]))
    else:
        # 2つ目以降はdf_allに列結合させる。
        seri = pd.Series(des_ro, index=des_ro.index, name=rank_num[i])
        df_all_ro = pd.concat([df_all_ro, seri], axis=1)

pd.DataFrame(df_all_ro).T.to_csv('/Users/nawajieita/Desktop/競馬予想/horse_racing/csv/odds_par_rank.csv')


#------ ヴァイオリンplot
vp_ro = rank_odds.query('rank == [1,2,3,4,5,6]')
plt.figure(facecolor="white", edgecolor="white")
plt.style.use('default')
sns.set()
sns.set_style('whitegrid')
sns.set_palette('gray')
sns.violinplot(x='rank', y='odds', data=vp_ro)
plt.savefig("/Users/nawajieita/Desktop/競馬予想/horse_racing/figure/scatter_plot/vp_ro_1-6.png")
plt.close('all')

vp_ro = rank_odds.query('rank == [7,8,9,10,11,12]')
plt.figure(facecolor="white", edgecolor="white")
plt.style.use('default')
sns.set()
sns.set_style('whitegrid')
sns.set_palette('gray')
sns.violinplot(x='rank', y='odds', data=vp_ro)
plt.savefig("/Users/nawajieita/Desktop/競馬予想/horse_racing/figure/scatter_plot/vp_ro_7-12.png")
plt.close('all')

vp_ro = rank_odds.query('rank == [13,14,15,16,17,18]')
plt.figure(facecolor="white", edgecolor="white")
plt.style.use('default')
sns.set()
sns.set_style('whitegrid')
sns.set_palette('gray')
sns.violinplot(x='rank', y='odds', data=vp_ro)
plt.savefig("/Users/nawajieita/Desktop/競馬予想/horse_racing/figure/scatter_plot/vp_ro_13-17.png")
plt.close('all')
