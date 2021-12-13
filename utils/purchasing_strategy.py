from abc import *

class PurchasingStrategy:
    def __init__(self, predicted_ranks):
        self.predicted_ranks = predicted_ranks
        pass

    def output_tickets(self, ticket_type):
        tickets = []
        if ticket_type == "tansyo":
            tickets = self.tansyo()
        elif ticket_type == "hukusyo":
            tickets = self.hukusyo()
        
        return tickets
    
    @abstractmethod
    def tansyo(self):
        raise NotImplementedError()

    @abstractmethod
    def hukusyo(self):
        raise NotImplementedError()
