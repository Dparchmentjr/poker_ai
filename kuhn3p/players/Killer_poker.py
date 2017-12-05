import random, matplotlib.pyplot as plt, math, sys
from kuhn3p import betting, deck, Player
import itertools
from .player_utilities import UTILITY_DICT
import pandas as pd

hand = [deck.JACK, deck.QUEEN, deck.KING, deck.ACE]
handperm = list(itertools.permutations(hand, 3))

Actions = {
    'i': ('k', 'b'),
    'ik': ('k', 'b'),
    'ikk': ('k', 'b'),
    'ikkb': ('c', 'f'),
    'ikkbc': ('c', 'f'),
    'ikkbf': ('c', 'f'),
    'ikb': ('c', 'f'),
    'ikbf': ('c', 'f'),
    'ikbc': ('c', 'f'),
    'ib': ('c', 'f'),
    'ibf': ('c', 'f'),
    'ibc': ('c', 'f'),
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
            'c': 0.5,
            'f': 0.5            
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
            'c': 0.5,
            'f': 0.5
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
            'c': 0.5,
            'f': 0.5            
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
            'c': 0.5,
            'f': 0.5            
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
            'c': 0.5,
            'f': 0.5            
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
            'c': 0.5,
            'f': 0.5            
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
            'c': 0.5,            
            'f': 0.5
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
            'c': 0.5,
            'f': 0.5            
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
            'c': 0.5,
            'f': 0.5            
        }
    }
}

Strategy = dict()

state_map = {
    'i':     'i',
    'c':     'ik',
    'cc':    'ikk',
    'ccr':   'ikkb',
    'ccrf':  'ikkbf',    
    'ccrc':  'ikkbc',
    'cr':    'ikb',
    'crf':   'ikbf',
    'crc':   'ikbc',
    'r':      'ib',
    'rf':    'ibf',
    'rc':    'ibc'
}

for a in Actions:
    Strategy[a] = dict([[k, 0] for k in Actions[a]])

class SmartAgent(Player):
    def __init__(self):
        self.player = -1
        self.card = -1
        self.tables = tree
        self.avg_strategy = Strategy
        self.score_perf = []

        if len(sys.argv) > 1:
            self.train_cfr()

    def train_cfr(self):
        iterations = 10000
        t = 0
        self.performance = [0 for _ in range(iterations)]
        while t < iterations:
            i = 0
            score = 0    
            self.training_hand = random.choice(handperm)                           
            while i < 3:
                score = self.cfr('i', i, t, .5, 1)
                i += 1
            self.score_perf.append(score)

            if t == iterations:

                self.get_average_strategy()

                data = pd.Series([self.avg_strategy[n] for n in self.avg_strategy], index=[n for n in self.avg_strategy])
                self.performance = [0 for _ in range(iterations)]
                      
                        
                plt.plot(self.performance)
                plt.show()

            t = (t + 1) % iterations    
            
      

    def start_hand(self, position, card):
        self.player = position
        self.card = card

    def act(self, state, card, node = None):
        if node is not None:
            key = state_map[node] if node else state_map['i']
            node_weights = self.avg_strategy[key]
            node_strategy = [node_weights[k] for k in node_weights]
            decision = node_strategy.index(max(node_strategy))
        return decision

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
            self.update_table(h, pi)
        else:
            self.update_table(h, pni)
        
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
            
        self.performance[t] = vsigma
        return vsigma

    def update_table(self, h, pi):
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
        return 'SmartAgent'
