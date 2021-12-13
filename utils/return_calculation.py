import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import numpy as np

PRICE_OF_BETTING_TICKET = 100

def tansho(tickets, target_ranks, prizes):
    num_hit = 0
    ret = 0
    for ticket in tickets:
        rank = target_ranks[ticket][0]
        if rank == 1:
            num_hit += 1
            ret += prizes[ticket][0] - PRICE_OF_BETTING_TICKET
        else:
            ret -= PRICE_OF_BETTING_TICKET
    return num_hit, ret

def fukusho(tickets, target_ranks, prizes):
    num_hit = 0
    ret = 0
    for ticket in tickets:
        rank = target_ranks[ticket][0]
        if rank == 1 or rank == 2:
            num_hit += 1
            ret += prizes[ticket][0] - PRICE_OF_BETTING_TICKET
        else:
            ret -= PRICE_OF_BETTING_TICKET
    return num_hit, ret

def wakuren(tickets, target_ranks, prizes):
    raise NotImplementedError()

def umaren(tickets, target_ranks, prizes):
    num_hit = 0
    ret = 0
    for ticket in tickets:
        rank = target_ranks[ticket]
        if rank[0] in [1, 2] and rank[1] in [1, 2]:
            num_hit += 1
            ret += prizes[ticket][0] - PRICE_OF_BETTING_TICKET
        else:
            ret -= PRICE_OF_BETTING_TICKET
    return num_hit, ret

def umatan(tickets, target_ranks, prizes):
    num_hit = 0
    ret = 0
    for ticket in tickets:
        rank = target_ranks[ticket]
        if rank[0] == 1 and rank[1] == 2:
            num_hit += 1
            ret += prizes[ticket][0] - PRICE_OF_BETTING_TICKET
        else:
            ret -= PRICE_OF_BETTING_TICKET
    return num_hit, ret

def wide(tickets, target_ranks, prizes):
    num_hit = 0
    ret = 0
    for ticket in tickets:
        rank = target_ranks[ticket][0]
        print(rank)
        if rank == 1 or rank == 2:
            num_hit += 1
            ret += prizes[ticket][0] - PRICE_OF_BETTING_TICKET
        else:
            ret -= PRICE_OF_BETTING_TICKET
    return num_hit, ret

def sanrempuku(tickets, target_ranks, prizes):
    num_hit = 0
    ret = 0
    for ticket in tickets:
        rank = target_ranks[ticket][0]
        print(rank)
        if rank == 1 or rank == 2:
            num_hit += 1
            ret += prizes[ticket][0] - PRICE_OF_BETTING_TICKET
        else:
            ret -= PRICE_OF_BETTING_TICKET
    return num_hit, ret

def sanrentan(tickets, target_ranks, prizes):
    num_hit = 0
    ret = 0
    for ticket in tickets:
        rank = target_ranks[ticket][0]
        print(rank)
        if rank == 1 or rank == 2:
            num_hit += 1
            ret += prizes[ticket][0] - PRICE_OF_BETTING_TICKET
        else:
            ret -= PRICE_OF_BETTING_TICKET
    return num_hit, ret

if __name__ == "__main__":
    from utils.top_n_box import TopNBox
    predicted_ranks = np.array([1, 3, 4, 2, 5, 6])
    target_ranks = np.array([1, 2, 3, 4, 5, 6])
    prizes = np.array([500, 500, 500, 500, 500])
    top_n_box = TopNBox(predicted_ranks, 4)
    for t in ["umatan"]:#TopNBox.ticket_types:
        tickets = top_n_box.output_tickets(t)
        num_hit, ret = umatan(tickets, target_ranks, prizes)
        print(f"-----ticket type: {t}------")
        print("predicted ranks:", predicted_ranks)
        print("prizes:", prizes)
        print("tickets: ", tickets)
        print("num hit:", num_hit)
        print("return:", ret)
