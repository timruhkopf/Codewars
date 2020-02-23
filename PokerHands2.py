from operator import sub

class PokerCard(object):
    def __init__(self, card):
        self.card = card

        d = {'T': '10', 'J': '11', 'Q': '12', 'K': '13', 'A': '14'}
        for k, v in d.items():
            card = card.replace(k, v)

        self.value = int(card[:-1])
        self.suit = card[-1]

    def __repr__(self):
        return str(self.card)

    # def __eq__(self, other):
    #     return self.value == other.value
    # #

    # def __ge__(self, other):
    #     return self.value >= other.value

    def __gt__(self, other):
        return self.value > other.value

    # def eq_suit(self, other):
    #     return self.suit == other.suit


class PokerHand(object):
    def __init__(self, hand):
        cards = hand.split(' ')
        self.cards = [PokerCard(card) for card in cards]
        self.myrank()

    def myrank(self):
        # (0) (pair, twopair, three, four) -------------------------------------
        d_values = {k: [] for k in set(card.value for card in self.cards)}
        for card in self.cards:
            d_values[card.value].append(card)

        multiples = {k: v for k, v in d_values.items() if len(v) > 1}
        multiples_len = {k: len(v) for k, v in multiples.items()}

        others = [v[0] for v in d_values.values() if len(v) == 1]

        if len(others) == 5:  # highcard
            self.rank = 0
            self.kicker = max(others)

        if len(multiples) == 1:  # pair, three, four
            typ = len(list(multiples.values())[0]) - 1
            self.rank = (1, 3, 7)[typ]
            self.kicker = list(multiples.keys())[0]

        if len(multiples) == 2:
            if set(multiples_len.keys()) == {2}:  # twopair
                self.rank = 2
                self.kicker = max(multiples.keys())

            elif set(multiples_len.keys()) == {2, 3}:  # fullhouse
                self.rank = 6
                self.kicker = max(multiples.keys())

        valuelist = list(x.value for x in self.cards)

        def straight():
            valuelist.sort()
            return set(map(sub, valuelist[1:], valuelist[:-1])) == {1}

        def flush():
            return len(set(x.suit for x in self.cards)) == 1

        def straight_flush():
            return flush() & straight()

        def royal_flush():
            return straight_flush() & (max(self.cards).value == 14)


        if royal_flush():
            self.rank = 9
            self.kicker = 'CDHS'.index(self.cards[0].suit)

        elif straight_flush():
            self.rank = 8
            self.kicker = max(self.cards)

        elif straight():
            self.rank = 4
            self.kicker = max(self.cards)

        elif flush():
            self.rank = 5
            self.kicker = 'CDHS'.index(self.cards[0].suit)

            # kicker2 = max(self.cards)




    def compare_with(self, opponent):

        # determine kicker2 from leftovers after removing joint cards from others.
        # if len(multiples) == 1: # pair, three, four
        #     o = set(opponent.others)
        #     me = set(others)
        #     self.kicker2 = me - o

        # myrank's content must be here for others calculation (clean

        # (0) check rank win
        if self.rank > opponent.rank:
            return 'Win'
        elif self.rank < opponent.rank:
            return 'Loss'
        elif self.rank == opponent.rank:

            if self.kicker > opponent.kicker:
                return 'Win'
            elif self.kicker < opponent.kicker:
                return 'Loss'
            elif self.kicker == opponent.kicker:
                pass


if __name__ == '__main__':
    card = PokerCard('TH')
    card1 = PokerCard('JH')

    # three = PokerHand("AH AC 5H 6H AS")
    # three1 = PokerHand("AH AC 5H 7H AS")
    # three.compare_with(three1)

    # high = PokerHand("3S 6H QH 5S 4C")
    # pair = PokerHand("3S 6H 4H 5S 4C")
    pair2 = PokerHand("2S 2H 4H 5S 4C")
    three = PokerHand("AH AC 5H 6H AS")
    straight = PokerHand("2S 3H 4H 5S 6C")
    flush = PokerHand("2S AS TS QS JS")
    full_house = PokerHand("2S AH 2H AS AC")
    four = PokerHand("JS JD JC JH AD")
    straight_flush = PokerHand("2H 3H 4H 5H 6H")
    royal_flush = PokerHand("AS KS QS JS TS")
