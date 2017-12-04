import random
from kuhn3p import betting, deck
import itertools
from Player_Utilities import *

hand = [deck.JACK, deck.QUEEN, deck.KING, deck.ACE]
handperm = itertools.permutations(hand, 3)

Actions = {
    'k': ('k', 'b'),
    'kk': ('k', 'b'),
    # 'kkk': (),
    'kkb': ('c', 'f'),
    'kkbc': ('c', 'f'),
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
			}	'f': 0,
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
			}	'f': 0,
	}, 'profile': [{
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
				}	'f': 0.5,
			}],
		'strategy': 		})


class Player(object):
    def __init__(self):
        self.player = -1
        self.card = -1
		self.tree = tree
		self.tree_index = -1

    def start_hand(self, position, card):
        self.player = position
        self.card = card
		iterations = 50
		for t in range(iterations):
			for i in range(2):
				self.cfr('', i, t, 1, 1)

    def act(self, state, card):
        raise NotImplementedError

    def end_hand(self, position, card, state, shown_cards):
        pass

    def cfr(self, h, i, t, pi, pni):
    """
		@Description: counter factual regret recursive function
		@Params:
			h: action history
			i: player i
			t: iteration
			pi: probability profile for player i
			pni: probability profile without player i
	"""
        if not h:
            a = random.choice(['c', 'b'])
			self.tree_index = random.randint(0, 24)
            return self.cfr(h + a, i, t, pi, pni)
        elif h not in Actions:
			return utility(h, i, handperm[self.tree_index])

        vsigma = 0

		Vsigma = {
			'k': 0,
			'kk': 0,
			'kkb': 0,
			'kkbc': 0,
			'kb': 0,
			'kbf': 0,
			'kbc': 0,
			'b': 0,
			'bf': 0,
			'bc': 0
		}

        for a in Actions[h]:
			if self.player == i:
            	Vsigma[a] = self.cfr(ha, i, t, self.get_action_profile(t, h, a) * pi, pni)
			else:
            	Vsigma[a] = self.cfr(ha, i, t, pi, self.get_action_profile(t, h, a) *  pni)				
            vsigma += self.get_action_profile(t, h, a) * Vsigma[a]

        if self.player == i:
            for a in Actions[h]:
                self.tree[self.tree_index]['regrets'][h][a] += pni * (Vsigma[a] - vsigma)
                self.tree['strategy'][h][a] += pi * self.get_action_profile(t, h, a)

            for a in Actions[h]:
                actionregret = self.tree['regrets'][h][a]
                nextprofile[h][a] = actionregret / \
                    sum(self.tree['regrets'][h]) if actionregret > 0 else 0.5

        self.tree[self.tree_index]['profile'].append(nextprofile)

    def get_action_profile(self, t, h, a):
        return self.tree['profile'][t][h][a]

	def utility(self, h, i, hand):
        return UTILITY_DICT.get(h)(i, hand)
