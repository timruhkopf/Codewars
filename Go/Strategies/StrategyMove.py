from itertools import chain

from ..Board.Group import Group


class StrategyMove:
    def execute_move(board, *positions):
        """todo add more extensive doc
        positions may take multiple values: move("4A", "5A", "6A")"""
        for position in positions:
            r, c = board.parse_position(position)

            if board._occupied(r, c):
                color = ['x', 'o'][len(board.history) % 2]
                board.board[r][c] = color
                neighb = board._find_neighb(r, c)

                # (0) create new group (single stone)
                groupID = len(board.history) + board.handicap
                board.groups.update({groupID: Group(
                    firststone=(r, c),
                    groupID=groupID,
                    liberties=set(n for n in neighb if n not in board.affiliation.keys()),
                    color=color)})
                board.history.append(position)
                board.affiliation.update({(r, c): groupID})

                # (1) same color (including mid stone)
                StrategyMove._merge_same_color(board, neighb, color, groupID, r, c)

                # (2) different colored neighbours: steal liberty
                StrategyMove._different_color_update(board, neighb, color, r, c)

                # (3) check move was no suicide
                # (notice the group above has new affil. after merger)
                if not bool(board.groups[board.affiliation[(r, c)]].liberties):
                    board.rollback(1)
                    raise ValueError('Suicide')

    def _merge_same_color(board, neighb, color, groupID, r, c):
        """merge all stones of same color in neighb. including mid stone"""
        pos_same_col = [n for n in neighb if board.board[n[0]][n[1]] == color]

        if pos_same_col != []:
            # find largest Group (a bit of extra logic for fast moves in mid/end game)
            membersize = [len(board._fetch_group(n).member) for n in pos_same_col]
            pos_max_grsize = pos_same_col[membersize.index(max(membersize))]
            pos_same_col.remove(pos_max_grsize)
            same_col_nomax = [board.groups[id] for id in [board.affiliation[n] for n in pos_same_col]]
            max_id = board.affiliation[pos_max_grsize]

            # merge to max group
            board.groups[max_id].merge(board.groups[groupID], *same_col_nomax)

            # remove mid (new) stone liberty
            board.groups[max_id].liberties.remove((r, c))

            # change the affiliation of all same colored to val of max group aff.
            for tup in (*chain(*[group.member for group in same_col_nomax]), (r, c)):
                board.affiliation[tup] = max_id

    def _different_color_update(board, neighb, color, r, c):
        """steal the liberty (of the new stone at r,c)
        of all different colored neighbours"""
        pos_diff_col = set(board._fetch_group(n) for n in neighb
                           if board.board[n[0]][n[1]] != color
                           and board.board[n[0]][n[1]] != '.')

        if pos_diff_col != []:
            for group in pos_diff_col:
                if (r, c) in group.liberties:
                    group.liberties.remove((r, c))

                # check if group has no liberties
                if not bool(group.liberties):
                    StrategyMove._capture(board, group=group)

    def _capture(board, group):
        """remove group when it has no liberty after _different_color_update
        each member's neighbour's group must be added this members position is a
        new liberty of that neighbour's group."""
        if len(board.history) - 1 in board.capured.keys():
            if {board.parse_position(board.history[-1])} == \
                    board.capured[len(board.history) - 1] and len(group.member) == 1:
                board.rollback(1)
                raise ValueError('Ko')

        board.capured.update({len(board.history): group.member})

        # opposite color
        color = ['x', 'o']
        color.remove(group.color)
        color = color[0]

        # find neighb. of each member & give them the respective liberty!
        member_neighb = list(map(lambda position: board._find_neighb(*position), group.member))
        diff_group = [set(board._fetch_group(n) for n in neighb if board.board[n[0]][n[1]] == color)
                      for neighb in member_neighb]

        for member, ngroups in zip(group.member, diff_group):
            for ngroup in ngroups:
                ngroup.liberties.update({member})

        for i, pos in enumerate(group.member):
            # remove affiliations of all group member:
            board.affiliation.pop(pos)

            # remove member from board
            board.board[pos[0]][pos[1]] = '.'
