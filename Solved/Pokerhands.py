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

    def __eq__(self, other):
        return (self.value == other.value)  # & (self.suit == other.suit)

    def __lt__(self, other):  # for sorting
        return self.value < other.value

    def __gt__(self, other):  # for set
        return self.value > other.value

    def __hash__(self):  # for set behaviour on values
        return self.value


class PokerHand(object):
    def __init__(self, hand):
        cards = hand.split(' ')
        self.cards = [PokerCard(card) for card in cards]
        self.cards.sort()
        self.myrank()

        # print(self)

    def __repr__(self):
        hand = ['highcard', 'pair', 'two_pair', 'three', 'straight', 'flush',
                'full_house', 'four', 'straight_flush', 'royal_flush'][self.rank]
        return 'rank {}, {}, {}'.format(self.rank, hand, self.cards)

    def myrank(self):
        # looking for pair orders
        d_values = {k: [] for k in set(card.value for card in self.cards)}
        for card in self.cards:
            d_values[card.value].append(card)

        self.multiples = [v for v in d_values.values() if len(v) > 1]
        self.multiples.sort(key=len, reverse=True)  # for full house relevant
        self.remain = {v[0] for v in d_values.values() if len(v) == 1}

        def royal_flush():
            return straight_flush() & (max(self.cards).value == 14)

        def straight_flush():
            return flush() & straight()

        def fullhouse():
            return (len(self.multiples) == 2) & (set(len(l) for l in self.multiples) == {2, 3})

        def flush():
            return len(set(x.suit for x in self.cards)) == 1

        def straight():
            valuelist = list(x.value for x in self.cards)
            valuelist.sort()
            return set(map(sub, valuelist[1:], valuelist[:-1])) == {1}

        def twopair():
            return (len(self.multiples) == 2) & (set(len(l) for l in self.multiples) == {2})

        bo = [royal_flush(), straight_flush(), fullhouse(), flush(), straight(), twopair(), True]
        self.rank = max([v for v, b in zip([9, 8, 6, 5, 4, 2, 0], bo) if b])

        if len(self.multiples) == 1:  # pair, three, four
            self.rank = (1, 3, 7)[len(self.multiples[0]) - 2]

    def compare_with(self, other):
        assert (isinstance(other, PokerHand))

        if self.rank > other.rank:
            return 'Win'
        if self.rank < other.rank:
            return 'Loss'
        elif self.rank == other.rank:

            if self.rank in (1, 2, 3, 6, 7):  # check non-empty multiples
                for a, b in zip(self.multiples, other.multiples):
                    if a[0] > b[0]:
                        return 'Win'
                    elif a[0] < b[0]:
                        return 'Loss'
                    else:
                        continue

            if self.rank in (0, 1, 2, 3, 4, 5, 7, 8):   # check unused cards
                mine = self.remain - other.remain
                oppo = other.remain - self.remain
                if any((mine == set(), oppo == set())):
                    return 'Tie'
                elif max(mine) > max(oppo):
                    return 'Win'
                elif max(mine) < max(oppo):
                    return 'Loss'

        return 'Tie'



