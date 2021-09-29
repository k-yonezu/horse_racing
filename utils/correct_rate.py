import numpy as np

def correct_rate_of_horse_within_3(target_ranks: np.array, predicted_ranks: np.array) -> float:
    """
    3着以内に入った馬の正解率を計算
    
    Parameters
    ----------
    target_ranks : numpy.array
        馬の順位の正解データ
        
    predicted_ranks : numpy.array
        モデルで予測した馬の順位
    
    Returns
    -------
    correct_rate : float
        正解率
    """
    
    index_within_3 = target_ranks <= 3
    corrects = predicted_ranks[index_within_3] <= 3

    correct_rate = corrects.sum() / len(predicted_ranks[index_within_3])
    
    return correct_rate

def correct_rate_of_top_horse(target_ranks: np.array, predicted_ranks: np.array) -> float:
    """
    一着の馬の正解率を計算
    
    Parameters
    ----------
    target_ranks : numpy.array
        馬の順位の正解データ
        
    predicted_ranks : numpy.array
        モデルで予測した馬の順位
    
    Returns
    -------
    correct_rate : float
        正解率
    """
    
    index_of_top_horse = target_ranks == 1
    corrects = predicted_ranks[index_of_top_horse] == 1
    
    correct_rate = corrects.sum() / len(predicted_ranks[index_of_top_horse])
    
    return correct_rate