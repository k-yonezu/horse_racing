
import pandas as pd
import os

def read_horse_csv(path, target_year):
    df = pd.DataFrame()
    df1 = pd.DataFrame()
    for dire in sorted(os.listdir(path)):
        if dire == '.DS_Store' : continue
        for file in sorted(os.listdir(path + '/' + dire)):
            base, ext = os.path.splitext(file)
            if str(target_year+1) in base: break
            if ext == '.csv' and 'horse' in base:
                print(base+ext)
                df = pd.concat([df, pd.read_csv(path + '/' + dire + '/' + file)])
        if str(target_year+1) in base: break
    
    df1 = df.loc[:,['race_id','rider_id','rank','odds']]
    
    return df1.reset_index(drop=True)

def add_horse_csv(path, target_year):
    df = pd.DataFrame()
    df1 = pd.DataFrame()
    for dire in sorted(os.listdir(path)):
        #if not df.empty: break
        if dire == '.DS_Store' : continue
        for file in sorted(os.listdir(path + '/' + dire)):
            base, ext = os.path.splitext(file)
            if ext == '.csv' and ('horse-' + str(target_year)) == base:
                print(base+ext)
                df = pd.concat([df, pd.read_csv(path + '/' + dire + '/' + file)])
                break
    
    df1 = df.loc[:,['race_id','rider_id','rank','odds']]
    
    return df1.reset_index(drop=True)

def isdigit_rank(data):
    tmp = []
    for i in range(len(data.loc[:,'rank'])):
        tmp.append(int(data.loc[i,'rank'].isdigit()))
    Tmp = pd.DataFrame({'T':tmp})
    f_only = Tmp.query(' T != 1').index.tolist()
    data.loc[f_only,'rank'] = -1

    f_odds = data.query('odds == "---"').index.tolist()
    data.loc[f_odds,'odds'] = 999
    
    return data

def make_mean(data, race_uni):
    df_mean = pd.DataFrame()
    for i, race_num in enumerate(race_uni):
        if i % 1000 == 0: 
            print(i, '残り ', (len(race_uni) - (i+1)))
            print('df_mean shape= ',df_mean.shape, 'data shape= ',data.shape)
        # race_idで要素を抽出
        index_race = data[data["race_id"] == race_num].index.tolist()
        if i == 0:
            df_mean = pd.concat([df_mean, data.loc[index_race,:]])
            df_mean['mean_rank'] = data['rank']
            df_mean['mean_odds'] = data['odds']
            df_mean['counts'] = 1
        else:
            index_race = data[data["race_id"] == race_num].index.tolist()
            riders = list(data.loc[index_race, 'rider_id'])
            #  dataのindexを修正。
            tmp_df = data.iloc[index_race,:].reset_index(drop=True)
            l_rank = []
            l_odds = []
            l_count = []
            diff_rank = []
            diff_odds = []
            for j in range(len(riders)):
                if not (int(riders[j]) in list(map(int, df_mean['rider_id']))):
                    l_rank.append(tmp_df.loc[j,'rank'])
                    l_odds.append(tmp_df.loc[j,'odds'])
                    l_count.append(1)
                    diff_rank.append(tmp_df.loc[j,'rank'])
                    diff_odds.append(tmp_df.loc[j,'odds'])
                else:
                    counts = df_mean.query('rider_id == "%s"' %riders[j]).count()['rider_id']
                    before_rider_index = max(df_mean.query('rider_id == "%s"' %riders[j]).index.tolist())
                    # rankの平均を計算
                    before_mean_rank = df_mean.loc[before_rider_index,'mean_rank']
                    l_rank.append(
                        (before_mean_rank * counts / (counts+1)) + (tmp_df.loc[j,'rank'] / (counts+1))
                    )
                    # oddsの平均を計算
                    before_mean_odds = df_mean.loc[before_rider_index,'mean_odds']
                    l_odds.append(
                        (before_mean_odds * counts / (counts+1)) + (tmp_df.loc[j,'odds'] / (counts+1))
                    )
                    # 参加したレース数を計算
                    l_count.append(int(counts+1))
                    # 直前のレースとの差を計算: race
                    diff_rank.append(tmp_df.loc[j,'rank'] - df_mean.loc[before_rider_index,'rank'])
                    # 直前のレースとの差を計算: odds
                    diff_odds.append(tmp_df.loc[j,'odds'] - df_mean.loc[before_rider_index,'odds'])


            tmp_df['mean_rank'] = l_rank
            tmp_df['mean_odds'] = l_odds
            tmp_df['counts'] = l_count
            tmp_df['diff_rank'] = diff_rank
            tmp_df['diff_odds'] = diff_odds

            #race_id毎にindexをreset
            df_mean = pd.concat([df_mean, tmp_df]).reset_index(drop=True)
    
    return df_mean

def add_mean(df_mean, data, race_uni):
    for i, race_num in enumerate(race_uni):
        if i % 500 == 0: 
            print(i, '残り ', (len(race_uni) - (i+1)))
            print('df_mean shape= ',df_mean.shape, 'data shape= ',data.shape)
        # race_idで要素を抽出
        index_race = data[data["race_id"] == race_num].index.tolist()
        riders = list(data.loc[index_race, 'rider_id'])
        #  dataのindexを修正。
        tmp_df = data.iloc[index_race,:].reset_index(drop=True)
        l_rank = []
        l_odds = []
        l_count = []
        diff_rank = []
        diff_odds = []
        for j in range(len(riders)):
            if not (int(riders[j]) in list(map(int, df_mean['rider_id']))):
                l_rank.append(tmp_df.loc[j,'rank'])
                l_odds.append(tmp_df.loc[j,'odds'])
                l_count.append(1)
                diff_rank.append(tmp_df.loc[j,'rank'])
                diff_odds.append(tmp_df.loc[j,'odds'])
            else:
                counts = df_mean.query('rider_id == "%s"' %riders[j]).count()['rider_id']
                before_rider_index = max(df_mean.query('rider_id == "%s"' %riders[j]).index.tolist())
                # rankの平均を計算
                before_mean_rank = df_mean.loc[before_rider_index,'mean_rank']
                l_rank.append(
                    (before_mean_rank * counts / (counts+1)) + (tmp_df.loc[j,'rank'] / (counts+1))
                )
                # oddsの平均を計算
                before_mean_odds = df_mean.loc[before_rider_index,'mean_odds']
                l_odds.append(
                    (before_mean_odds * counts / (counts+1)) + (tmp_df.loc[j,'odds'] / (counts+1))
                )
                # 参加したレース数を計算
                l_count.append(int(counts+1))
                # 直前のレースとの差を計算: race
                diff_rank.append(tmp_df.loc[j,'rank'] - df_mean.loc[before_rider_index,'rank'])
                # 直前のレースとの差を計算: odds
                diff_odds.append(tmp_df.loc[j,'odds'] - df_mean.loc[before_rider_index,'odds'])

        tmp_df['mean_rank'] = l_rank
        tmp_df['mean_odds'] = l_odds
        tmp_df['counts'] = l_count
        tmp_df['diff_rank'] = diff_rank
        tmp_df['diff_odds'] = diff_odds

        #race_id毎にindexをreset
        df_mean = pd.concat([df_mean, tmp_df]).reset_index(drop=True)
    
    return df_mean