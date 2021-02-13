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

class StrategySuperset:
    def executeStrategy(Game):
        # TODO call superset_douoble & superset_triplet. executeStrategy gets the relentless decorator
        pass

    @relentless
    def superset_solver(self):
        # TODO check if splitable here: rename superset_solver part I:
        #  @relentless
        #  def superset_double(self):
        #       """update doc"""
        # first find the neighbours to remaining questionmarks
        inquestion = set(n for q in self.clues.values()
                         for n in q.neighb_inst
                         if q.clue == '?' and n.clue not in ['?', 'x'])  # TODO discard this simplification

        # most informative intersections start with:
        single = set(n for n in inquestion if n._state == 1)
        candidates = ([inst1, inst2] for inst1, inst2 in product(single, inquestion)
                      if (inst1.isneighb(inst2)) and inst2._state != 0)

        for inst1, inst2 in candidates:
            a = inst1.questionmarks
            b = inst2.questionmarks

            if b.issuperset(a) and bool(a):  # SUPERSET and a was not filled
                # in the meantime whilest iterating over candidates
                remain = (b - a)

                # remaining can be opened
                if inst2._state - inst1._state == 0:  # since inst1 is subset
                    toopen = remain.copy()
                    for n in toopen:
                        self.open(*n.position)

                # remaining are bombs
                elif len(remain) == inst2._state - inst1._state:
                    Position.communicate_bombs(bombs=remain)  # FIXME deprec

            elif inst2._state - inst1._state == len(a.union(b) - a):
                remain = a.union(b) - a
                Position.communicate_bombs(bombs=remain)  # FIXME deprec

        # TODO check if splitable here:
        #  @relentless
        #  def superset_triplet(self):
        #       """update doc"""
        # search for all direct neighbor triplet who share the same questionmarks to make inferrence about bomb location
        inquestion = set(n for q in self.clues.values()
                         for n in q.neighb_inst
                         if q.clue == '?' and n.clue not in ['?', 'x'])

        single = set(n for n in inquestion if n._state == 1)
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
                        and len(union) == len(a) + len(c):  # otherwise the code opens fields which it cannot
                    toopen = remain.copy()
                    for n in toopen:
                        self.open(*n.position)

                    # remaining are bombs
                elif len(remain) == inst2._state - inst1._state - inst3._state:
                    Position.communicate_bombs(bombs=remain)  # fixme: deprec
