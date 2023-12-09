import numpy as np

from common import CodeBase


class Hand:
    def __init__(self, hand, bid, use_jokers=False):
        self.hand = hand
        self.bid = bid
        self.use_jokers = use_jokers
        self.cardinality = None
        self.diversity = None
        self.hand_values = self.compute_hand_values(hand)
        self.type = self.get_type()

    def get_type(self):
        values = np.array(self.hand_values)
        n_jokers = 0
        if self.use_jokers:
            joker_filter = values == 1
            values = values[~joker_filter]
            n_jokers = np.sum(joker_filter)
        cards, card_counts = np.unique(values, return_counts=True)
        self.cardinality = np.max(card_counts) if len(card_counts) else 0
        self.diversity = len(cards) if len(cards) else 1
        if n_jokers > 0:
            self.cardinality += n_jokers

        if self.cardinality == 5:
            return '5 of a kind'
        elif self.cardinality == 4:
            return '4 of a kind'
        elif self.cardinality == 3:
            if self.diversity == 2:
                return 'Full house'
            else:
                return '3 of a kind'
        elif self.cardinality == 2:
            if self.diversity == 3:
                return '2 pairs'
            else:
                return '1 pair'
        else:
            return 'High card'

    def __str__(self):
        return f'{self.hand} [{self.bid}] --- {self.type} --- {self.cmp_key()}'

    def compute_hand_values(self, hand):
        card_values = []
        for card in hand:
            try:
                card_value = int(card)
            except ValueError:
                if card == 'T':
                    card_value = 10
                elif card == 'J':
                    card_value = 1 if self.use_jokers else 11
                elif card == 'Q':
                    card_value = 12
                elif card == 'K':
                    card_value = 13
                elif card == 'A':
                    card_value = 14
                else:
                    raise ValueError(f'Unknown card: {card}')
            card_values.append(card_value)
        return card_values

    def cmp_key(self):
        return [self.cardinality, -self.diversity]+self.hand_values


class Code(CodeBase):

    def __init__(self):
        super().__init__('D7')
        self.hands = []
        self.joker_hands = []

    def run(self):
        self.greet()

        for line in self.lines:
            self.process_line(line)
            h = self.hands[-1]
            j = self.joker_hands[-1]
            pass

        self.hands.sort(key=lambda x: x.cmp_key())
        self.joker_hands.sort(key=lambda x: x.cmp_key())

        s = self.get_winnings(self.hands)
        print(f'Total winnings: {s}')

        sj = self.get_winnings(self.joker_hands)
        print(f'Total winnings (with jokers): {sj}')

    def process_line(self, line):
        hand, bid = [w.strip() for w in line.split()]
        bid = int(bid)
        self.hands.append(Hand(hand, bid))
        self.joker_hands.append(Hand(hand, bid, use_jokers=True))

    @staticmethod
    def get_winnings(hands):
        ranks = np.arange(1, len(hands)+1)
        bids = np.array([hand.bid for hand in hands])
        winnings = np.sum(ranks * bids)
        return winnings


def test():
    lines = [
        '32T3K 765',
        'T55J5 684',
        'KK677 28',
        'KTJJT 220',
        'QQQJA 483',
    ]

    code = Code()

    for line in lines:
        code.process_line(line)
    for hand in code.hands:
        print(hand)
    print("With jokers:")
    for hand in code.joker_hands:
        print(hand)

    code.hands.sort(key=lambda x: x.cmp_key())
    code.joker_hands.sort(key=lambda x: x.cmp_key())
    print()
    print("After Sort")
    print()
    for hand in code.hands:
        print(hand)
    print("With jokers:")
    for hand in code.joker_hands:
        print(hand)

    print(f'Total winnings: {code.get_winnings(code.hands)}')
    print(f'Total winnings (with jokers): {code.get_winnings(code.joker_hands)}')


if __name__ == '__main__':
    test()
