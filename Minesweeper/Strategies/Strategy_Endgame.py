from itertools import combinations

from .Strategy_Superset import relentless


class Strategy_Endgame:

    def remain_bomb_count(game):
        remain_q = [_ for _ in game.clues.values() if _._clue == '?']
        # all remaining ? must be bombs due to count
        if game.remain_bomb == len(remain_q):
            game.mark_bomb(remain_q)

        # open all when there are no bombs
        elif game.remain_bomb == 0 and len(remain_q) != 0:
            for _ in remain_q:
                game.open(*_.position)

    @relentless
    def sequential_combinations(game):
        """"""
        remain_q = set(q for q in game.clues.values() if q._clue == '?')
        anreiner = set(n for q in game.clues.values()
                       for n in q.neighb_inst
                       if q.clue == '?' and n.clue not in ['?', 'x'])

        potential_bomb = set()
        for bombcombi in combinations(remain_q, game.remain_bomb):
            # update the states for this trial
            for bomb in bombcombi:
                for n in bomb.neighb_inst:
                    n._state -= 1

            # check if this is a valid combinations (all anreiner are happy)
            if set(a._state for a in anreiner) == {0}:
                potential_bomb.update(set(bombcombi))

            # undo this trial
            for bomb in bombcombi:
                for n in bomb.neighb_inst:
                    n._state += 1

        untouched = remain_q - potential_bomb
        for node in untouched:
            game.open(*node.position)
