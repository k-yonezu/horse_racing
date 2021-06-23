import pandas as pd
import numpy as np
import utils.preprocessing as pp
import utils.sampling_new_columns as sc

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
                 "prize-1", "prize-2", "prize-3"]

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
        学習用データフレーム
    """
    df_for_learning = process_features(raw_df)
    # ラベル作成
    df_for_learning.loc[: ,"label"] = pp.make_label(df_for_learning.loc[: ,"rank"].values, df_for_learning.loc[: ,"total_horse_number_x"].values)
    df_for_learning.loc[: ,"rank-1"] = pp.make_label(df_for_learning.loc[: ,"rank-1"].values, df_for_learning.loc[: ,"total_horse_number_x-1"].values)
    df_for_learning.loc[: ,"rank-2"] = pp.make_label(df_for_learning.loc[: ,"rank-2"].values, df_for_learning.loc[: ,"total_horse_number_x-2"].values)
    df_for_learning.loc[: ,"rank-3"] = pp.make_label(df_for_learning.loc[: ,"rank-3"].values, df_for_learning.loc[: ,"total_horse_number_x-3"].values)
    # one-hotベクトル化
    df_for_learning = pp.one_hot_encoding(df_for_learning[columns_after_processing+["label"]])

    return df_for_learning
    
def prepare_data_for_prediction(df_for_prediction: pd.DataFrame, past_data_df: pd.DataFrame) -> pd.DataFrame:
    """
    データを予測に使えるように加工
    
    Parameters
    ----------
    df_for_prediction : pandas.DataFrame
        予測に使うデータ
        
    past_data_df : pandas.DataFrame
        学習に使った過去データ、予測用データには一部のカテゴリデータしかないので、
        one-hotベクトル化後、学習済みモデルの入力次元数と次元数が合わない。
        そこで、過去データを参照して追加する。
    
    Retures
    -------
    df_after_processing : pandas.DataFrame
        加工済み予測用データ
    """
    df_after_processing = process_features(df_for_prediction)
    df_after_processing.loc[: ,"rank-1"] = pp.make_label(df_after_processing.loc[: ,"rank-1"].values, df_after_processing.loc[: ,"total_horse_number_x-1"].values)
    df_after_processing.loc[: ,"rank-2"] = pp.make_label(df_after_processing.loc[: ,"rank-2"].values, df_after_processing.loc[: ,"total_horse_number_x-2"].values)
    df_after_processing.loc[: ,"rank-3"] = pp.make_label(df_after_processing.loc[: ,"rank-3"].values, df_after_processing.loc[: ,"total_horse_number_x-3"].values)
    df_after_processing = pp.one_hot_encoding(df_after_processing[columns_after_processing])
    past_data_df = process_features(past_data_df)
    past_data_df.loc[: ,"rank-1"] = pp.make_label(past_data_df.loc[: ,"rank-1"].values, past_data_df.loc[: ,"total_horse_number_x-1"].values)
    past_data_df.loc[: ,"rank-2"] = pp.make_label(past_data_df.loc[: ,"rank-2"].values, past_data_df.loc[: ,"total_horse_number_x-2"].values)
    past_data_df.loc[: ,"rank-3"] = pp.make_label(past_data_df.loc[: ,"rank-3"].values, past_data_df.loc[: ,"total_horse_number_x-3"].values)
    past_data_df = pp.one_hot_encoding(past_data_df[columns_after_processing])
    
    pp.fill_missing_columns(df_after_processing, past_data_df)
    
    return df_after_processing
    
def process_features(df_before_processing: pd.DataFrame) -> pd.DataFrame:
    """
    特徴量を加工
        Parameters
    ----------
    df_before_processing : pandas.DataFrame
        特徴量加工前のデータフレーム
    
    Returns
    -------
    df_after_processing : pandas.DataFrame
        特徴量加工後のデータフレーム
    """
    df_after_processing = df_before_processing[columns_before_processing]
    df_after_processing.loc[:, "where_racecourse"] = df_after_processing.loc[: ,"where_racecourse"].map(sc.extract_place)

    df_after_processing.loc[: ,"sex"] = df_after_processing.loc[: ,"sex_and_age"].map(lambda sex_and_age: sex_and_age[0])
    df_after_processing.loc[: ,"age"] = df_after_processing.loc[: ,"sex_and_age"].map(lambda sex_and_age: sex_and_age[1:]).astype(int)
    
    df_after_processing.loc[: ,"goal_time-1"] = df_after_processing.loc[: ,"goal_time-1"].map(sc.to_seconds)
    df_after_processing.loc[: ,"goal_time-2"] = df_after_processing.loc[: ,"goal_time-2"].map(sc.to_seconds)
    df_after_processing.loc[: ,"goal_time-3"] = df_after_processing.loc[: ,"goal_time-3"].map(sc.to_seconds)
    
    df_after_processing.loc[: ,"horse_weight"] = df_after_processing.loc[: ,"horse_weight"].map(pp.extract_weight).astype(np.int64)
    
    df_after_processing.loc[: ,"prize-1"] = df_after_processing.loc[: ,"prize-1"].map(
        lambda prize: prize.replace(",", "") if type(prize) == str else prize).astype(np.float32)
    df_after_processing.loc[: ,"prize-2"] = df_after_processing.loc[: ,"prize-2"].map(
        lambda prize: prize.replace(",", "") if type(prize) == str else prize).astype(np.float32)
    df_after_processing.loc[: ,"prize-3"] = df_after_processing.loc[: ,"prize-3"].map(
        lambda prize: prize.replace(",", "") if type(prize) == str else prize).astype(np.float32)
    
    df_after_processing.loc[: ,"kyakusitu-1"] = [sc.kyakusitu_code_c(n, r) 
        for n, r in zip(df_after_processing.loc[: ,"total_horse_number_x-1"].values, df_after_processing.loc[: ,"half_way_rank-1"])]
    df_after_processing.loc[: ,"kyakusitu-2"] = [sc.kyakusitu_code_c(n, r) 
        for n, r in zip(df_after_processing.loc[: ,"total_horse_number_x-2"].values, df_after_processing.loc[: ,"half_way_rank-2"])]
    df_after_processing.loc[: ,"kyakusitu-3"] = [sc.kyakusitu_code_c(n, r) 
        for n, r in zip(df_after_processing.loc[: ,"total_horse_number_x-3"].values, df_after_processing.loc[: ,"half_way_rank-3"])]
    
    # 欠損値処理
    df_after_processing = df_after_processing.replace('---', -1)
    df_after_processing = df_after_processing.fillna(-1)

    df_after_processing.loc[: ,"odds"] = df_after_processing.loc[: ,"odds"].astype(np.float32)
    
    return df_after_processing
