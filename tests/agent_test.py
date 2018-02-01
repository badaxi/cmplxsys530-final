""" Test functionality of base agent """
from agent.base_agent import Base_Agent

def testWinLoss():
    """ Test calculation of win/loss ratio"""
    ba1 = Base_Agent()
    ba1.num_wins = 50
    assert(ba1.win_loss_ratio() == None) 
    ba1.num_losses = 10
    assert(ba1.win_loss_ratio() == 5) 

testWinLoss()