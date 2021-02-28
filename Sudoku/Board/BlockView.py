from itertools import chain

from Sudoku.Board.ListSliceView import ListSliceView, ListViewIterator


class BlockView:
    def __init__(self, aproblem):
        """
        Creates a block view on aproblem; i.e. a list of "lists" that are in fact
        references to the aproblem object - and not copies of it
        :param aproblem:
        """
        self.aproblem = aproblem
        self.blocks = [[ListSliceView(aproblem[rref + i], start=cref, alen=3) for i in range(3)]
                       for rref in (0, 3, 6) for cref in (0, 3, 6)]

    def __getitem__(self, i):
        return list(chain(*self.blocks[i]))

    def __len__(self):
        return len(self.blocks)

    def __iter__(self):
        return ListViewIterator(self)


if __name__ == '__main__':
    problem = [[0, 9, 0, 0, 7, 1, 0, 0, 4],
               [2, 0, 0, 0, 0, 0, 0, 7, 0],
               [0, 0, 3, 0, 0, 0, 2, 0, 0],
               [0, 0, 0, 9, 0, 0, 0, 3, 5],
               [0, 0, 0, 0, 1, 0, 0, 8, 0],
               [7, 0, 0, 0, 0, 8, 4, 0, 0],
               [0, 0, 9, 0, 0, 6, 0, 0, 0],
               [0, 1, 7, 8, 0, 0, 0, 0, 0],
               [6, 0, 0, 0, 2, 0, 7, 0, 0]]

    trueblocks = [[[0, 9, 0], [2, 0, 0], [0, 0, 3]],  # block 1
                  [[0, 7, 1], [0, 0, 0], [0, 0, 0]],  # block 2 ...
                  [[0, 0, 4], [0, 7, 0], [2, 0, 0]],
                  [[0, 0, 0], [0, 0, 0], [7, 0, 0]],
                  [[9, 0, 0], [0, 1, 0], [0, 0, 8]],
                  [[0, 3, 5], [0, 8, 0], [4, 0, 0]],
                  [[0, 0, 9], [0, 1, 7], [6, 0, 0]],
                  [[0, 0, 6], [8, 0, 0], [0, 2, 0]],
                  [[0, 0, 0], [0, 0, 0], [7, 0, 0]]]
    blocks = BlockView(problem)

    assert blocks[0] == [0, 9, 0, 2, 0, 0, 0, 0, 3]
    assert blocks[1] == [0, 7, 1, 0, 0, 0, 0, 0, 0]
    assert blocks[2] == [0, 0, 4, 0, 7, 0, 2, 0, 0]
    assert blocks[3] == [0, 0, 0, 0, 0, 0, 7, 0, 0]
    assert blocks[4] == [9, 0, 0, 0, 1, 0, 0, 0, 8]
    assert blocks[8] == [0, 0, 0, 0, 0, 0, 7, 0, 0]
