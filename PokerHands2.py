from operator import sub


#
# class Multiples(object):
#     """Object for High, pair, pair2, three, four"""
#     def __init__(self, ):
#         pass
#
#     def __gt__(self, other):
#         if self.rank > other.rank:
#             return True
#         if self.rank < other.rank:
#             return False
#
# class Fivecard(object):
#     def __init__(self):
#         pass
#     def __gt__(self, other):
#         self.rank > other.rank

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

    def __eq__(self, other):
        return self.value == other.value

    # def __ge__(self, other):
    #     return self.value >= other.value

    def __lt__(self, other):
        return self.value < other.value     # for sorting

    def __gt__(self, other):    # for set
        return self.value > other.value

    def __hash__(self):     # for set
        return self.value

    # def eq_suit(self, other):
    #     return self.suit == other.suit


class PokerHand(object):
    def __init__(self, hand):
        cards = hand.split(' ')
        self.cards = [PokerCard(card) for card in cards]
        self.cards.sort()
        self.myrank()
        print(self)

    def __eq__(self, other): # short circuit
        return (self.rank == other.rank) & (self.high_incombo == other.high_incombo)

    def __gt__(self, other):
        if self.rank > other.rank:
            return True

        if self.rank == other.rank:
            if self.high_incombo > other.high_incombo:
                return True
            elif self.rank in (0, 1, 2, 3, 7):  # corner case: max of non shared self.other wins
                if self.high_incombo == other.high_incombo:
                    kicker_me = max(set(self.others) - set(other.others))
                    kicker_o = max(set(other.others) - set(self.others))
                    if kicker_me > kicker_o:
                        return True
        else:
            return False

    def __lt__(self, other):
        if self.rank < other.rank:
            return True

        if self.rank == other.rank:
            if self.high_incombo < other.high_incombo:
                return True
            elif self.rank in (1, 2, 3, 7):  # corner case: max of non shared self.other wins
                if self.high_incombo == other.high_incombo:
                    kicker_me = max(set(self.others) - set(other.others))
                    kicker_o = max(set(other.others) - set(self.others))
                    if kicker_me < kicker_o:
                        return True
        else:
            return False


    def __repr__(self):
        hand = ['highcard', 'pair', 'two_pair', 'three', 'straight', 'flush',
                'full_house', 'four', 'straight_flush', 'royal_flush'][self.rank]
        return 'rank {}, {}, {}, high_incombo: {}'.format(self.rank, hand, self.cards, self.high_incombo)

    def myrank(self):
        # (0) (pair, twopair, three, four, fullhouse related) ------------------
        d_values = {k: [] for k in set(card.value for card in self.cards)}
        for card in self.cards:
            d_values[card.value].append(card)

        multiples = {k: v for k, v in d_values.items() if len(v) > 1}
        multiples_len = {k: len(v) for k, v in multiples.items()}

        self.others = [v[0] for v in d_values.values() if len(v) == 1]

        def royal_flush():
            return straight_flush() & (max(self.cards).value == 14)

        def straight_flush():
            return flush() & straight()

        def fullhouse():
            return (len(multiples) == 2) & (set(multiples_len.values()) == {2, 3})

        def flush():
            return len(set(x.suit for x in self.cards)) == 1

        def straight():
            valuelist = list(x.value for x in self.cards)
            valuelist.sort()
            return set(map(sub, valuelist[1:], valuelist[:-1])) == {1}

        def twopair():
            return (len(multiples) == 2) & (set(multiples_len.values()) == {2})

        if royal_flush():
            self.rank = 9
            self.high_incombo = 'CDHS'.index(self.cards[0].suit)

        elif straight_flush():
            self.rank = 8
            self.high_incombo = max(self.cards).value

        elif fullhouse():
            self.rank = 6
            self.high_incombo = max(multiples.keys())

        elif flush():
            self.rank = 5
            self.high_incombo = 'CDHS'.index(self.cards[0].suit)
            # high_incombo2 = max(self.cards.value)  # value

        elif straight():
            self.rank = 4
            self.high_incombo = max(self.cards).value

        elif len(multiples) == 1:  # pair, three, four
            typ = len(list(multiples.values())[0]) - 2
            self.rank = (1, 3, 7)[typ]
            self.high_incombo = list(multiples.keys())[0]  # FIXME: Other will retain this value!

        elif twopair():
            self.rank = 2
            self.high_incombo = max(multiples.keys())

        else:  # highcard
            self.rank = 0
            self.high_incombo = max(self.cards).value

    def compare_with(self, opponent):
        assert (isinstance(opponent, PokerHand))

        # same hand short circuit
        if self.cards == opponent.cards:
            return 'Tie'

        # different hands: rank win
        if self > opponent:
            return 'Win'
        elif self < opponent:
            return 'Loss'
        else:
            return 'Tie'


        # # (0) check rank win
        # if self.rank > opponent.rank:
        #     return 'Win'
        # elif self.rank < opponent.rank:
        #     return 'Loss'
        # elif self.rank == opponent.rank:
        #
        #     if self.high_incombo > opponent.high_incombo:
        #         return 'Win'
        #     elif self.high_incombo < opponent.high_incombo:
        #         return 'Loss'
        #     elif self.rank in (1, 2, 3, 7):  # corner case: max of non shared self.other wins
        #         if self.high_incombo == opponent.high_incombo:
        #             kicker_me = max(set(self.others) - set(opponent.others))
        #             kicker_o = max(set(opponent.others) - set(self.others))
        #             if kicker_me > kicker_o:
        #                 return 'Win'
        #             elif kicker_me < kicker_o:
        #                 return 'Loss'
        #     else:
        #         return 'Tie'
        #
        #     # all other 5 card cases


