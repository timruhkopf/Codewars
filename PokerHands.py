from collections import Counter
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
    #     assert (isinstance(other, PokerCard))
    #     return self.value == other.value
    #
    # def __gt__(self, other):
    #     assert (isinstance(other, PokerCard))
    #     return self.value > other.value


class PokerHand(object):
    def __init__(self, hand):
        self.cards = [PokerCard(card) for card in hand.split(' ')]
        self.myrank()
        print(self.__repr__())

    def __repr__(self):
        hand = ['highcard', 'pair', 'two_pair', 'three', 'straight', 'flush',
                'full_house', 'four', 'straight_flush', 'royal_flush'][self.rank]

        return 'rank {}, {}, {}, kicker: {}'.format(self.rank, self.cards, hand, self.kicker)

    def myrank(self):

        suitlist = list(x.suit for x in self.cards)
        valuelist = list(x.value for x in self.cards)
        counter = Counter(valuelist)

        # high_card
        self.rank = 0
        self.kicker = max(valuelist)

        def pair():
            if 2 in counter.values():
                self.rank = 1

                self.kicker = [k for k, v in counter.items() if v == 2]
                # self.suit = max(['CDHS'.index(x.suit) for x in self.cards if (x.value in self.kicker)])
                self.multicard = max([k for k, v in counter.items() if v != 2])
                return True
            return False

        def pair2():
            multicard = [k for k, v in counter.items() if v == 2]
            if (2 in counter.values()) & (len(multicard) == 2):
                self.rank = 2
                self.kicker = max(multicard)
                # self.suit = max(['CDHS'.index(x.suit) for x in self.cards if x.value == self.kicker])
                self.multicard = max([k for k, v in counter.items() if v != 2])

        def three():
            if 3 in counter.values():
                self.rank = 3
                self.kicker = [k for k, v in counter.items() if v == 3]
                # self.suit = max(['CDHS'.index(x.suit) for x in self.cards if (x.value in self.kicker)])
                self.multicard = max([k for k, v in counter.items() if v != 3])
                return True
            return False

        def straight():
            valuelist.sort()
            if set(map(sub, valuelist[1:], valuelist[:-1])) == {1}:
                self.rank = 4
                self.kicker = max(valuelist)
                return True
            return False

        def flush():
            if len(set(suitlist)) == 1:
                self.rank = 5
                self.kicker = 'CDHS'.index(self.cards[0].suit)

                return True
            return False

        def full_house():
            if (3 in counter.values()) & (2 in counter.values()):
                self.rank = 6
                self.kicker = max(valuelist)  # Fixme how to determine the kicker?

        def four():
            if 4 in counter.values():
                self.rank = 7
                self.kicker = [k for k, v in counter.items() if v == 4]
                self.multicard = max([k for k, v in counter.items() if v != 4])

        def straight_flush():
            if flush() & straight():
                self.rank = 8
                self.kicker = max(valuelist)
                return True
            return False

        def royal_flush():
            if straight_flush() & (14 in counter.keys()):
                self.rank = 9
                self.kicker = 'CDHS'.index(self.cards[0].suit)

        # early stopping
        for f in [royal_flush, straight_flush, four, full_house, flush,
                  straight, three, pair2, pair]:
            f()
            if self.rank != 0:
                break

    def compare_with(self, other):
        assert (isinstance(other, PokerHand))

        # (0) check rank win
        if self.rank > other.rank:
            return 'Win'
        elif self.rank < other.rank:
            return 'Loss'
        elif self.rank == other.rank:

            if self.kicker > other.kicker:
                return 'Win'
            elif self.kicker < other.kicker:
                return 'Loss'
            elif self.kicker == other.kicker:
                # (1.1) pair, pair2, three, four (check kicker)
                if self.rank in (1, 2, 3, 7):
                    # if self.suit > other.suit:
                    #     return 'Win'
                    # elif self.suit < other.suit:
                    #     return 'Loss'

                    if self.multicard > other.multicard:
                        return 'Win'
                    if self.multicard < other.multicard:
                        return 'Loss'
                return 'Tie'


if __name__ == '__main__':
    # card = PokerCard('TH')
    # card1 = PokerCard('JH')

    #
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


    def runTest(msg, expected, hand, other):
        player, opponent = PokerHand(hand), PokerHand(other)
        print(expected)
        print("{}: '{}' against '{}'".format(msg, hand, other))
        assert (player.compare_with(opponent) == expected)


    runTest("Highest pair wins", 'Loss', '6S AD 7H 4S AS', 'AH AC 5H 6H 7S' ) # FIXME! Thisone expects the value of kicker to be 4 and 5 respectively : the highest NON! shared value!!

    runTest("Straight flush wins of 4 of a kind", "Win", "2H 3H 4H 5H 6H", "AS AD AC AH JD")

    runTest("4 Of a kind wins of full house", "Loss", "2S AH 2H AS AC", "JS JD JC JH AD")
    runTest("Full house wins of flush", "Win", "2S AH 2H AS AC", "2H 3H 5H 6H 7H")

    runTest("Flush wins of straight", "Win", "2H 3H 5H 6H 7H", "2S 3H 4H 5S 6C")
    runTest("Equal straight is tie", "Tie", "2S 3H 4H 5S 6C", "3D 4C 5H 6H 2S")
    runTest("Straight wins of three of a kind", "Win", "2S 3H 4H 5S 6C", "AH AC 5H 6H AS")
    runTest("3 Of a kind wins of two pair", "Loss", "2S 2H 4H 5S 4C", "AH AC 5H 6H AS")
    runTest("2 Pair wins of pair", "Win", "2S 2H 4H 5S 4C", "AH AC 5H 6H 7S")

    runTest("Pair wins of nothing", "Loss", "2S AH 4H 5S KC", "AH AC 5H 6H 7S")
    runTest("Highest card loses", "Loss", "2S 3H 6H 7S 9C", "7H 3C TH 6H 9S")
    runTest("UnEqual straight is loss", "Loss", "2S 3H 4H 5S 6C", "3D 4C 5H 6H 7S")
    runTest("Equal cards is tie", "Tie", "2S AH 4H 5S 6C", "AD 4C 5H 6H 2C")
    runTest("Highest flush wins", "Win", "AS 3S 4S 8S 2S", "2H 3H 5H 6H 7H")
    runTest("Highest 4 of a kind wins", "Win", "AS AH 2H AD AC", "JS JD JC JH 3D")

    runTest("Highest straight flush wins", "Loss", "2H 3H 4H 5H 6H", "KS AS TS QS JS")

    runTest("Highest pair wins", "Loss", "6S AD 7H 4S AS", "AH AC 5H 6H 7S")
    runTest("Highest card wins", "Win", "4S 5H 6H TS AC", "3S 5H 6H TS AC")

    print('')
