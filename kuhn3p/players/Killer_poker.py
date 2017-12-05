import random
from kuhn3p import betting, deck, Player
import itertools
from .player_utilities import UTILITY_DICT

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

tree = {}
treenode = {
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


class SmartAgent(Player):
    def __init__(self):
        self.player = -1
        self.card = -1
        self.tree = tree
        self.hand_index = -1
        self.training_hand = ()

    def start_hand(self, position, card):
        self.player = position
        self.card = card
        iterations = 50
        i = 0
        for t in range(iterations):
            while i < 3:
                self.cfr('', i, t, 1, 1)
                i += 1
        latest_profile = Profile[len(Profile) - 1]
        print(len(latest_profile))
        for node in latest_profile:
            print(node, latest_profile[node])

    def act(self, state, card):
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
        if not h:
            a = random.choice(['k', 'b'])
            number = self.cfr(h + a, i, t, pi, pni)
            return number
        elif h not in Actions:
            hand_options = [x for x in handperm if x[self.player] == self.card]
            hand = random.choice(hand_options)
            self.hand_index = str(hand)
            self.training_hand = hand
            self.tree[self.hand_index] = treenode
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
            if Profile[t][h]['player'] == i:
                Vsigma[a] = self.cfr(
                    h + a, i, t, self.get_action_profile(t, h, a) * pi, pni)
            else:
                Vsigma[a] = self.cfr(
                    h + a, i, t, pi, pni * self.get_action_profile(t, h, a))

            vsigma += self.get_action_profile(t, h, a) * Vsigma[a]

        if Profile[t][h]['player'] == i:
            for a in Actions[h]:
                self.tree[self.hand_index][h]['regrets'][a] += pni * \
                                                               (Vsigma[a] - vsigma)
                self.tree[self.hand_index][h]['strategy'][a] += pi * \
                                                                self.get_action_profile(t, h, a)

            profile = Profile[t]

            for a in Actions[h]:
                actionregret = max(
                    [self.tree[self.hand_index][h]['regrets'][a], 0])
                values = list(self.tree[self.hand_index][h]['regrets'].values())
                normalizedsum = list([max([x, 0]) for x in values])
                regretsum = sum(normalizedsum)
                profile[h]['profile'][a] = actionregret / \
                                           regretsum if regretsum > 0 else 0.5

            profile['hand'] = self.training_hand
            profile['player'] = i
            Profile.append(profile)
        return vsigma

    def get_action_profile(self, t, h, a):
        profile = Profile[t][h]['profile'][a]
        return profile

    def utility(self, h, i, hand):
        utility = UTILITY_DICT.get(h)(i, hand)
        return utility

    def __str__(self):
        return 'SmartAgeet'