if __name__ == '__main__':
    card = PokerCard('TH')
    card1 = PokerCard('JH')

    # three = PokerHand("AH AC 5H 6H AS")
    # three1 = PokerHand("AH AC 5H 7H AS")
    # three.compare_with(three1)

    # high = PokerHand("3S 6H QH 5S 4C")
    # pair = PokerHand("3S 6H 4H 5S 4C")
    # pair2 = PokerHand("2S 2H 4H 5S 4C")
    # three = PokerHand("AH AC 5H 6H AS")
    # straight = PokerHand("2S 3H 4H 5S 6C")
    # flush = PokerHand("2S AS TS QS JS")
    # full_house = PokerHand("2S AH 2H AS AC")
    # four = PokerHand("JS JD JC JH AD")
    # straight_flush = PokerHand("2H 3H 4H 5H 6H")
    # royal_flush = PokerHand("AS KS QS JS TS")

    four2 = PokerHand("JS JD JC JH 3D")


    def runTest(msg, expected, hand, other):
        player, opponent = PokerHand(hand), PokerHand(other)
        print(expected)
        print("{}: '{}' against '{}'".format(msg, hand, other))
        assert (player.compare_with(opponent) == expected)


    runTest("Highest straight flush wins", "Loss", "2H 3H 4H 5H 6H", "KS AS TS QS JS")
    runTest("Straight flush wins of 4 of a kind", "Win", "2H 3H 4H 5H 6H", "AS AD AC AH JD")
    runTest("Highest 4 of a kind wins", "Win", "AS AH 2H AD AC", "JS JD JC JH 3D")
    runTest("4 Of a kind wins of full house", "Loss", "2S AH 2H AS AC", "JS JD JC JH AD")
    runTest("Full house wins of flush", "Win", "2S AH 2H AS AC", "2H 3H 5H 6H 7H")
    runTest("Highest flush wins", "Win", "AS 3S 4S 8S 2S", "2H 3H 5H 6H 7H")
    runTest("Flush wins of straight", "Win", "2H 3H 5H 6H 7H", "2S 3H 4H 5S 6C")
    runTest("Equal straight is tie", "Tie", "2S 3H 4H 5S 6C", "3D 4C 5H 6H 2S")
    runTest("Straight wins of three of a kind", "Win", "2S 3H 4H 5S 6C", "AH AC 5H 6H AS")
    runTest("3 Of a kind wins of two pair", "Loss", "2S 2H 4H 5S 4C", "AH AC 5H 6H AS")
    runTest("2 Pair wins of pair", "Win", "2S 2H 4H 5S 4C", "AH AC 5H 6H 7S")
    runTest("Highest pair wins", "Loss", "6S AD 7H 4S AS", "AH AC 5H 6H 7S")
    runTest("Pair wins of nothing", "Loss", "2S AH 4H 5S KC", "AH AC 5H 6H 7S")
    runTest("Highest card loses", "Loss", "2S 3H 6H 7S 9C", "7H 3C TH 6H 9S")
    runTest("Highest card wins", "Win", "4S 5H 6H TS AC", "3S 5H 6H TS AC")
    runTest("Equal cards is tie", "Tie", "2S AH 4H 5S 6C", "AD 4C 5H 6H 2C")

    print('')
