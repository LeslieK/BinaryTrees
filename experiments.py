#from bst import BST
from redblacktrees2 import RedBlackBST
import random
import argparse
import math
from collections import OrderedDict
#import BTrees


def countRedNodes(N, num_trials=100):
    """
    N = number of random keys
    num_trials: at least 100
    """
    res = []
    black_heights = []
    heights = []
    dsumred = OrderedDict()
    dsumblack = OrderedDict()
    trials = num_trials
    # print "{:>10} {:>15}".format("trial",
    #                              "% red nodes")
    keys = range(N)
    while trials > 0:
        random.shuffle(keys)
        st = RedBlackBST()
        #st = BTrees.IOBTree.BTree()
        for k in keys:
            red_nodes_per_path, black_nodes_per_path = st.put(k, k)
            #print "red", red_nodes_per_path.items(),
            print sum(red_nodes_per_path.values()) / st.size()
            #print "black", black_nodes_per_path.items(),
            print sum(black_nodes_per_path.values()) / st.size()
            print
        dsumred = sumdicts(red_nodes_per_path, dsumred, keys)
        dsumblack = sumdicts(black_nodes_per_path, dsumblack, keys)
        #print "avg red per path:", mean(red_nodes),
        #print "avg percent red per path:", mean(percent_red_per_path)

        # output results
        percent_red = 100 * st.count_red_nodes() / float(N)
        # print "{:10} {:15}".format(num_trials - trials + 1,
        #                            percent_red)
        res.append(percent_red)
        black_heights.append(st.black_height())
        heights.append(st.height())
        trials -= 1
    for k in keys:
        dsumred[k] = dsumred[k] / num_trials
        dsumblack[k] = dsumblack[k] / num_trials

    return res, black_heights, heights, dsumred, dsumblack


def avgSearchTime(N=10000, num_trials=1000):
    """
    avg length of path to a random node =
    1 + (internal path length) / N
    """
    keys = range(N)
    trials = num_trials
    compares = []
    while trials > 0:
        random.shuffle(keys)
        st = RedBlackBST()
        for k in keys:
            st.put(k, k)
        avg_num_compares_to_a_node = (st.internalPathLengthAllNodes() / N) + 1
        compares.append(avg_num_compares_to_a_node)
        trials -= 1
    return math.log(N, 2) - .5, mean(compares), std(compares)


def avgCostPerPut(N, num_trials=1000):
    """
    avg cost to insert =
    external_path_length/N =
    (1 + internal_path_length/N) + 1
    (still think answer is 1 + E/N)
    """
    keys = range(N)
    trials = num_trials
    compares = []
    while trials > 0:
        random.shuffle(keys)
        st = RedBlackBST()
        for k in keys:
            st.put(k, k)
        avg_num_compares_to_insert = (st.internalPathLengthAllNodes() / N) + 2
        compares.append(avg_num_compares_to_insert)
        trials -= 1
    return mean(compares), std(compares)


def mean(x):
    """
    x: a list
    """
    return float(sum(x)) / len(x)


def std(x):
    """
    x: a list
    """
    m = mean(x)
    variance = [(i - m) ** 2 for i in x]
    return math.sqrt(mean(variance))


def sumdicts(d1, d2, keys):
    """
    dsum[k] = d1[k] + d2[k]
    """
    dsum = {}
    for k in keys:
        dsum[k] = d1[k] + d2.get(k, 0)
    return dsum

##############################
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", "-N", help="number of keys", type=int)
    parser.add_argument("--trials", "-t", default=100, help="num of trials",
                        type=int)
    args = parser.parse_args()

    # res, black_heights, heights, avg_red_nodes, avg_black_nodes = \
    #     countRedNodes(args.N, args.trials)
    # print "mean/std % red", mean(res), "/", std(res), "min/max", \
    #     min(res), "/", max(res)
    # print "mean/std black height", mean(black_heights), "/", \
    #     std(black_heights)
    # print "mean/std height", mean(heights), "/", std(heights)
    # print
    # #print "avg red nodes per path:", avg_red_nodes.items()
    # print
    # #print "avg black nodes per path", avg_black_nodes.items()
    # #print "avg black nodes per path:", avg_black_nodes.items()

############################################################################
    # calculate average search time (3.3.44)
    avg_search_times = []
    for i in xrange(1, args.N + 1):
        avg_search_times.append(avgSearchTime(i, args.trials))




