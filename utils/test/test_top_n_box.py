import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from top_n_box import *
import unittest
    
class Test(unittest.TestCase):
        
    def test_tansyo_ret(self):
        # 予測が当たっている場合
        target_ranks = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
        predicted_ranks = np.array([1, 3, 4, 5, 6, 2, 7, 8, 9, 10, 11, 12, 13, 14, 15])
        tansyo = np.array([300 for _ in range(len(predicted_ranks))])
        is_hit, ret = tansyo_ret(target_ranks, predicted_ranks, tansyo)
        self.assertTrue(is_hit)
        self.assertEqual(ret, 200)
        
        # 予測が当たっていない場合
        target_ranks = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
        predicted_ranks = np.array([2, 3, 4, 5, 6, 1, 7, 8, 9, 10, 11, 12, 13, 14, 15])
        tansyo = np.array([300 for _ in range(len(predicted_ranks))])
        is_hit, ret = tansyo_ret(target_ranks, predicted_ranks, tansyo)
        self.assertFalse(is_hit)
        self.assertEqual(ret, 0)
            
    
    
if __name__ == "__main__":
    unittest.main()