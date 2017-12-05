import random, matplotlib.pyplot as plt, math
from kuhn3p import betting, deck, Player
import itertools
from .player_utilities import UTILITY_DICT

hand = [deck.JACK, deck.QUEEN, deck.KING, deck.ACE]
handperm = list(itertools.permutations(hand, 3))

Actions = {
    'i': ('k', 'b'),
    'ik': ('k', 'b'),
    'ikk': ('k', 'b'),
    'ikkb': ('c', 'f'),
    'ikkbc': ('c', 'f'),
    'ikkbf': ('c', 'f'),
    'ikb': ('f', 'c'),
    'ikbf': ('f', 'c'),
    'ikbc': ('f', 'c'),
    'ib': ('f', 'c'),
    'ibf': ('f', 'c'),
    'ibc': ('f', 'c'),
}


tree = {
    'i': {
        'player': 0,        
        'strategySum': {
            'k': 0,
            'b': 0
        },
        'regretSum': {
            'k': 0,
            'b': 0
        },
        'strategy': {
            'k': 0.5,
            'b': 0.5
        }
    },
    'ik': {
        'player': 1,        
        'strategySum': {
            'k': 0,
            'b': 0
        },
        'regretSum': {
            'k': 0,
            'b': 0
        },
        'strategy': {
            'k':0.5,
            'b': 0.5
        }
    },
    'ikk': {
        'player': 2,        
        'strategySum': {
            'k': 0,
            'b': 0
        },
        'regretSum': {
            'k': 0,
            'b': 0
        },
        'strategy': {
            'k': 0.5,
            'b': 0.5
        },
    },
    'ikkb': {
        'player': 0,        
        'strategySum': {
            'f': 0,
            'c': 0
        },
        'regretSum': {
            'f': 0,
            'c': 0
        },
        'strategy': {
            'f': 0.5,
            'c': 0.5
        }
    },
    'ikkbc': {
        'player': 1,        
        'strategySum': {
            'f': 0,
            'c': 0
        },
        'regretSum': {
            'f': 0,
            'c': 0
        },
        'strategy': {
            'f': 0.5,
            'c': 0.5
        }
    },
    'ikkbf': {
        'player': 1,        
        'strategySum': {
            'f': 0,
            'c': 0
        },
        'regretSum': {
            'f': 0,
            'c': 0
        },
        'strategy': {
            'f': 0.5,
            'c': 0.5
        }
    },
    'ikb': {
        'player': 2,        
        'strategySum': {
            'f': 0,
            'c': 0
        },
        'regretSum': {
            'f': 0,
            'c': 0
        },
        'strategy': {
            'f': 0.5,
            'c': 0.5
        }
    },
    'ikbf': {
        'player': 0,        
        'strategySum': {
            'f': 0,
            'c': 0
        },
        'regretSum': {
            'f': 0,
            'c': 0
        },
        'strategy': {
            'f': 0.5,
            'c': 0.5
        }
    },
    'ikbc': {
        'player': 0,        
        'strategySum': {
            'f': 0,
            'c': 0
        },
        'regretSum': {
            'f': 0,
            'c': 0
        },
        'strategy': {
            'f': 0.5,
            'c': 0.5
        }
    },
    'ib': {
        'player': 1,        
        'strategySum': {
            'f': 0,
            'c': 0
        },
        'regretSum': {
            'f': 0,
            'c': 0
        },
        'strategy': {
            'f': 0.5,
            'c': 0.5
        }
    },
    'ibf': {
        'player': 2,        
        'strategySum': {
            'f': 0,
            'c': 0
        },
        'regretSum': {
            'f': 0,
            'c': 0
        },
        'strategy': {
            'f': 0.5,
            'c': 0.5
        }
    },
    'ibc': {
        'player': 2,        
        'strategySum': {
            'f': 0,
            'c': 0
        },
        'regretSum': {
            'f': 0,
            'c': 0
        },
        'strategy': {
            'f': 0.5,
            'c': 0.5
        }
    }
}

Strategy = dict()

for a in Actions:
    Strategy[a] = dict([[k, 0] for k in Actions[a]])

class SmartAgent(Player):
    def __init__(self):
        super().__init__()
        self.player = -1
        self.card = -1
        self.tables = tree
        self.avg_strategy = Strategy
        self.score_perf = []

        iterations = 50
        self.performance = [0 for _ in range(iterations)]
        for t in range(iterations):
            i = 0
            score = 0      
            while i < 3:
                self.training_hand = random.choice(handperm)                
                score = self.cfr('i', i, t, .5, 1)
                i += 1
            self.score_perf.append(score)

        for i in self.tables:
            print(i, self.tables[i])
            
        self.get_average_strategy()

        for node in self.avg_strategy:
            print(node, self.avg_strategy[node])

        # plt.plot(self.score_perf)
        plt.plot(self.performance)
        plt.show()

      

    def start_hand(self, position, card):
        self.player = position
        self.card = card

    def act(self, state, card):
        print(('state:', state, card, self.player))
        return betting.BET

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
            return self.utility(h, i, self.training_hand)

        vsigma = 0
        Vsigma = {
            'c': 0,
            'b': 0,
            'k': 0,
            'f': 0
        }

        if self.tables[h]['player'] == i:
            self.update_table(pi)
        else:
            self.update_table(pni)
        
        for a in Actions[h]:
            if self.tables[h]['player'] == i:
                Vsigma[a] = self.cfr(
                    h + a, i, t, self.tables[h]['strategy'][a] * pi, pni)
            else:
                Vsigma[a] = self.cfr(
                    h + a, i, t, pi, pni * self.tables[h]['strategy'][a])

            vsigma += self.tables[h]['strategy'][a] * Vsigma[a]

        for a in Actions[h]:   
            if self.tables[h]['player'] == i:        
                regret = pni * (Vsigma[a] - vsigma)
            else:
                regret = pi * (Vsigma[a] - vsigma)
                
            assert not math.isnan(regret)
            self.tables[h]['regretSum'][a] += regret
            if t < 5:
                print('iteration %s for node %s' % (t, h), self.tables[h]['strategySum'])
            

        self.performance[t] = vsigma
        return vsigma

    def update_table(self, pi):
        for h in Actions:
            normalization = 0
            actionregret = {
                    'c': 0,
                    'b': 0,
                    'k': 0,
                    'f': 0
            }                     
            for a in Actions[h]:
                actionregret[a] = max([self.tables[h]['regretSum'][a], 0])
                normalization += actionregret[a]

            for a in Actions[h]:
                self.tables[h]['strategy'][a] = actionregret[a] / normalization if normalization > 0 else 0.5
                self.tables[h]['strategySum'][a] += pi * self.tables[h]['strategy'][a]
                
                    

    def get_average_strategy(self):
        for h in Actions:
            normalization = 0
            for a in Actions[h]:
                normalization += self.tables[h]['strategySum'][a]

            for a in Actions[h]:
                self.avg_strategy[h][a] = self.tables[h]['strategySum'][a] / normalization if normalization > 0 else 0.5


    def utility(self, h, i, hand):
        return UTILITY_DICT.get(h[1:])(i, hand)

    def __str__(self):
        return 'SmartAgeet'
