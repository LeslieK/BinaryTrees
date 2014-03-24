"""
Generalized queue. Design a generalized queue data type that supports all of
the following operations in logarithmic time (or better) in the worst case.
Create an empty data structure.
Append an item to the end of the queue.
Remove an item from the front of the queue.
Return the ith item in the queue.
Remove the ith item from the queue.
"""

import redblacktrees as RBT


class GeneralizedQueue(object):
    def __init__(self):
        # use a balanced search tree as the underlying data structure
        self.queue = RBT.RedBlackBST()
        self.next_key = 0

    def append(self, item):
        """
        append to end of queue
        """
        self.queue.put(self.next_key, item)
        self.next_key += 1

    def pop(self):
        """
        remove from the front of queue
        """
        item, value = RBT.findMin(self.queue.root)
        self.queue.deleteMin()
        return value

    def peek(self, i):
        """
        return the ith item from the queue
        """
        _, value = self.queue.select(i)
        return value

    def delete(self, i):
        """
        delete the ith item from the queue
        """
        self.queue.delete(i)
        pass

###################################################
if __name__ == "__main__":
    q = GeneralizedQueue()
    keys = "ABCDEFGHIJKLMNOP"
    for k in keys:
        q.append(k)

    print("peeking")
    print(q.peek(0))
    print(q.peek(len(keys) / 3))
    print(q.peek(len(keys) - 1))

    print("popping")
    for i in range(len(keys) / 2):
        print(q.pop())

    q.append('ZZZZ')

    for i in range(len(keys) / 2):
        print(q.pop())

    print(q.peek(0))





