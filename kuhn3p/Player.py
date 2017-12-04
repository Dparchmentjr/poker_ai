from Player_Utilities import *

class Player:
    def __init__(self):
        pass

    def start_hand(self, position, card):
        pass

    def act(self, state, card):
        raise NotImplementedError

    def end_hand(self, position, card, state, shown_cards):
        pass
    
    def expected_utility(self, h, i, hand):
        return UTILITY_DICT.get(h)(i, hand)