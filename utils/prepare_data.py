import pandas as pd
import numpy as np
import utils.preprocessing as pp

# 学習に使用するカラム、過去データは3レース前までのデータを用いる
# これらのカラムに対して加工を行う為、新たなカラムが加わる。
# その為、最終的に用いる特徴量のカラムは別な変数で定義する(columns_after_processing)
columns_before_processing = ["race_course", "weather", "ground_status", 
           "where_racecourse", "race_class", "running_condition", 
           "frame_number", "horse_number",
           "sex_and_age", "burden_weight", "rider_id", 
           "tamer_id", "horse_weight", "odds", "popular",
           "rank", "total_horse_number_x", 
           "rank-1", "rank-2", "rank-3",
           "total_horse_number_x-1", "total_horse_number_x-2","total_horse_number_x-3",
           "goal_time-1", "goal_time-2", "goal_time-3",
           "last_time-1", "last_time-2", "last_time-3", 
           "half_way_rank-1", "half_way_rank-2", "half_way_rank-3", 
           "prize-1", "prize-2", "prize-3"]

columns_after_processing = ["race_course", "weather", "ground_status", 
                 "where_racecourse", "race_class", "running_condition", 
                 "frame_number", "horse_number",
                 "sex", "age", "burden_weight", "rider_id", 
                 "tamer_id", "horse_weight", "popular",
                 "rank-1", "rank-2", "rank-3", "odds", 
                 "goal_time-1", "goal_time-2", "goal_time-3",
                 "last_time-1", "last_time-2", "last_time-3", 
                 "kyakusitu-1", "kyakusitu-2", "kyakusitu-3", 
                 "prize-1", "prize-2", "prize-3", "label"]

def prepare_train_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    生データを学習用のデータに加工する
    
    Parameters
    ----------
    raw_df : pandas.DataFrame
        生データのデータフレーム
    
    Returns
    -------
    df_for_learning : pandas.DataFrame
        学習用データ
    """
    df_for_learning = raw_df[columns_before_processing]
    df_for_learning ["where_racecourse"] = df_for_learning ["where_racecourse"].map(pp.extract_place)

    df_for_learning["sex"] = df_for_learning["sex_and_age"].map(lambda sex_and_age: sex_and_age[0])
    df_for_learning["age"] = df_for_learning["sex_and_age"].map(lambda sex_and_age: sex_and_age[1:])
    
    df_for_learning["goal_time-1"] = df_for_learning["goal_time-1"].map(pp.to_seconds)
    df_for_learning["goal_time-2"] = df_for_learning["goal_time-2"].map(pp.to_seconds)
    df_for_learning["goal_time-3"] = df_for_learning["goal_time-3"].map(pp.to_seconds)
    
    df_for_learning["horse_weight"] = df_for_learning["horse_weight"].map(pp.extract_weight).astype(np.int64)
    
    df_for_learning["prize-1"] = df_for_learning["prize-1"].map(lambda prize: prize.replace(",", "") if type(prize) == str else prize).astype(np.float64)
    df_for_learning["prize-2"] = df_for_learning["prize-2"].map(lambda prize: prize.replace(",", "") if type(prize) == str else prize).astype(np.float64)
    df_for_learning["prize-3"] = df_for_learning["prize-3"].map(lambda prize: prize.replace(",", "") if type(prize) == str else prize).astype(np.float64)
    
    df_for_learning["kyakusitu-1"] = [pp.kyakusitu_code_c(n, r) for n, r in zip(df_for_learning["total_horse_number_x-1"].values, df_for_learning["half_way_rank-1"])]
    df_for_learning["kyakusitu-2"] = [pp.kyakusitu_code_c(n, r) for n, r in zip(df_for_learning["total_horse_number_x-2"].values, df_for_learning["half_way_rank-2"])]
    df_for_learning["kyakusitu-3"] = [pp.kyakusitu_code_c(n, r) for n, r in zip(df_for_learning["total_horse_number_x-3"].values, df_for_learning["half_way_rank-3"])]
    
    # 欠損値処理
    df_for_learning = df_for_learning.replace('---', -1)
    df_for_learning = df_for_learning.fillna(-1)

    df_for_learning["odds"] = df_for_learning["odds"].astype(np.float64)
    
    return df_for_learning
    
    