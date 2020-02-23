from functools import reduce
from collections import Counter
from operator import sub


class PokerCard(object):
    def __init__(self, card):
        card = reduce(
            lambda a, kv: a.replace(*kv),
            {'T': '10', 'J': '11', 'Q': '12', 'K': '13', 'A': '14'}.items(),
            card)

        # b = {'i': 'I', 's': 'S'}
        # for x, y in b.items():
        #     a = a.replace(x, y)

        self.value = int(card[:-1])
        self.suit = card[-1]

    def __repr__(self):
        value = reduce(
            lambda a, k,: a.replace(k[1], k[0]),
            {'T': '10', 'J': '11', 'Q': '12', 'K': '13', 'A': '14'}.items(),
            str(self.value))

        return value + self.suit

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

    def kicker(self):
        # a not used card!
        pass

    def myrank(self):
        suitlist = list(x.suit for x in self.cards)
        valuelist = list(x.value for x in self.cards)
        counter = Counter(valuelist)

        def highcard():
            return max(valuelist)

        def pair():
            return 2 in counter.values()

        def two_pair():
            vals = list(counter.values())
            vals.sort()
            return vals == [1, 2, 2]

        def three_of_a_kind():
            return 3 in counter.values()

        def straight():
            valuelist.sort()
            return set(map(sub, valuelist[1:], valuelist[:-1])) == {1}

        def flush():
            return len(set(suitlist)) == 1

        def full_house():  # Fixme how to determine the kicker?
            return three_of_a_kind() & pair()

        def four_of_a_kind():  # FIXME kicker case
            return 4 in counter.values()

        def straight_flush():
            return flush() & straight()

        def royal_flush():
            return straight_flush() & (14 in counter.keys())

        self.high = highcard()

        isit = [True, pair(), two_pair(), three_of_a_kind(), straight(), flush(),
                full_house(), four_of_a_kind(), straight_flush(), royal_flush()]

        # first occurence is the highest rank
        self.rank = isit[::-1].index(True)

    def compare_with(self, other):
        """
        The result of your poker hand compare can be one of these 3 options:
        [ "Win", "Tie", "Loss" ]

        they can make from the seven cards comprising their two-hole cards and
        the five community cards. A player may use both of their own two hole
        cards, only one, or none at all, to form their final five-card hand.
        If the five community cards form the player's best hand, then the
        player is said to be playing the board and can only hope to split the
        pot, because each other player can also use the same five cards
        to construct the same hand.

        Nevertheless, one must be careful in determining the best hand;
        if the hand involves fewer than five cards, (such as two pair or three
        of a kind), then kickers are used to settle ties. The card's numerical
        rank is of sole importance; suit values are irrelevant in hold 'em.
        """
        assert (isinstance(other, PokerHand))

        choices = ['royal', 'straight_flush', 'four', 'full', 'flush', 'straight', 'three', 'two_pair', 'pair', 'high']
        myhand = choices[self.rank]
        ophand = choices[other.rank]

        print('\n', 'player: ', myhand, str(self.high), '\n',
              'op: ', ophand, str(other.high))


        if self.rank < other.rank:
            return 'Win'
        elif self.rank > other.rank:
            return 'Loss'

        elif self.rank == other.rank:
        # Fixme look at kickers ! # also to determine if 5 e.g. flushes win over one another
            if self.high > other.high:
                return 'Win'
            elif self.high < other.high:
                return 'Loss'
            return 'Tie'


if __name__ == '__main__':
    # card = PokerCard('TH')
    # card1 = PokerCard('JH')
    #
    # # four = PokerHand("JS JD JC JH AD")
    # pair2 = PokerHand("2S 2H 4H 5S 4C")
    # straight = PokerHand("2S 3H 4H 5S 6C")
    # fullhouse = PokerHand("2S AH 2H AS AC")
    # flushS = PokerHand("KS AS TS QS JS")
    # flushH = PokerHand("2H 3H 4H 5H 6H")
    #
    # flushS.compare_with(flushH) == 'Loss'

    def runTest(msg, expected, hand, other):
        player, opponent = PokerHand(hand), PokerHand(other)
        assert (player.compare_with(opponent) == expected)
        print(expected)
        print("{}: '{}' against '{}'".format(msg, hand, other))


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

    # runTest("Highest pair wins", "Loss", "6S AD 7H 4S AS", "AH AC 5H 6H 7S")
    # runTest("Highest card wins", "Win", "4S 5H 6H TS AC", "3S 5H 6H TS AC")

    print('')
