import random
from kuhn3p import betting, deck, Player
import itertools
from player_utilities import UTILITY_DICT

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

Profile = [{
    'k':{ 
        'player': 1,
        'profile': {
            'k': 0.5,
            'b': 0.5
        }
    },
    'kk': { 
        'player': 2,
        'profile': {
            'k': 0.5,
            'b': 0.5
        }
    },
    'kkb': { 
        'player': 0,
        'profile': {
            'f': 0.5,
            'c': 0.5
        }
    },
    'kkbc': { 
        'player': 1,
        'profile': {
            'f': 0.5,
            'c': 0.5
        }
    },
    'kkbf': { 
        'player': 1,
        'profile': {
            'f': 0.5,
            'c': 0.5
        }
    },
    'kb': { 
        'player': 2,
        'profile': {
            'f': 0.5,
            'c': 0.5
        }
    },
    'kbf': { 
        'player': 0,
        'profile': {
            'f': 0.5,
            'c': 0.5
        }
    },
    'kbc': { 
        'player': 0,
        'profile': {
            'f': 0.5,
            'c': 0.5
        }
    },
    'b': { 
        'player': 1,
        'profile': {
            'f': 0.5,
            'c': 0.5
        }
    },
    'bf': { 
        'player': 2,
        'profile': {
            'f': 0.5,
            'c': 0.5
        }
    },
    'bc': { 
        'player': 2,
        'profile': {
            'f': 0.5,
            'c': 0.5
        }
    }
}]

tree = []

for _ in range(24):
    tree.append({
            'k': {
                'strategy': {
                    'k': 0,
                    'b': 0
                },
                'regrets': {
                    'k': 0,
                    'b': 0
                },
            },
            'kk': {
                ''
                'strategy': {
                    'k': 0,
                    'b': 0
                },
                'regrets': {
                    'k': 0,
                    'b': 0
                },
            },
            'kkb': {
                'strategy': {
                    'f': 0,
                    'c': 0
                },
                'regrets': {
                    'f': 0,
                    'c': 0
                },
            },
            'kkbc': {
                'strategy': {
                    'f': 0,
                    'c': 0
                },
                'regrets': {
                    'f': 0,
                    'c': 0
                },
            },
            'kkbf': {
                'strategy': {
                    'f': 0,
                    'c': 0
                },
                'regrets': {
                    'f': 0,
                    'c': 0
                },
            },
            'kb': {
                'strategy': {
                    'f': 0,
                    'c': 0
                },
                'regrets': {
                    'f': 0,
                    'c': 0
                },
            },
            'kbf': {
                'strategy': {
                    'f': 0,
                    'c': 0
                },
                'regrets': {
                    'f': 0,
                    'c': 0
                },
            },
            'kbc': {
                'strategy': {
                    'f': 0,
                    'c': 0
                },
                'regrets': {
                    'f': 0,
                    'c': 0
                },
            },
            'b': {
                'strategy': {
                    'f': 0,
                    'c': 0
                },
                'regrets': {
                    'f': 0,
                    'c': 0
                },
            },
            'bf': {
                'strategy': {
                    'f': 0,
                    'c': 0
                },
                'regrets': {
                    'f': 0,
                    'c': 0
                },
            },
            'bc': {
                'strategy': {
                    'f': 0,
                    'c': 0
                },
                'regrets': {
                    'f': 0,
                    'c': 0
                },
            }
        })


class SmartAgent(Player):
    def __init__(self):
        self.player = -1
        self.card = -1
        self.tree = tree
        self.tree_index = -1

    def start_hand(self, position, card):
        self.player = position
        self.card = card
        iterations = 10
        i = 0
        for t in range(iterations):
            while i < 3:
                self.cfr('', i, t, 1, 1)
                i += 1
        # print len(Profile), Profile[8] 

    def act(self, state, card):
        betting.BET

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
            a = random.choice(['k', 'b'])
            self.tree_index = random.randint(0, 23)
            number = self.cfr(h + a, i, t, pi, pni)
            return number
        elif h not in Actions:
            hand = [deck.JACK, deck.KING, deck.ACE]
            utility = self.utility(h, i, hand)
            return utility
        
        vsigma = 0

        Vsigma = {
            'c': 0,
            'k': 0,
            'f': 0,
            'b': 0
        }

        for a in Actions[h]:
            Vsigma[a] = self.cfr(h + a, i, t, self.get_action_profile(t, h, a) * pi,  pni)
            vsigma += self.get_action_profile(t, h, a) * Vsigma[a]

        if Profile[t][h]['player'] == i:
            for a in Actions[h]:
                self.tree[self.tree_index][h]['regrets'][a] += pni * \
                    (Vsigma[a] - vsigma)
                self.tree[self.tree_index][h]['strategy'][a] += pi * \
                    self.get_action_profile(t, h, a)

            profile = Profile[t]

            for a in Actions[h]:
                actionregret = self.tree[self.tree_index][h]['regrets'][a]
                regretsum = sum(self.tree[self.tree_index][h]['regrets'].values())
                print regretsum, actionregret, self.tree[self.tree_index][h]['regrets'].values()
                profile[h][a] = max([0, actionregret]) / \
                    regretsum if regretsum > 0 else 0.5

            Profile.append(profile)
        return vsigma

    def get_action_profile(self, t, h, a):
        # print t, h, a
        profile = Profile[t][h]['profile'][a]
        return profile

    def utility(self, h, i, hand):
        utility = UTILITY_DICT.get(h)(i, hand)
        return utility

    def __str__(self):
        return 'SmartAgeet'
