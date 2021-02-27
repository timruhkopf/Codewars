import collections


class ListSliceView(collections.Sequence):

    def __init__(self, alist, start, alen):
        """
        A read and writable view of a list slice (shared values) - pointer arithmetic:
        idea taken from :
        https://stackoverflow.com/questions/3485475/can-i-create-a-view-on-a-python-list

        :param alist: some list, on which the view works
        :param start: start index in alist, (where view begins)
        :param alen: length of view
        """
        self.alist = alist
        self.start = start
        self.alen = alen

    def __repr__(self):
        return str(self.alist[self.start: self.start + self.alen])

    def __len__(self):
        return self.alen

    # READABILITY ----------------
    def adj(self, i):
        """shift to the appropriate part of the list"""
        if i < 0: i += self.alen
        return i + self.start

    def __getitem__(self, i):
        return self.alist[self.adj(i)]

    # WRITEABLE SLICE ----------
    # not strictly necessary though
    def __setitem__(self, i, v):
        self.alist[self.adj(i)] = v

    def __delitem__(self, i, v):
        del self.alist[self.adj(i)]
        self.alen -= 1

    def insert(self, i, v):
        self.alist.insert(self.adj(i), v)
        self.alen += 1

    # ITERABLE -------------------------
    # (needed in Blockview getitem *self.blocks)
    def __iter__(self):
        return ListViewIterator(self)


class ListViewIterator:
    def __init__(self, listview):
        self._listview = listview
        self._index = 0

    def __next__(self):
        if self._index < len(self._listview):
            value = self._listview[self._index]
            self._index += 1
            return value
        else:
            raise StopIteration


if __name__ == '__main__':
    alist = [1, 2, 3, 4, 5]
    b = ListSliceView(alist, start=2, alen=3)
    len(b)
    print(b)
    assert b[2] == 5

    iterator = b.__iter__()
    assert next(iterator) == 3
    assert next(iterator) == 4
    assert next(iterator) == 5

    # with self.assertRaises(StopIteration):
    #     next(iterator)
    try:
        next(iterator)  # raises

    except StopIteration:
        print('Iterator successfully ended')
