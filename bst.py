
from visualizerAccumulator import VisualAnalyzer


class Node(object):

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self._count = 1

    def size(self):
        return self._count


class BST(object):

    def __init__(self, trials=None, maxval=None):
        self.root = None
        self.count = 0  # counts 'put' compares
        if trials:
            self.a = VisualAnalyzer(trials, maxval)

    def put(self, key, value):
        self.count = 0

        def helper_put(x, key, value):
            if x is None:
                self.count += 1
                return Node(key, value)
            self.count += 1  # book counts compareTo() not primitive < and >
            if key < x.key:
                x.left = helper_put(x.left, key, value)
                #self.count += 1
            elif key > x.key:
                x.right = helper_put(x.right, key, value)
                #self.count += 2
            else:
                x.value = value
                #self.count += 2

            x._count = _sizeOf(x.left) + _sizeOf(x.right) + 1
            return x

        self.root = helper_put(self.root, key, value)
        if self.a:
            self.a.addDataValue(self.count)

        return self

    def get(self, key):
        def helper_get(x, key):
            if x is None:
                return
            if key == x.key:
                return x.value
            elif key < x.key:
                return helper_get(x.left, key)
            else:
                return helper_get(x.right, key)
        return helper_get(self.root, key)

    def contains(self, key):
        return self.get(key) is not None

    def delMin(self):
        """
        deletes min element in BST (excl root)
        """
        def helper_delMin(x):
            if x.left is None and x is self:
                return "can't delete root"
            if x.left is None:
                return x.right
            x.left = helper_delMin(x.left)
            x._count = _sizeOf(x.left) + _sizeOf(x.right) + 1
            return x
        helper_delMin(self.root)

    def delMax(self):
        """
        deletes max element in BST (excl root)
        """
        def helper_delMax(x):
            if x.right is None and x is self:
                return "can't delete root"
            if x.right is None:
                return x.left
            x.right = helper_delMax(x.right)
            x._count = _sizeOf(x.left) + _sizeOf(x.right) + 1
            return x
        helper_delMax(self.root)

    def delete(self, key):
        """
        Hilbert delete
        deletes node with given key
        """
        def helper_delete(x, k):
            if x is None:
                return
            if k == self.key:
                return "can't delete root"
            if k < x.key:
                x.left = helper_delete(x.left, k)
            elif k > x.key:
                x.right = helper_delete(x.right, k)
            else:
                if x.right is None:
                    return x.left
                if x.left is None:
                    return x.right
                else:
                    t = x
                    x = findMin(t.right)
                    x.right = t.right.delMin()
                    x.left = t.left
            x._count = _sizeOf(x.left) + _sizeOf(x.right) + 1
            return x
        helper_delete(self.root, key)

    def inOrder(self):
        def helper_inOrder(x):
            if x is None:
                return
            helper_inOrder(x.left)
            print x.key, x.value
            helper_inOrder(x.right)
        return helper_inOrder(self.root)

    def __iter__(self):
        return _in_order_g(self.root)

    def height(self):
        """
        returns the height of tree
        """
        def helper_height(x, count):
            if x is None:
                return count - 1
            return max(helper_height(x.left, count + 1),
                       helper_height(x.right, count + 1))
        return helper_height(self.root, 0)

    def internalPathLength(self):
        def helper_internal_path(x):
            if x is None:
                return 0
            return helper_internal_path(x.left) + \
                helper_internal_path(x.right) + x.size() - 1
        return helper_internal_path(self.root)

    # def size(self):
    #     return _sizeOf(self.root)

    def size(self, lo=None, hi=None):
        if lo is None:
            return _sizeOf(self.root)

        def helper_size(x, cnt, lo, hi):
            if x is None:
                return cnt
            if lo < x.key:
                cnt = helper_size(x.left, cnt, lo, hi)
            if x.key < hi:
                cnt = helper_size(x.right, cnt, lo, hi)
            if lo <= x.key <= hi:
                cnt += 1
            return cnt
        return helper_size(self.root, 0, lo, hi)

    def range(self, lo, hi):
        """
        returns a generator
        yields keys in range

        """
        return _in_range_g(self.root, lo, hi)

    def minkey(self):
        def helper_minkey(x):
            if x is None:
                return
            if x.left is None:
                return x.key
            return helper_minkey(x.left)
        return helper_minkey(self.root)

    def maxkey(self):
        def helper_maxkey(x):
            if x is None:
                return
            if x.right is None:
                return x.key
            return helper_maxkey(x.right)
        return helper_maxkey(self.root)

    def floor(self, key):
        """
        return largest key less than query
        """
        def helper_floor(x, key):
            if x:
                if key == x.key:
                    return key
                if key < x.key:
                    return helper_floor(x.left, key)
                if key > x.key:
                    t = helper_floor(x.right, key)
                    if t:
                        return t
                    else:
                        return x.key
        return helper_floor(self.root, key)

    def ceiling(self, key):
        """
        return smallest key greater than query
        """
        def helper_ceiling(x, key):
            if x:
                if key == x.key:
                    return key
                if key > x.key:
                    return helper_ceiling(x.right, key)
                if key < x.key:
                    t = helper_ceiling(x.left, key)
                    if t:

                        return t
                    else:
                        return x.key
        return helper_ceiling(self.root, key)

    def rank(self, key):
        """
        return number of keys < query
        """
        def helper_rank(x, key):
            if x is None:
                return 0
            if x.left is None:
                return 0
            if key < x.key:
                return helper_rank(x.left, key)
            if key > x.key:
                return x.left.size() + 1 + helper_rank(x.right, key)
            return x.left.size()
        return helper_rank(self.root, key)

    def select(self, k):
        """
        return key with rank k
        """
        def helper_select(x, k):
            if x is None:
                return
            if k < self.rank(x.key):
                return x.left and helper_select(x.left, k)
            if k > self.rank(x.key):
                return x.right and helper_select(x.right, k)
            return x.key
        return helper_select(self.root, k)


def findMin(tree):
    if tree is None:
        return
    if tree.left is None:
        return tree.key
    return findMin(tree.left)


def findMax(tree):
    if tree:
        if tree.right is None:
            return tree.key
        return findMax(tree.right)


def _sizeOf(x):
    """
    x: root node
    """
    if x is None:
        return 0
    return x._count


def _in_range_g(node, lo, hi):
    if node:
        if lo < node.key:
            for x in _in_range_g(node.left, lo, hi):
                yield x
        if lo <= node.key <= hi:
            yield node.key
        if node.key < hi:
            for x in _in_range_g(node.right, lo, hi):
                yield x


def _in_order_g(node):
    if node:
        for x in _in_order_g(node.left):
            yield x
        yield node.key
        for x in _in_order_g(node.right):
            yield x


#################################################
if __name__ == "__main__":
    # keys = list("EASYQUTION")
    # N = len(keys)

    # t = BST()
    # for i in range(N):
    #     t = t.put(keys[i], i)
    # t.inOrder()
    # print t.internalPathLength(), t.height()
    ####################
    ## Exercise 3.3.24: Find % of red nodes in a random red-black BST
    ####################
    ####################
    ## visualize put compares
    ####################

    """
    trials = 50
    maxval = 30

    b = BST(trials, maxval)

    keys = range(trials)
    import random
    random.shuffle(keys)
    for k in keys:
        b.put(k, k)
    b.a.plotData()
    """

    with open("TaleOfTwoCities.txt") as f:
        words = (word for line in f for word in line.split() if len(word) > 7)
        total = (1 for word in words)
        print sum(total)












