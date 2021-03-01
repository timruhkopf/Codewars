from itertools import product


def relentless(func):
    def wrapper(self, *args):
        before = True
        after = False
        while before != after:
            before = str(self)
            func(self, *args)
            after = str(self)

    return wrapper


class Strategy_Superset:
    @relentless
    def execute(game):
        """see readme for details on this strategy"""
        Strategy_Superset.double(game)
        Strategy_Superset.triple(game)

    #
    # def __repr__(board):
    #     """visualisation method to derive the current partial board - including all relevant
    #     positions to a superset"""
    #
    #     pass

    def double(game):
        # first find the known neighbours to the remaining questionmarks.
        single, inquestion = Strategy_Superset.find_anreiner(game)

        candidates = ([inst1, inst2] for inst1, inst2 in product(single, inquestion)
                      if (inst1.isneighb(inst2)) and inst2._state != 0)

        for inst1, inst2 in candidates:
            a = inst1.questionmarks
            b = inst2.questionmarks

            if b.issuperset(a) and bool(a):
                # bool(a) STATESAFETY (since recursion or other superset may have
                # reduced the questionmarks in the  meantime)
                remain = (b - a)

                # remaining can be opened
                if inst2._state - inst1._state == 0:  # since inst1 is subset its state must be smaller eq

                    toopen = remain.copy()
                    for n in toopen:
                        if n.clue != '?':  # STATESAFETY
                            game.open(*n.position)

                # remaining are bombs, after 'soft state reduction' on superset's instance;
                # i.e. knowing at least x-bombs must be in the intersection
                elif len(remain) == inst2._state - inst1._state:
                    game.mark_bomb(remain)


            # inst1's questionmarks are a superset to b's questionmarks
            # This branch is essentially the reverse to the first, but
            # the convention of starting with zip(single, inquestion) cuts the
            # number of combinations to look at by half. in turn this branch is necessary
            elif inst2._state - inst1._state == len(a.union(b) - a):
                # look at the following partial example from a larger board
                # 2 3 ? ? *
                # 1 x 2 1 *
                # 1 2 ? ? *
                # * (== a.union(b) - a) can be opened because of 2 & 1
                remain = a.union(b) - a
                game.mark_bomb(remain)

    def triple(game):
        # TODO triple & double's code is very similar: make it Dry (Do not Repeat Yourself)
        # search for all direct neighbor triplet who share the same questionmarks to make inferrence about bomb location
        single, inquestion = Strategy_Superset.find_anreiner(game)
        candidates2 = ([inst1, inst2, inst3] for inst1, inst2, inst3 in product(single, inquestion, single)
                       if (inst1.isneighb(inst2) and inst3.isneighb(inst2)) and inst2._state != 0 and inst1 != inst3)

        for inst1, inst2, inst3 in candidates2:
            a = inst1.questionmarks
            b = inst2.questionmarks
            c = inst3.questionmarks
            union = a.union(c)

            if b.issuperset(union) and bool(a) and bool(b):
                remain = (b - union)

                if inst2._state - inst1._state - inst3._state == 0 \
                        and len(union) == len(a) + len(c):  # they are dissected,
                    # otherwise the code opens fields which  it shouldn't
                    # solves e.g.:
                    # * ? ?   can open *
                    # ? 2 1
                    # ? 1 0
                    toopen = remain.copy()
                    for n in toopen:
                        if n.clue != '?':  # STATESAFETY
                            game.open(*n.position)

                # remaining are bombs
                elif len(remain) == inst2._state - inst1._state - inst3._state:
                    game.mark_bomb(remain)

    def find_anreiner(game):
        """find those positions, that are neighbours to questionmarks and
        of those also find those that are of state one"""
        # CONSIDER; make generator? to ensure statesafety
        inquestion = set(n for q in game.clues.values()
                         for n in q.neighb_inst
                         if q.clue == '?' and n.clue not in ['?', 'x'])  # here is the simplification
        # most informative intersections start with those that have state 1:
        single = set(n for n in inquestion if n._state == 1)
        return single, inquestion
