import random
from info import info_gain
import g_vars


def select_col(examples, a):
    res = []
    for i in examples:
        res.append(i[a])
    return res


def choose_attribute(examples, attr):
    global max_gain
    global best_attr
    global best_thresh
    max_gain = -1
    best_attr = -1
    best_thresh = -1

    def thresh_optimize(a):
        global max_gain
        global best_attr
        global best_thresh
        attr_val = select_col(examples, a)
        l = min(attr_val)
        m = max(attr_val)
        for k in range(1, 51):
            thresh = l + ((k * (m - l)) / 51)
#           For each threshold, measure the information gain attained on these
#           examples using that combination of attribute A and threshold.
            gain = info_gain(examples, a, thresh)
            if gain > max_gain:
                max_gain = gain
                best_attr = a
                best_thresh = thresh

    if g_vars.option == "optimized":
        for a in attr:
            thresh_optimize(a)

    elif g_vars.option == "randomized":
        a = random.choice(attr)
        thresh_optimize(a)

    elif g_vars.option == "forest3":
        a = random.choice(attr)
        thresh_optimize(a)

    elif g_vars.option == "forest15":
        a = random.choice(attr)
        thresh_optimize(a)

    return(best_attr, best_thresh, max_gain)
