
# from collections import deque
RED = True
BLACK = False


class Node(object):

    def __init__(self, key, value, color=BLACK):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self._count = 1
        self.color = color

    def size(self):
        return self._count


class RedBlackBST(object):

    def __init__(self, trials=None, maxval=None, title=None):
        self.root = None

    def put(self, key, value):

        def helper_put(x, key, value):
            if x is None:
                return Node(key, value, RED)

            # book counts compareTo() not primitive < and >
            if key < x.key:
                x.left = helper_put(x.left, key, value)
            elif key > x.key:
                x.right = helper_put(x.right, key, value)
            else:
                x.value = value

            # local transformations
            if x.right and self._isRed(x.right):
                x = self._rotateLeft(x)

            if x.left and x.left.left and self._isRed(x.left) and \
                    self._isRed(x.left.left):
                x = self._rotateRight(x)

            if x.right and x.left and self._isRed(x.left) and \
                    self._isRed(x.right):
                x = self._flipColors(x)

            x._count = _sizeOf(x.left) + _sizeOf(x.right) + 1
            return x

        self.root = helper_put(self.root, key, value)
        self.root.color = BLACK

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

    def inOrder(self):
        def helper_inOrder(x):
            if x is None:
                return
            helper_inOrder(x.left)
            print(x.key)
            helper_inOrder(x.right)
        return helper_inOrder(self.root)

    def range(self, lo, hi):
        def range_g(x, lo, hi):
            if x:
                if x.key > lo:
                    for n in range_g(x.left, lo, hi):
                        yield n
                if lo <= x.key <= hi:
                        yield x.key
                if x.key < hi:
                    for n in range_g(x.right, lo, hi):
                        yield n
        g = range_g(self.root, lo, hi)
        return g

    def __iter__(self):
        return _in_order_g(self.root)

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
        return key, value with rank k
        """
        def helper_select(x, k):
            if x is None:
                return
            if k < self.rank(x.key):
                return x.left and helper_select(x.left, k)
            if k > self.rank(x.key):
                return x.right and helper_select(x.right, k)
            return x.key, x.value
        return helper_select(self.root, k)

    def _rotateLeft(self, h):
        """
        h: a node
        """
        x = h.right
        h.right = x.left
        x.left = h
        x.color = h.color
        h.color = RED
        x._count = h._count
        h._count = 1 + _sizeOf(h.left) + _sizeOf(h.right)
        return x

    def _rotateRight(self, h):
        """
        h: a node
        """
        x = h.left
        h.left = x.right
        x.right = h
        x.color = h.color
        h.color = RED
        x._count = h._count
        h._count = _sizeOf(h.left) + _sizeOf(h.right) + 1
        return x

    def _balance(self, x):
        """
        consolidates all transformations in one function
        same as local transformations used in put() except for
        rotateLeft; in deleteMin no need to check if x.left is BLACK
        after min delete it is None which is BLACK
        """

        # local transformations

        # rotateLeft for delete min
        # don't have to check if x.left is BLACK
        # since it is None and None is BLACK
        if x.right and self._isRed(x.right):
            x = self._rotateLeft(x)

        # for put: do have to check if x.left is BLACK
        # if x.right and self._isRed(x.right) and self._isBlack(x.left):
        #     x = self._rotateLeft(x)

        if x.left and x.left.left and self._isRed(x.left) and \
                self._isRed(x.left.left):
            x = self._rotateRight(x)

        if x.right and x.left and self._isRed(x.left) and \
                self._isRed(x.right):
            x = self._flipColors(x)

        x._count = _sizeOf(x.left) + _sizeOf(x.right) + 1
        return x

    def _flipColors(self, h):
        """
        h: a node
        parent is RED and children are BLACK
        used to put into a RBTree
        used to split 4-nodes
        """
        assert(self._isRed(h) and
               self._isBlack(h.left) and
               self._isBlack(h.right)
               or (self._isBlack(h) and
                   self._isRed(h.left) and
                   self._isRed(h.right)))
        h.color = not h.color
        h.left.color = not h.left.color
        h.right.color = not h.right.color
        return h

    def _isRed(self, x):
        if x is None:
            return False
        else:
            return x.color == RED

    def _isBlack(self, x):
        if x is None:
            return True
        else:
            return x.color == BLACK

    def isBalanced(self):
        """
        all paths from root to null node must have same black_height
        """

        def helper_isBalanced(x, count):
            if x is None:
                return True
            if x.color == BLACK:
                # print helper_isBalanced(x.left, count + 1),
                # helper_isBalanced(x.right, count + 1)
                return helper_isBalanced(x.left, count + 1) == \
                    helper_isBalanced(x.right, count + 1)
            else:
                # print helper_isBalanced(x.left, count),
                # helper_isBalanced(x.right, count)
                return helper_isBalanced(x.left, count) == \
                    helper_isBalanced(x.right, count)

        return helper_isBalanced(self.root.left, 0) == \
            helper_isBalanced(self.root.right, 0)

    def is23(self):
        """
        certifies that every node is a 2-3 node:
        - no right leaning red links
        - no consecutive red links (parent of a red node cannot be red)
        """
        def helper_is23(x):
            if self._isRed(x) and self._isRed(x.left):
                return False
            if self._isBlack(x) and self._isRed(x.right):
                return False
            return True
        return helper_is23(self.root)

    def isRedBlackBST(self):
        """
        - a binary search tree
        - 2-3 nodes and is balanced
        """
        return self.isBST() and self.isBalanced() and self.is23()

    def black_height(self):
        """
        returns the black height of tree
        height = number of black links on any path from root to null link
        so I only count links on leftmost path
        """
        def helper_height(x, count):
            if x is None:
                return count
            if self._isBlack(x.left):
                return helper_height(x.left, count + 1)
            else:
                return helper_height(x.left, count)
        return helper_height(self.root, 0)

    def height(self):
        """
        returns total height (black + red nodes) of tree
        """
        def helper_height(x, count):
            if x is None:
                return count
            else:
                return max(helper_height(x.left, count + 1),
                           helper_height(x.right, count + 1))
        return helper_height(self.root, 0)

    def internalPathLength(self):
        """
        return the sum of the depths of all nodes
        (take into account the color of the node)
        """
        def helper_internal_path(x):
            if x is None:
                return 0
            if self._isBlack(x):
                return helper_internal_path(x.left) + \
                    helper_internal_path(x.right) + x.size() - 1
            else:
                return helper_internal_path(x.left) + \
                    helper_internal_path(x.right) - 1
        return helper_internal_path(self.root)

    def internalPathLengthAllNodes(self):
        """
        """
        def helper_internal_path(x):
            if x is None:
                return 0
            return helper_internal_path(x.left) + \
                helper_internal_path(x.right) + x.size() - 1
        return helper_internal_path(self.root)

    def size(self):
        return _sizeOf(self.root)

    def isBST(self):
        minkey, _ = findMin(self.root)
        maxkey, _ = findMax(self.root)

        def helper_isBST(x, minval, maxval):
            if x is None:
                return True
            if x.key < minval:
                return False
            if x.key > maxval:
                return False
            return helper_isBST(x.left, minval, x.key) and \
                helper_isBST(x.right, x.key, maxval)
        return helper_isBST(self.root, minkey, maxkey)

    def deleteMin(self):
        """
        delete min key in a RBTree
        """
        # if both children of root is BLACK, set root to RED (why)?
        if self._isBlack(self.root.left) and self._isBlack(self.root.right):
            self.root.color = RED

        def helper_deleteMin(x):
            """
            delete the key-value pair with the min key rooted at x
            """
            if x is None:
                # tree is empty
                return "BST underflow"

            if x.left is None:
                return

            if self._isRed(x) and self._isBlack(x.left) and \
                    self._isBlack(x.left.left):
                # h.left is a 2-node
                x = self._moveRedLeft(x)

            x.left = helper_deleteMin(x.left)

            return self._balance(x)

        self.root = helper_deleteMin(self.root)

        if self.root is not None:
            self.root.color = BLACK

        return self

    def deleteMax(self):
        pass

    def delete(self, key):
        pass

    def _moveRedLeft(self, x):
        """
        used to delete min in RBTree
        move red links down the left spine of RBTree
        if x is RED and x.left and x.left.left are BLACK
        then make h.left RED or one of its children RED
        correspondes to transformation on p.442
        """
        x = self._flipColors(x)
        if self._isRed(x.right.left):
            # left 2-node can borrow from its siblings
            x.right = self._rotateRight(x.right)
            x = self._rotateLeft(x)
            # why isn't this invoked (see booksite code)?
            # is it because _balance splits nodes on the way up?
            self._flipColors(x)  # splits nodes on the way down
        return x


def findMin(x):
    """
    x: a node
    """
    if x is None:
        return
    if x.left is None:
        return x.key, x.value
    return findMin(x.left)


def findMax(x):
    """
    x: a node
    """
    if x is None:
        return
    if x.right is None:
        return x.key, x.value
    return findMax(x.right)


def _sizeOf(x):
    """
    x: root node
    """
    if x is None:
        return 0
    else:
        return x._count


def _in_order_g(node):
    if node:
        for x in _in_order_g(node.left):
            yield x
        yield node.key
        for x in _in_order_g(node.right):
            yield x

#################################################
if __name__ == "__main__":

    keys = list("ABCDEFG")
    N = len(keys)

    t = RedBlackBST()
    for i in range(N):
        t.put(keys[i], i)
    t.inOrder()
    t.isRedBlackBST()
    t.height()
    t.black_height()

    print("keys in range")
    for k in t.range("C", "F"):
        print(k)

    # for i in range(len(keys) - 1):
    #     t.deleteMin()
    #     print
    #     t.inOrder()
    #     print
    # print(t.size())

    # print(t.deleteMin().size())












