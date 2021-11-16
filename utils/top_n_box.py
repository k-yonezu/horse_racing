import pandas as pd
import numpy as np
from typing import Tuple

PRICE_OF_BETTING_TICKET = 100

def extract_race(horse_race_df, race_id):
    return horse_race_df[horse_race_df["race_id"] == race_id]

def tansyo_ret(target_ranks: np.array, predicted_ranks: np.array, tansyo: np.array) -> Tuple[float, float]:
    if target_ranks.dtype != np.int32:
        raise "target_ranks.dtype must be np.int32"
    
    index_of_top_horse = target_ranks == 1
    is_hit = predicted_ranks[index_of_top_horse] == 1
    
    if is_hit:
        ret = int(tansyo[index_of_top_horse]) - PRICE_OF_BETTING_TICKET
    else:
        ret = 0
    
    return is_hit, ret

def hukusyo_ret():
    return 0

def top_1_box(race_horse_df: pd.DataFrame, predicted_ranks_df: pd.DataFrame):
    stats = {"tansyo": {"correct_rate": 0, "ret_rate": 0, "ret_std": 0, "hit_list": [], "ret_list": [], "total_hit": 0, "total_ret": 0}}

    race_ids = list(set(race_horse_df["race_id"].values))
    for race_id in race_ids:
        predicted_ranks = extract_race(predicted_ranks_df, race_id)["rank"].values
        target_race_df = extract_race(race_horse_df, race_id)
        is_hit, ret = tansyo_ret(target_race_df["rank"].values, predicted_ranks, target_race_df["tansyo"].values)
        stats["tansyo"]["hit_list"].append(int(is_hit))
        stats["tansyo"]["ret_list"].append(ret)
    
    return stats
