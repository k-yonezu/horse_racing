import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
from utils.purchasing_strategy import PurchasingStrategy

class TopNBox(PurchasingStrategy):
    def __init__(self, predicted_ranks, n):
        super().__init__(predicted_ranks)
        self.n = n

    def tansyo(self):
        tickets = []
        for i in range(1, self.n+1):
            ticket = np.where(self.predicted_ranks == i)
            # ticket = (array([something...]), ) 
            # ticket[0] => array[something...]
            tickets.append(ticket[0])
        return tickets

    def hukusyo(self):
        tickets = self.tansyo()
        return tickets

if __name__ == "__main__":
    predicted_ranks = np.array([1, 3, 4, 2, 5, 6])
    top_n_box = TopNBox(predicted_ranks, 2)
    print(top_n_box.tansyo())
    print(top_n_box.hukusyo())