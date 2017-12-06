import math
import g_vars
import pdb

def entropy(l):
    # pdb.set_trace()
    # No of samplesin this node
    suminnode = len(l)
    s1 = 0
    # Sum of each class in node for each example
    classlist = [0] * g_vars.classnum
    # For each attribute find sum of all classes in it
    for i in l:
        classlist[i[-1]] += 1
    for i in range(g_vars.classnum):
        val = float(classlist[i]) / suminnode
        if classlist[i]:
            s1 -= (val * math.log(val,2))
    return s1

def info_gain_list(l, r):
    s1 = s2 = P = 0
    sum1 = len(l)
    sum2 = len(r)
    s = len(l) + len(r)
    if l:
        s1 = entropy(l)
    if r:
        s2 = entropy(r)
    # pdb.set_trace()
    P = entropy(l + r)
    gain = P - (s1 * (sum1 / float(s))) - (s2 * (sum2 / float(s)))
    return gain


def separate(examples, a, thresh):
    left = []
    right = []
    for i in range(len(examples)):
        if examples[i][a] < thresh:
            left.append(examples[i])
        else:
            right.append(examples[i])
    return (left, right)


def info_gain(examples, a, thresh):
    gain = 0
    left, right = separate(examples, a, thresh)
    return info_gain_list(left, right)


def sameclass(examples):
    c = examples[0][-1]
    for i in range(1, len(examples)):
        if c != examples[i][-1]:
            return False
        else:
            c = examples[i][-1]
    return True


def DISTRIBUTION(examples):
    distlist = [0] * g_vars.classnum
    s = len(examples)
    res = []
    for i in examples:
        distlist[i[-1]] += 1
    for i in distlist:
        res.append(i / float(s))
    return res
