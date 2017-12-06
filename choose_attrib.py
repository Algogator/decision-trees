import random
from info import info_gain

def select_col(examples, a):
    res = []
    # print examples[-1]
    for i in examples:
        # print i,i[a]
        res.append(i[a])
    # print res
    return res

def choose_attribute(examples, attr, option):
    global max_gain
    global best_attr
    global best_thresh
    max_gain = -1
    best_attr = -1
    best_thresh = -1
    # print attr, examples
    def thresh_optimize(a):
        global max_gain
        global best_attr
        global best_thresh
        attr_val = select_col(examples, a)
        l  = min(attr_val)
        m = max(attr_val)
        for k in range(1,51):
            # print k
            thresh = l + ((k*(m-l))/51)
#           For each threshold, measure the information gain attained on these
#           examples using that combination of attribute A and threshold.
            gain = info_gain(examples, a, thresh)
            # print gain, "gain"
            if gain > max_gain:
                max_gain = gain
                best_attr = a
                best_thresh = thresh
    if option == "optimized":
        for a in attr:
            thresh_optimize(a)
            #attribute _values is the array containing the values of all examples for attribute A
            # print a
    elif option == "randomized":
        a = random.choice(attr)
        thresh_optimize(a)

    elif option == "forest3":
        a = random.choice(attr)
        thresh_optimize(a)

    elif option == "forest15":
        a = random.choice(attr)
        thresh_optimize(a)

        # print best_attr, best_thresh, "@@@@"
    return(best_attr,best_thresh,max_gain)
