import datetime
import re
import numpy as np

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
    if horse_weight == "計不":
        return -1
    weight = re.match(r"(\d+)\([+-]?\d+\)", horse_weight).groups()[0]
    return weight 