if __name__ == '__main__':
    # (PokerCard behaviour) ----------------------------------------------------
    # card = PokerCard('TH')
    # card1 = PokerCard('JH')
    # card2 = PokerCard('JC')
    # card3 = PokerCard('3S')
    # card4 = PokerCard('4S')
    #
    # card < card1  # higher value*, same suit
    # card1 > card2  # same value, different suit*
    # card == card  # identity
    #
    # a = set([card, card1, card2])
    # b = set([card, card1])
    #
    # c = a - b
    # c == set([card2])
    #
    # d = b - a
    # d == set()
    #
    # c > d  # due to len
    #
    # max(c)
    # # max(d) # will not work, as empty sequence
    # max([card, card1, card2])
    #
    # e = set([*b, card3, card4])
    # f = set([*b, card2])
    #
    # g = f - e
    # h = e - f
    #
    # max(g) > max(h)

    # (PokerHand identification) -----------------------------------------------
    high = PokerHand("3S 6H QH 5S 4C")
    pair = PokerHand("3S 6H 4H 5S 4C")
    pair2 = PokerHand("2S 2H 4H 5S 4C")
    three = PokerHand("AH AC 5H 6H AS")
    straight = PokerHand("2S 3H 4H 5S 6C")
    flush = PokerHand("2S AS TS QS JS")
    full_house = PokerHand("2S AH 2H AS AC")
    four = PokerHand("JS JD JC JH AD")
    straight_flush = PokerHand("2H 3H 4H 5H 6H")
    royal_flush = PokerHand("AS KS QS JS TS")

    # (PokerHand behaviour) ----------------------------------------------------
    def runTest(msg, expected, hand, other):
        player, opponent = PokerHand(hand), PokerHand(other)
        print(expected)
        print("{}: '{}'  {} against '{}'".format(msg, hand, expected, other))
        assert (player.compare_with(opponent) == expected)


    # runTest("Highest straight flush wins", "Loss", "2H 3H 4H 5H 6H", "KS AS TS QS JS")
    # runTest("Straight flush wins of 4 of a kind", "Win", "2H 3H 4H 5H 6H", "AS AD AC AH JD")
    # runTest("Highest 4 of a kind wins", "Win", "AS AH 2H AD AC", "JS JD JC JH 3D")
    # runTest("4 Of a kind wins of full house", "Loss", "2S AH 2H AS AC", "JS JD JC JH AD")
    # runTest("Full house wins of flush", "Win", "2S AH 2H AS AC", "2H 3H 5H 6H 7H")
    # runTest("Highest flush wins", "Win", "AS 3S 4S 8S 2S", "2H 3H 5H 6H 7H")
    # runTest("Flush wins of straight", "Win", "2H 3H 5H 6H 7H", "2S 3H 4H 5S 6C")
    # runTest("Equal straight is tie", "Tie", "2S 3H 4H 5S 6C", "3D 4C 5H 6H 2S")
    # runTest("Straight wins of three of a kind", "Win", "2S 3H 4H 5S 6C", "AH AC 5H 6H AS")
    # runTest("3 Of a kind wins of two pair", "Loss", "2S 2H 4H 5S 4C", "AH AC 5H 6H AS")
    # runTest("2 Pair wins of pair", "Win", "2S 2H 4H 5S 4C", "AH AC 5H 6H 7S")
    # runTest("Highest pair wins", "Loss", "6S AD 7H 4S AS", "AH AC 5H 6H 7S")
    # runTest("Pair wins of nothing", "Loss", "2S AH 4H 5S KC", "AH AC 5H 6H 7S")
    # runTest("Highest card loses", "Loss", "2S 3H 6H 7S 9C", "7H 3C TH 6H 9S")
    # runTest("Highest card wins", "Win", "4S 5H 6H TS AC", "3S 5H 6H TS AC")
    # runTest("Equal cards is tie", "Tie", "2S AH 4H 5S 6C", "AD 4C 5H 6H 2C")
    # runTest('higher flush wins (highcard)', 'Win', '4C 5C 9C 8C KC', '8C 9C 5C 3C TC')
    # runTest('straight loses to flush', 'Loss', 'QC KH TS JS AH', 'JH AH TH KH QH')
    # runTest('', 'Loss', '3S 8S 9S 5S KS', 'JH 8H AH KH QH')
    # runTest('', 'Win', 'JH AH TH KH QH', 'QC KH TS JS AH')
    # runTest('high card KS, but going down', 'Win', 'TS KS 5S 9S AC', 'JH 8S TH AH QH')
    # runTest('flush flush 8C kicker', 'Win', '4C 5C 9C 8C KC', '3S 8S 9S 5S KS')
    # runTest('fullhouse fullhouse', 'Loss', '3D 2H 3H 2C 2D', '2H 2C 3S 3H 3D')
    # runTest('pair pair', 'Loss', 'KS 8D 4D 9S 4S', 'KD 4S KC 3H 8S')

    # runTest('', 'Loss', '2D 6D 3D 4D 5D', 'JH 9H TH KH QH')
    runTest('', 'Win', 'QC KH TS JS AH' ,'JS QS 9H TS KH')

print('')
