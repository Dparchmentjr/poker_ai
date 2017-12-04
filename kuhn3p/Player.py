import random
from kuhn3p import betting, deck
import itertools
from Player_Utilities import UTILITY_DICT

hand = [deck.JACK, deck.QUEEN, deck.KING, deck.ACE]
handperm = list(itertools.permutations(hand, 3))

Actions = {
    'k': ('k', 'b'),
    'kk': ('k', 'b'),
    # 'kkk': (),
    'kkb': ('c', 'f'),
    'kkbc': ('c', 'f'),
    'kkbf': ('c', 'f'),	
    # 'kkbcc': (),
    # 'kkbcf': (),
    # 'kkbfc': (),
    # 'kkbff': (),
    'kb': ('f', 'c'),
    'kbf': ('f', 'c'),
    # 'kbff': (),
    # 'kbfc': (),
    'kbc': ('f', 'c'),
    # 'kbcf': (),
    # 'kbcc': (),
    'b': ('f', 'c'),
    'bf': ('f', 'c'),
    # 'bfc': (),
    # 'bff': (),
    'bc': ('f', 'c'),
    # 'bcc': (),
    # 'bcf': ()
}

profile = {
		'k': {
			'k': 0.5,
			'b': 0.5
		},
		'kk': {
			'k': 0.5,
			'b': 0.5
		},
		'kkb': {
			'c': 0.5,
			'f': 0.5
		},
		'kkbc': {
			'c': 0.5,
			'f': 0.5
		},
		'kkbf': {
	        'c': 0.5,
			'f': 0.5
		},
		'kb': {
			'f': 0.5,
			'c': 0.5
		},
		'kbf': {
			'f': 0.5,
			'c': 0.5
		},
		'kbc': {
			'f': 0.5,
			'c': 0.5
		},
		'b': {
			'c': 0.5,
			'f': 0.5
		},
		'bf': {
			'c': 0.5,
			'f': 0.5
		},
		'bc': {
			'c': 0.5,
			'f': 0.5
		}	
	}

tree = []

for _ in range(24):
	tree.append({
		'strategy': {
			'k': {
				'k': 0,
				'b': 0
			},
			'kk': {
				'k': 0,
				'b': 0
			},
			'kkb': {
				'c': 0,
				'f': 0
			},
			'kkbc': {
				'c': 0,
				'f': 0
			},
			'kkbf': {
	        	'c': 0,
				'f': 0
			},
			'kb': {
				'f': 0,
				'c': 0
			},
			'kbf': {
				'f': 0,
				'c': 0
			},
			'kbc': {
				'f': 0,
				'c': 0
			},
			'b': {
				'c': 0,
				'f': 0
			},
			'bf': {
				'c': 0,
				'f': 0
			},
			'bc': {
				'c': 0,
				'f': 0
			}	
	}, 'regrets': {
			'k': {
				'k': 0,
				'b': 0
			},
			'kk': {
				'k': 0,
				'b': 0
			},
			'kkb': {
				'c': 0,
				'f': 0
			},
			'kkbc': {
				'c': 0,
				'f': 0
			},
			'kkbf': {
	        	'c': 0,
				'f': 0
			},
			'kb': {
				'f': 0,
				'c': 0
			},
			'kbf': {
				'f': 0,
				'c': 0
			},
			'kbc': {
				'f': 0,
				'c': 0
			},
			'b': {
				'c': 0,
				'f': 0
			},
			'bf': {
				'c': 0,
				'f': 0
			},
			'bc': {
				'c': 0,
				'f': 0
			}	
	}, 'profile': [profile]	
		})


class Player(object):
    def __init__(self):
        pass

    def start_hand(self, position, card):
        pass

    def act(self, state, card):
        raise NotImplementedError

    def end_hand(self, position, card, state, shown_cards):
        pass

  