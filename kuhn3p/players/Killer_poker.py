import random, matplotlib.pyplot as plt 
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
    'k': {
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

tree = {
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
        }
    }
}

Strategy = dict()

for a in Actions:
    Strategy[a] = dict([[k, 0] for k in Actions[a]])

class SmartAgent(Player):
    def __init__(self):
        self.perfomance = []
        self.player = -1
        self.card = -1
        self.tables = tree
        self.strategy = Strategy
        
        iterations = 200

        for t in range(iterations):
            i = 0        
            while i < 3:
                self.cfr('', i, t, 1, 1)
                i += 1
            
            self.perfomance.append(sum([sum(self.tables[k]['regrets'].values()) for k in self.tables]))
            

        # self.get_average_strategy()
        

        plt.plot(self.perfomance)
        plt.show()

        # for node in self.strategy:
        #     print(node, self.strategy[node])

    def start_hand(self, position, card):
        self.player = position
        self.card = card

    def act(self, state, card):
        print('state:', state, card, self.player)
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
        if h not in Actions:
            # hand_options = filter(
            #     lambda x: x[self.player] == self.card, handperm)
            hand = random.choice(handperm)
            utility = self.utility(h, i, hand)
            return utility

        vsigma = 0
        Vsigma = {}
        for a in Actions:
            Vsigma[a] = dict([[k, 0] for k in Actions[a]])

            
        for a in Actions[h]:
            if Profile[t][h]['player'] == i:
                Vsigma[h][a] = self.cfr(
                    h + a, i, t, self.get_action_profile(t, h, a) * pi,  pni)
            else:
                Vsigma[h][a] = self.cfr(
                    h + a, i, t, pi,  pni * self.get_action_profile(t, h, a))

            vsigma += self.get_action_profile(t, h, a) * Vsigma[h][a]

        if Profile[t][h]['player'] == i:
            for a in Actions[h]:
                regret = pni * (Vsigma[h][a] - vsigma)
                self.tables[h]['regrets'][a] += regret
                self.tables[h]['strategy'][a] += pi * \
                    self.get_action_profile(t, h, a)


            profile = Profile[t]
            normalization = 0
            for a in Actions[h]:
                actionregret = max([self.tables[h]['regrets'][a], 0])
                normalization += actionregret

            for a in Actions[h]:
                profile[h]['profile'][a] /= normalization if normalization > 0 else 0.5
                # self.tables[h]['strategy'][a] += pi * profile[h]['profile'][a]

            Profile.append(profile)
        return vsigma

    def get_average_strategy(self):        
        for h in Actions:  
            normalization = 0 
            for a in Actions[h]:
                normalization += self.tables[h]['strategy'][a]

            for a in Actions[h]:
                self.strategy[h][a] = self.tables[h]['strategy'][a] / normalization if normalization > 0 else 0.5

    def get_action_profile(self, t, h, a):
        profile = Profile[t][h]['profile'][a]
        return profile

    def utility(self, h, i, hand):
        utility = UTILITY_DICT.get(h)(i, hand)
        return utility

    def __str__(self):
        return 'SmartAgeet'
