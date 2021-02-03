import numpy as np
import pandas as pd

def kyakusitu_code_c(horse_number,half_way_rank):
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