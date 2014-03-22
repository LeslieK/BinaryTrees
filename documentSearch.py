"""
Document search. Design an algorithm that takes a sequence of N document
words and a sequence of M query words and find the shortest interval in
which the M query words appear in the document in the order given. The
length of an interval is the number of words in that interval.

Hint (I thought of this!):
Hint: for each word, maintain a sorted list of the indices in the document
in which that word appears.
Scan through the sorted lists of the query words in a judicious manner.
"""

from collections import defaultdict


def docSearch(filename, query_list):
    """
    return the shortest interval in which the query_list appears, in order
    """

    # index the document
    st = indexDoc(filename)
    query_list = map(lambda w: w.lower(), query_list)

    word0 = query_list[0]
    min_interval = ""
    for p0 in st[word0]:
        p = p0              # iterate thru all positions in word0
        for word in query_list[1:]:
            if p + 1 > st[word][-1]:
                return st[min_interval]
            i = binsearch(st[word], p + 1)  # i: ith index in word list
            p = st[word][i]                # p: abs position of word in doc

        # after looping thru all query words: store min interval
        if st[min_interval] == []:
            st[min_interval] = [p0, p]
        elif interval_range([p0, p]) < interval_range(st[min_interval]):
            st[min_interval] = [p0, p]

        if interval_range(st[min_interval]) == len(query_list):
            # found the minimum interval
            return st[min_interval]

    return st[min_interval]


def interval_range(alist):
    return alist[1] - alist[0]


def indexDoc(filename):
    st = defaultdict(list)
    index = -1
    with open(filename, 'r') as f:
        words = (word.lower() for line in f for word in line.split())

        for word in words:
            index += 1
            st[word].append(index)
    return st


def binsearch(alist, key):
    low = 0
    high = len(alist) - 1
    while low <= high:

        mid = low + (high - low) / 2
        if key < alist[mid]:
            high = mid - 1
        elif key > alist[mid]:
            low = mid + 1
        else:
            return mid
    return low

####################################
if __name__ == "__main__":
    #st = indexDoc("tiny.txt")
    st = indexDoc("TaleOfTwoCities.txt")
    #interval = docSearch("tiny.txt", ["a", "sorted", "query"])
    #interval = docSearch("TaleOfTwoCities.txt", ["the", "best", "of"])
    interval = docSearch("TaleOfTwoCities.txt", ["elicit", "boar", "manner"])

    print interval


