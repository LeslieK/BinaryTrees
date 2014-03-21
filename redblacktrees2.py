import random
from collections import OrderedDict
from collections import deque
from visualizerAccumulator import VisualAnalyzer
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

    def __init__(self, trials=None, maxval=None):
        self.root = None
        self._red_count = 0
        self._black_count = 0
        # key: node(path)  value: # red nodes on path
        self.red_nodes = OrderedDict()
        self.black_nodes = OrderedDict()
        self.count_compares = 0     # counts compares
        self.count_rotations = 0    # count rotations
        self.count_node_splits = 0  # count node splits
        if trials:
            self.a = VisualAnalyzer(trials, maxval)  # used to plot data

    def put(self, key, value):
        self.count_compares = 0
        self.count_rotations = 0
        self.count_node_split = 0

        def helper_put(x, key, value):
            if x is None:
                self.count_compares += 1
                if x is not self.root:
                    self.red_nodes[key] = self.red_nodes.get(key, 0) + 1
                else:
                    self.black_nodes[key] = self.black_nodes.get(key, 0) + 1
                return Node(key, value, RED)

            self.count_compares += 1  # book counts compareTo() not primitive < and >
            if key < x.key:
                if self._isRed(x):
                    self.red_nodes[key] = self.red_nodes.get(key, 0) + 1
                else:
                    self.black_nodes[key] = self.black_nodes.get(key, 0) + 1
                x.left = helper_put(x.left, key, value)
                #self.count_compares += 1
            elif key > x.key:
                if self._isRed(x):
                    self.red_nodes[key] = self.red_nodes.get(key, 0) + 1
                else:
                    self.black_nodes[key] = self.black_nodes.get(key, 0) + 1
                x.right = helper_put(x.right, key, value)
                #self.count_compares += 2
            else:
                x.value = value
                #self.count_compares += 2

            # local transformations
            if x.right and self._isRed(x.right):
                x = self._rotateLeft(x)
                self.count_rotations += 1
                # add 1 red node
                self.red_nodes[x.left.key] = \
                    self.red_nodes.get(x.left.key, 0) + 1
                # add 1 red node to subtree
                self.red_nodes = addRedNode(x.left.left, self.red_nodes)
                # sub 1 red node
                self.red_nodes[x.key] -= 1
                # sub 1 red node from subtree
                self.red_nodes = subRedNode(x.right, self.red_nodes)

            if x.left and x.left.left and self._isRed(x.left) and \
                    self._isRed(x.left.left):
                x = self._rotateRight(x)
                self.count_rotations += 1
                # add 1 red node
                self.red_nodes[x.right.key] = \
                    self.red_nodes.get(x.right.key, 0) + 1
                self.red_nodes = addRedNode(x.right.right, self.red_nodes)
                # sub 1 red node
                self.red_nodes[x.key] -= 1
                self.red_nodes = subRedNode(x.left, self.red_nodes)

            if x.right and x.left and self._isRed(x.left) and \
                    self._isRed(x.right):
                x = self._flipColors(x)
                self.count_node_split += 1

                if x == self.root:
                    # split the root
                    # sub 1 red node from x.left and x.right
                    self.red_nodes = subRedNode(x.left, self.red_nodes)
                    self.red_nodes = subRedNode(x.right, self.red_nodes)
                    # add 1 black node to all paths
                    for k in range(self.size()):
                        self.black_nodes[k] = self.black_nodes.get(k, 0) + 1
                        # but x remains unchanged
                    self.black_nodes[x.key] -= 1
                else:
                    # add 1 red node to x
                    # sub 1 black node from x
                    self.red_nodes[x.key] += 1
                    self.black_nodes[x.key] -= 1

            x._count = _sizeOf(x.left) + _sizeOf(x.right) + 1
            return x

        self.root = helper_put(self.root, key, value)
        self.root.color = BLACK
        if self.a:
            self.a.addDataValue(self.count_compares)
            #self.a.addDataValue(self.count_rotations)

        return self.red_nodes, self.black_nodes

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
            #x._count = _sizeOf(x.left) + _sizeOf(x.right) + 1
            return x
        helper_delete(self.root, key)

    def inOrder(self):
        def helper_inOrder(x):
            if x is None:
                return
            helper_inOrder(x.left)
            print x.key, x.value, x.color
            helper_inOrder(x.right)
        return helper_inOrder(self.root)

    def range(self, lo, hi):
        """
        return an iterable of keys in range
        """
        q = deque()

        def helper_range(x, lo, hi):
            """
            x: a node
            """
            if x is None:
                return
            if x.root > lo:
                helper_range(x.left, lo, hi)
            if lo <= x.root <= hi:
                q.append(x.key)
            if x.root < hi:
                helper_range(x.right, lo, hi)

        helper_range(self.root)
        return q

    def __iter__(self):
        return _in_order_g(self.root)

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

    def _flipColors(self, h):
        """
        h: a node
        """
        h.left.color = BLACK
        h.right.color = BLACK
        h.color = RED
        return h

    def _isRed(self, x):
        if x is None:
            return False
        else:
            return x.color == RED

    def _isBlack(self, x):
        if x is None:
            return False
        else:
            return x.color == BLACK

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

    def count_red_nodes(self):
        def helper_count_red_nodes(x):
            if x is None:
                return 0
            return helper_count_red_nodes(x.left) + \
                helper_count_red_nodes(x.right) + \
                1 * self._isRed(x)
        return helper_count_red_nodes(self.root)

    def count_black_nodes(self):
        return self.size() - self.count_red_nodes()

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


def addRedNode(x, red_nodes):
    """
    add a red node to all nodes in tree x
    x: a node
    """
    if x is None:
        return red_nodes
    red_nodes[x.key] += 1
    red_nodes = addRedNode(x.left, red_nodes)
    red_nodes = addRedNode(x.right, red_nodes)
    return red_nodes


def subRedNode(x, red_nodes):
    """
    sub a red node from all nodes in tree x
    x: a node
    """
    if x is None:
        return red_nodes
    red_nodes[x.key] -= 1
    red_nodes = subRedNode(x.left, red_nodes)
    red_nodes = subRedNode(x.right, red_nodes)
    return red_nodes


def findMin(tree):
    if tree is None:
        return
    if tree.left is None:
        return tree.key
    return findMin(tree.left)


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


def genrandomtree(N):
    """
    build 2 16-node random red-black BSTs
    """
    keys = range(N)

    # build red-black BST t1
    random.shuffle(keys)
    t1 = RedBlackBST()
    for i in range(N):
        t1 = t1.put(keys[i], i)

    # build red-black BST t2
    random.shuffle(keys)
    t2 = RedBlackBST()
    for i in range(N):
        t2 = t2.put(keys[i], i)

    return t1, t2


#################################################
if __name__ == "__main__":

    keys = list("EASYQUTION")
    N = len(keys)

    t = RedBlackBST()
    for i in range(N):
        t = t.put(keys[i], i)
    t.inOrder()
    print t.internalPathLength(), t.black_height()


    ####################
    ## Exercise 3.3.24: Find % of red nodes in a random red-black BST
    ####################











