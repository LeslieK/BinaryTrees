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

    def __init__(self):
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

    def _balance(self, h):
        """
        consolidates all transformations in one function
        removes violations (right-leaning red links, 4-nodes) as recursion
        returns up the tree
        """
        # local transformations

        # rotateLeft: used for put
        #if h.right and self._isRed(h.right) and self._isBlack(h.left):
        #    h = self._rotateLeft(h)

        # rotateLeft: used for delete min
        # for delete min/max: don't need to check that h.left is BLACK since
        # it is null, and null is BLACK
        if h and self._isRed(h.right):
            h = self._rotateLeft(h)

        if h and self._isRed(h.left) and \
                self._isRed(h.left.left):
            h = self._rotateRight(h)

        if h and self._isRed(h.left) and \
                self._isRed(h.right):
            h = self._flipColors(h)

        h._count = _sizeOf(h.left) + _sizeOf(h.right) + 1
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
        minkey = findMin(self.root)
        maxkey = findMax(self.root)

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
        invariant: current node cannot be a 2-node
        in terms of bst: x or x.left must be RED
        """
        # if both children of root are BLACK, set root to RED
        # (makes flipColors work)
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
                # found min => delete it
                #print("deleted", x.key)
                return

            if self._isBlack(x.left) and self._isBlack(x.left.left):
                # x.left is a 2-node
                #print("calling moveRedLeft")
                x = self._moveRedLeft(x)

            x.left = helper_deleteMin(x.left)

            return self._balance(x)

        self.root = helper_deleteMin(self.root)

        if self.root:
            self.root.color = BLACK

        return self

    def deleteMax(self):
        """
        delete the max key in a RBTree
        invariant: current node cannot be a 2-node
        in terms of bst: x or x.right must be RED
        """
        if self._isBlack(self.root.left) and self._isBlack(self.root.right):
            self.root.color = RED

        def helper_deleteMax(x):
            """
            helper to deleteMax from RBTree
            """
            if x is None:
                # tree is empty
                return "BST underflow"

            if self._isRed(x.left):
                # left-leaning child => rotate it right
                x = self._rotateRight(x)

            if x.right is None:
                # you found the max => delete it
                #print("deleted", x.key)
                return

            if self._isBlack(x.right) and self._isBlack(x.right.left):
                # x.right is a 2-node: move red link down one level
                x = self._moveRedRight(x)

            # move down the right spine
            x.right = helper_deleteMax(x.right)

            return self._balance(x)

        self.root = helper_deleteMax(self.root)

        if self.root is not None:
            self.root.color = BLACK

        return self

    def delete(self, key):
        """
        delete a key at the bottom in a RBTree
        invariant: current node cannot be a 2-node
        in terms of bst: x or one of its children must be RED
        (x.right or x.left)
        """
        if not self.contains(key):
            return "key not found"

        def helper_delete(x, key):
            if key < x.key:
                # GO LEFT
                # follow code for deleteMin
                if self._isBlack(x.left) and self._isBlack(x.left.left):
                    # x.left is a 2-node; push red left
                    #print("calling moveRedLeft")
                    x = self._moveRedLeft(x)
                # continue down the left spine
                x.left = helper_delete(x.left, key)
            else:
                # DELETE NODE or GO RIGHT
                # follow code for deleteMax (not identical)
                if self._isRed(x.left):
                    x = self._rotateRight(x)
                if key == x.key and x.right is None:  # different on this line
                    # found node to delete (at bottom)
                    #print("deleting bottom key", x.key)
                    return None
                if self._isBlack(x.right) and self._isBlack(x.right.left):
                    # x.right is a 2-node; push red right
                    #print("calling moveRedRight")
                    x = self._moveRedRight(x)

                # check if current node is node to delete
                # (this node has 2 children)
                # EQUAL (not at bottom)
                if key == x.key:
                    #print("deleting key", key)
                    # copy successor node (key, value) to this node
                    x.key, x.value = findMin(x.right)
                    # then delete successor node
                    x.right = _deleteMin(self, x.right)
                else:
                    # continue down the right spine
                    x.right = helper_delete(x.right, key)

            return self._balance(x)

        # before recursion
        if self._isBlack(self.root.left) and self._isBlack(self.root.right):
            self.root.color = RED

        # recurse down tree and then back up tree
        self.root = helper_delete(self.root, key)

        # after recursion
        if self.root:
            self.root.color = BLACK

        return self

    def _moveRedLeft(self, x):
        """
        used to delete min in RBTree
        move red links down the left spine of RBTree
        if x is RED and x.left and x.left.left are BLACK
        then make h.left RED or one of its children RED
        corresponds to transformation on p.442
        (Algorithms 4th ed, Sedgewick and Wayne)
        """
        assert(x is not None)
        assert(self._isRed(x) and self._isBlack(x.left) and
               self._isBlack(x.left.left))
        x = self._flipColors(x)
        if self._isRed(x.right.left):
            # left 2-node can borrow from its siblings
            x.right = self._rotateRight(x.right)
            x = self._rotateLeft(x)
            # why isn't this invoked?
            #self._flipColors(x)
        return x

    def _moveRedRight(self, x):
        """
        used to delete max in RBTree
        move red links down the right spine of RBTree
        Assuming that x is red and both x.right and x.right.left are black,
        make x.right or one of its children red.
        """
        assert(x is not None)
        assert(self._isRed(x) and self._isBlack(x.left) and
               self._isBlack(x.right))
        x = self._flipColors(x)
        if self._isRed(x.left.left):
            x = self._rotateRight(x)
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


def _deleteMin(tree, x):
            """
            delete the key-value pair with the min key rooted at x
            """
            if x is None:
                # tree is empty
                return "BST underflow"

            if x.left is None:
                # found min => delete it
                return

            if tree._isRed(x) and tree._isBlack(x.left) and \
                    tree._isBlack(x.left.left):
                # x.left is a 2-node
                print("calling moveRedLeft")
                x = tree._moveRedLeft(x)

            x.left = _deleteMin(tree, x.left)

            return tree._balance(x)

#################################################
if __name__ == "__main__":

    keys = list("ABCDEFGHIJKLMNO")
    N = len(keys)

    t = RedBlackBST()
    for i in range(N):
        t.put(keys[i], i)
    t.inOrder()
    t.isRedBlackBST()
    t.height()
    t.black_height()

    #print("in range")
    #for k in t.range("C", "F"):
    #    print k

    #print(t.internalPathLength(), t.black_height())
    #print(t.isRedBlackBST())

    #for i in range(len(keys) - 1):
    #    t.deleteMax()
    #    print
    #    t.inOrder()
    #    print
    #print(t.size())

    #t.deleteMax()
    #print(t.size())

    import random
    random.shuffle(keys)
    for k in keys:
        print("key to delete: ", k)
        t.delete(k)



    ####################
    ## Exercise 3.3.24: Find % of red nodes in a random red-black BST
    ####################











