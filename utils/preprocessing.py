import re
import datetime
import pandas as pd
import tensorflow as tf
import numpy as np
#from tqdm import tqdm


def kyakusitu_code_c(horse_number,half_way_rank):
    # 欠損値の場合
    if type(half_way_rank) != str:
        return half_way_rank
     
    tuuka= [int(s) for s in half_way_rank.split('-')]
    if len(tuuka)==1:
        if tuuka[0]==1:
            kyakusitu_code=0
        elif tuuka[0]>=2 and tuuka[0]<=4:
            kyakusitu_code=1
        elif tuuka[0]<=(horse_number/3*2) and horse_number>=8:
            kyakusitu_code=2
        else:
            kyakusitu_code=3
    if len(tuuka)>=2:
        last_couner=tuuka.pop()
        if 1 in tuuka:
            kyakusitu_code=0
        elif last_couner>=2 and last_couner<=4:
            kyakusitu_code=1
        elif last_couner<=(horse_number/3*2) and horse_number>=8:
            kyakusitu_code=2
        else:
            kyakusitu_code=3
    return kyakusitu_code

def extract_place(where_racecourse):
    place = re.match(r"\d+回(\D+)\d+日目", where_racecourse).groups()[0]
    return place

def to_seconds(time):
    if type(time) != str:
        return time
    minutes, second_milliseconds = time.split(":")
    seconds, milliseconds = second_milliseconds.split(".")
    td = datetime.timedelta(minutes=int(minutes), seconds=int(seconds), milliseconds=int(milliseconds))
    return td.total_seconds()

def extract_weight(horse_weight):
    if horse_weight == "計不" or type(horse_weight) != str:
        return -1
    weight = re.match(r"(\d+)\([+-]?\d+\)", horse_weight).groups()[0]
    return weight 

def one_hot_encoding(df):
    return pd.get_dummies(df)

def make_label(rank_values, horse_number_values):
    labels = []
    high = 1 / 3
    mid = 2 / 3
    for rank, horse_number in zip(rank_values, horse_number_values):
        # 欠損値の場合
        if rank == -1:
            labels.append(rank)
            continue
        # 順位が付かないデータに関しては最低レベルのラベルを付与
        not_rank = False
        # "(" => ...(再)　or ...(降)
        for c in ["中", "取", "除", "(", "失"]:
            if c in str(rank):
                labels.append("low")
                not_rank = True
                break
        if not_rank:
            continue
            
        relative_rank = int(rank) / horse_number
    
        if relative_rank < high:
            labels.append("high")
        elif relative_rank < mid:
            labels.append("middle")
        else:
            labels.append("low")
            
    return labels
